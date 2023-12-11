from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Literal, TypedDict
from xml.dom import minidom
from xml.etree import ElementTree

import httpx
import xmltodict

from .auth.pkcs12 import create_ssl_context
from .services.airspace.structure.aixm_dataset import AIXMDataset
from .services.flight.management.flightplanlist import FlightPlanList
from .services.flow.measures.regulationlist import RegulationList
from .types.common import InvalidInput


class OperationMode(TypedDict):
    base_url: str
    post_url: str
    file_url: str


class B2B(AIXMDataset, FlightPlanList, RegulationList):
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

    def post(self, data: dict[str, Any]) -> dict[str, Any]:
        res = httpx.post(
            url=self.mode["post_url"] + self.version,
            data=xmltodict.unparse(data).encode(),
            headers={"Content-Type": "application/xml"},
            verify=self.context,
        )
        res.raise_for_status()
        tree = ElementTree.fromstring(res.content)

        if tree is None:
            raise RuntimeError("Unexpected error")

        if tree.find("status").text != "OK":  # type: ignore
            rough_string = ElementTree.tostring(tree)
            reparsed = minidom.parseString(rough_string)
            raise RuntimeError(reparsed.toprettyxml(indent="  "))

        return xmltodict.parse(res.content)

    async def async_post(
        self,
        client: httpx.AsyncClient,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        request = httpx.Request(
            "POST",
            url=self.mode["post_url"] + self.version,
            data=xmltodict.unparse(data).encode(),
            headers={"Content-Type": "application/xml"},
        )
        res = await client.send(request)
        res.raise_for_status()
        tree = ElementTree.fromstring(res.content)

        if tree is None:
            raise RuntimeError("Unexpected error")

        if tree.find("status").text == "INVALID_INPUT":  # type: ignore
            errors = tree.find("inputValidationErrors")
            if errors is not None:
                rough_string = ElementTree.tostring(errors)
                errors_dict: InvalidInput = xmltodict.parse(rough_string)
                invalid = errors_dict["inputValidationErrors"]
                _type = invalid["type"]
                error_msg = invalid["parameters"]["item"]["value"]
                raise AttributeError(error_msg)
        if tree.find("status").text != "OK":  # type: ignore
            rough_string = ElementTree.tostring(tree)
            reparsed = minidom.parseString(rough_string)
            raise RuntimeError(reparsed.toprettyxml(indent="  "))

        return xmltodict.parse(res.content)
