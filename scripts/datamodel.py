# ruff: noqa: E402
# %%
from pathlib import Path
from typing import Any, TypedDict

import xmltodict
from typing_extensions import TypeGuard

Description = TypedDict(
    "Description",
    {"@xmi:id": str, "@xmi:type": str, "@name": str},
)


class Specification(TypedDict, total=False):
    xmi_id: str
    package: str
    name: str
    code: str
    json: Description
    attributes: dict[str, str]
    dependencies: set[str]
    general: str


class Enumeration(Description):
    ownedLiteral: Description | list[Description]


Bounds = TypedDict("Bounds", {"@value": str})

AttributeRef = TypedDict("AttributeRef", {"@xmi:idref": str})

Attribute = TypedDict(
    "Attribute",
    {
        "@xmi:id": str,
        "@xmi:type": str,
        "@name": str,
        "type": AttributeRef,
        "lowerValue": Bounds,
        "upperValue": Bounds,
    },
)


class Reference(TypedDict):
    type: str
    dep: None | str


class Class(Description):
    ownedAttribute: list[Attribute]


def is_enum(entry: Description) -> TypeGuard[Enumeration]:
    return entry["@xmi:type"] == "uml:Enumeration"


def is_primitive(entry: Description) -> bool:
    return entry["@xmi:type"] == "uml:PrimitiveType"


def is_class(entry: Description) -> TypeGuard[Class]:
    return entry["@xmi:type"] == "uml:Class"


class Package:
    def __init__(self, package_description: dict[str, Any]) -> None:
        self.packages = package_description

    @classmethod
    def from_file(
        cls, path: Path = Path("model") / "datamodel.xmi"
    ) -> "Package":
        datamodel = xmltodict.parse(path.read_text())
        model = datamodel["xmi:XMI"]["uml:Model"]
        packages = dict(
            (
                element["@name"],
                dict(
                    (package["@xmi:id"], package)
                    for package in element.get("packagedElement", [])
                    if not isinstance(package, str)
                ),
            )
            for element in model["packagedElement"]["packagedElement"]
        )
        return cls(packages)

    def process_enum(self, entry: Enumeration) -> Specification:
        assert entry["@xmi:type"] == "uml:Enumeration"
        literals = entry["ownedLiteral"]
        if not isinstance(literals, list):
            literals = [literals]
        package = entry["@xmi:id"].split(".")[-2]

        return {
            "name": entry["@name"],
            "package": package,
            "xmi_id": entry["@xmi:id"],
            "code": "{} = Literal[{}]".format(
                entry["@name"],
                ", ".join('"' + k["@name"] + '"' for k in literals),
            ),
            "json": entry,
            "dependencies": set(),
        }

    def process_primitive(self, entry: Description) -> Specification:
        name = entry["@name"]
        package = entry["@xmi:id"].split(".")[-2]
        return {
            "name": name,
            "package": package,
            "xmi_id": entry["@xmi:id"],
            "code": f"{name} = str",
            "json": entry,
            "dependencies": set(),
        }

    def process_attribute(
        self, entry: Attribute, orig_package: str
    ) -> Reference:
        # Some primitive types
        if entry["type"]["@xmi:idref"] == "ID_Boolean":
            return {"type": "Literal['true', 'false']", "dep": None}
        if (
            entry["type"]["@xmi:idref"]
            in self.packages["PrimitiveTypes"].keys()
        ):
            return {"type": "str", "dep": None}

        # Otherwise
        arity_low = entry["lowerValue"]["@value"]
        arity_up = entry["upperValue"]["@value"]

        identifier = entry["type"]["@xmi:idref"]
        reference = self.find_entry(identifier)
        name = reference["@name"]
        package = identifier.split(".")[-2]
        if package != orig_package:
            name = f"{package}.{name}"

        if arity_low == "1" and arity_up == "1":
            return {"type": name, "dep": identifier}
        if arity_low == "0" and arity_up == "1":
            return {
                "type": f"{name}",
                "dep": identifier,
            }  # TODO NotRequired fails when only one entry
        if arity_up != "1":  # "*":
            return {"type": f"Union[{name}, list[{name}]]", "dep": identifier}

        print(entry)

        raise ValueError(f"Unexpected arity {arity_low} - {arity_up}")

    def process_class(self, entry: Class) -> Specification:
        assert entry["@xmi:type"] == "uml:Class"
        name = entry["@name"]
        attributes: Attribute | list[Attribute] = entry.get(
            "ownedAttribute", []
        )
        if not isinstance(attributes, list):
            attributes = [attributes]

        package = entry["@xmi:id"].split(".")[-2]

        rep: Specification = {
            "xmi_id": entry["@xmi:id"],
            "package": package,
            "name": name,
            "json": entry,
            "dependencies": set(
                dep
                for attr in attributes
                if (dep := self.process_attribute(attr, package)["dep"])
                is not None
            ),
            "attributes": {
                attr["@name"]: self.process_attribute(attr, package)["type"]
                for attr in attributes
            },
            "general": "TypedDict, total=False",
        }
        if gen := entry.get("generalization", None):
            general = gen["@general"]  # type: ignore
            gen_package = general.split(".")[-2]
            gen_name = general.split(".")[-1]
            if gen_package == package:
                rep["general"] = gen_name
            else:
                rep["general"] = f"{gen_package}.{gen_name}"
            rep["dependencies"].add(general)

        import json
        import keyword

        if any(keyword.iskeyword(k) for k in rep["attributes"].keys()):
            dict_json = json.dumps(rep["attributes"], indent=2)
            code = f"{name} = TypedDict('{name}', {dict_json}, total=False)"
            rep["code"] = code
        else:
            rep["code"] = "\n    ".join(
                [
                    f"class {name}({rep['general']}):",
                    *(f"{k}: {v}" for k, v in rep["attributes"].items()),
                ]
            )

        if rep["code"].endswith(":"):
            rep["code"] += " ..."

        return rep

    def process_entry(self, entry: Description) -> Specification:
        if is_class(entry):
            return self.process_class(entry)
        if is_enum(entry):
            return self.process_enum(entry)
        if is_primitive(entry):
            return self.process_primitive(entry)
        raise ValueError(f"Unsupported {entry['@xmi:type']}")

    def find_by_name(self, name: str) -> None | Description:
        for packages in self.packages.values():
            for entry in packages.values():  # Description
                if entry["@name"].startswith(name):
                    print(entry["@xmi:id"])
        return None

    def find_entry(self, identifier: str) -> Description:
        index = ".".join(identifier[3:].split(".")[:-1])
        return self.packages[index][identifier]  # type: ignore

    def find_and_process(self, identifier: str) -> Specification:
        entry = self.find_entry(identifier)
        return self.process_entry(entry)


