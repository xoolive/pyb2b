from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar, Literal, TypedDict
from xml.dom import minidom
from xml.etree import ElementTree

import httpx
import xmltodict

from .auth.pkcs12 import create_ssl_context
from .services.airspace.structure.aixm_dataset import _AIXMDataset
from .services.flight.management.flightplanlist import _FlightPlanList
from .services.flight.management.flightretrieval import _FlightRetrieval
from .services.flow.measures.regulationlist import _RegulationList
from .types.generated.common import Reply


class OperationMode(TypedDict):
    base_url: str
    post_url: str
    file_url: str


class B2B(_AIXMDataset, _FlightPlanList, _FlightRetrieval, _RegulationList):
    """
    The main instance of this class is provided as:

    .. code:: python

        from pyb2b import b2b

    A path to your certificate and your password must be set in the
    configuration file. An ImportError is raised if the information is not
    available.

    """

    base_preops = "https://www.b2b.preops.nm.eurocontrol.int/"
    base_ops = "https://www.b2b.nm.eurocontrol.int/"

    PREOPS: ClassVar[OperationMode] = {
        "base_url": base_preops,
        "post_url": base_preops + "B2B_PREOPS/gateway/spec/",
        "file_url": base_preops + "FILE_PREOPS/gateway/spec/",
    }

    OPS: ClassVar[OperationMode] = {
        "base_url": base_ops,
        "post_url": base_ops + "B2B_OPS/gateway/spec/",
        "file_url": base_ops + "FILE_OPS/gateway/spec/",
    }

    def __init__(
        self,
        mode: Literal["PREOPS", "OPS"],
        version: str,
        pkcs12_filename: str | Path,
        pkcs12_password: str,
    ) -> None:
        self.mode: OperationMode = getattr(self.__class__, mode)
        self.version = version
        self.context = create_ssl_context(
            Path(pkcs12_filename).read_bytes(),
            pkcs12_password.encode(),
        )

    def raise_xml_errors(self, res: httpx.Response) -> None:
        tree = ElementTree.fromstring(res.content)

        if tree is None:
            raise RuntimeError("Unexpected error")
        status = tree.find("status")
        assert status is not None

        if status.text == "INVALID_INPUT":
            errors = []
            for error in tree.findall("inputValidationErrors"):
                rough_string = ElementTree.tostring(error)
                errors_dict: Reply = xmltodict.parse(rough_string)
                invalid = errors_dict["inputValidationErrors"]
                if isinstance(invalid, list):
                    invalid = invalid[0]
                _type = invalid["type"]
                parameters = invalid["parameters"]
                errors.append(f"{_type} {json.dumps(parameters, indent=2)}")
            raise AttributeError("\n".join(errors))

        if status.text != "OK":
            reason = tree.find("reason")
            if reason is not None:
                raise RuntimeError(f"{status.text}: {reason.text}")

            # otherwise
            rough_string = ElementTree.tostring(tree)
            reparsed = minidom.parseString(rough_string)
            raise RuntimeError(reparsed.toprettyxml(indent="  "))

    def post(self, data: dict[str, Any]) -> Reply:
        res = httpx.post(
            url=self.mode["post_url"] + self.version,
            data=xmltodict.unparse(data).encode(),
            headers={"Content-Type": "application/xml"},
            verify=self.context,
        )
        res.raise_for_status()
        self.raise_xml_errors(res)
        return xmltodict.parse(res.content)  # type: ignore

    async def async_post(
        self,
        client: httpx.AsyncClient,
        data: dict[str, Any],
    ) -> Reply:
        request = httpx.Request(
            "POST",
            url=self.mode["post_url"] + self.version,
            data=xmltodict.unparse(data).encode(),
            headers={"Content-Type": "application/xml"},
        )
        res = await client.send(request)
        res.raise_for_status()
        self.raise_xml_errors(res)
        return xmltodict.parse(res.content)  # type: ignore