datamodel = Package.from_file()

# %%


def process(*identifiers: str) -> list[Specification]:
    processed: set[str] = set()
    ordered: list[Specification] = list()

    def rec_process(id: str) -> None:
        if id in processed:
            return
        elt = datamodel.find_and_process(id)
        for dep in elt["dependencies"]:
            rec_process(dep)
        processed.add(id)
        ordered.append(elt)

    for id_ in identifiers:
        rec_process(id_)

    return ordered


# %%
items = process(
    "ID_eurocontrol.cfmu.cua.b2b.airspace.CompleteAIXMDatasetRequest",
    "ID_eurocontrol.cfmu.cua.b2b.airspace.CompleteAIXMDatasetReply",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightListByAerodromeRequest",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightListByAerodromeReply",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightListByAirspaceRequest",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightListByAirspaceReply",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightListByMeasureRequest",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightListByMeasureReply",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightPlanListRequest",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightPlanListReply",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightRetrievalRequest",
    "ID_eurocontrol.cfmu.cua.b2b.flight.FlightRetrievalReply",
    "ID_eurocontrol.cfmu.cua.b2b.flow.RegulationListRequest",
    "ID_eurocontrol.cfmu.cua.b2b.flow.RegulationListReply",
)

# %%
import functools
from itertools import groupby
from operator import iadd, itemgetter

output = Path(".") / "src" / "pyb2b" / "types" / "generated"
output.mkdir(parents=True, exist_ok=True)
(output / "__init__.py").write_text("")

for package, elts in groupby(
    sorted(items, key=itemgetter("package")),
    key=itemgetter("package"),
):
    file_ = output / f"{package}.py"
    content = "from typing import Literal, TypedDict, Union\n"
    elts_list = list(elts)
    list_dep_pkg: list[str] = functools.reduce(
        iadd,
        (
            (
                list(k.split(".")[-2] for k in elt["dependencies"])
                for elt in elts_list
            )
        ),
        [],
    )
    for package in set(list_dep_pkg) - {package}:
        content += f"from . import {package}\n"

    content += "\n\n"

    for elt in elts_list:
        content += elt["code"] + "\n\n"

    file_.write_text(content)

# %%
