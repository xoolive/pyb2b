from __future__ import annotations

from typing import Any, Optional, Set, Type, TypeVar
from xml.etree import ElementTree

import pandas as pd
from pyb2b.mixins import DataFrameMixin, JSONMixin
from pyb2b.types.generated.common import Request
from pyb2b.types.generated.flow import (
    RegulationListReply,
    RegulationListRequest,
)
                                        RegulationListRequest)

rename_cols = {"id": "tvId", "regulationState": "state", "subType": "type"}

default_regulation_fields: Set[str] = {
    "applicability",
    # "autolink",
    # "measureCherryPicked",
    # "initialConstraints",
    # "linkedRegulations",
    "location",
    "protectedLocation",
    "reason",
    # "remark",
    "regulationState",
    # "supplementaryConstraints",
    # "lastUpdate",
    # "noDelayWindow",
    # "updateCapacityRequired",
    # "updateTVActivationRequired",
    # "externallyEditable",
    "subType",
    # "delayTVSet",
    # "createdByFMP",
    # "sourceHotspot",
    # "mcdmRequired",
    # "dataId",
    # "scenarioReference",
    # "delayConfirmationThreshold",
}

# https://github.com/python/mypy/issues/2511
RegulationListTypeVar = TypeVar("RegulationListTypeVar", bound="RegulationList")


class RegulationInfo:
    @property
    def regulation_id(self) -> str:
        assert self.reply is not None
        elt = self.reply.find("regulationId")
        assert elt is not None
        assert elt.text is not None
        return elt.text

    @property
    def state(self) -> str:
        assert self.reply is not None
        elt = self.reply.find("regulationState")
        assert elt is not None
        assert elt.text is not None
        return elt.text

    @property
    def type(self) -> str:
        assert self.reply is not None
        elt = self.reply.find("subType")
        assert elt is not None
        assert elt.text is not None
        return elt.text

    @property
    def start(self) -> pd.Timestamp:
        assert self.reply is not None
        elt = self.reply.find("applicability/wef")
        assert elt is not None
        assert elt.text is not None
        return pd.Timestamp(elt.text, tz="UTC")

    @property
    def stop(self) -> pd.Timestamp:
        assert self.reply is not None
        elt = self.reply.find("applicability/unt")
        assert elt is not None
        assert elt.text is not None
        return pd.Timestamp(elt.text, tz="UTC")

    @property
    def tvId(self) -> str:
        assert self.reply is not None
        elt = self.reply.find("location/id")
        assert elt is not None
        assert elt.text is not None
        return elt.text

    @property
    def location(self) -> Optional[str]:
        assert self.reply is not None
        elt = self.reply.find(
            "location/referenceLocation-ReferenceLocationAirspace/id"
        )
        if elt is not None:
            return elt.text
        elt = self.reply.find(
            "location/referenceLocation-ReferenceLocationAerodrome/id"
        )
        if elt is not None:
            return elt.text
        return None

    @property
    def fl_min(self) -> int:
        assert self.reply is not None
        elt = self.reply.find("location/flightLevels/min/level")
        return int(elt.text) if elt is not None and elt.text is not None else 0

    @property
    def fl_max(self) -> int:
        assert self.reply is not None
        elt = self.reply.find("location/flightLevels/max/level")
        return (
            int(elt.text) if elt is not None and elt.text is not None else 999
        )

    def __getattr__(self, name: str) -> str:
        cls = type(self)
        assert self.reply is not None
        elt = self.reply.find(name)
        if elt is not None:
            return elt.text  # type: ignore
        msg = "{.__name__!r} object has no attribute {!r}"
        raise AttributeError(msg.format(cls, name))


class RegulationList(DataFrameMixin, JSONMixin[RegulationListReply]): ...


class _RegulationList:
    def regulation_list(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        traffic_volumes: None | list[str] = None,
        regulations: None | str | list[str] = None,
        fields: None | list[str] = None,
        reasons: None | list[str] = None,
        states: None | list[str] = None,
    ) -> None | RegulationList:
        """Returns information about a (set of) given regulation(s).

        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later

        :param traffic_volumes: impacted by a given regulation
        :param regulations: identifier(s) related to a regulation


        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.
        :param reasons: regulation reasons to filter
        :param states: regulation states to filter

        **Example usage:**

        .. jupyter-execute::

            nm_b2b.regulation_list()

        """
        request = self._regulation_list_request(
            start,
            stop,
            traffic_volumes,
            regulations,
            fields,
            reasons,
            states,
        )
        reply = self.post(request)  # type: ignore
        return RegulationList(reply["fw:RegulationListReply"])

    def _regulation_list_request(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        traffic_volumes: None | list[str] = None,
        regulations: None | str | list[str] = None,
        fields: None | list[str] = None,
        reasons: None | list[str] = None,
        states: None | list[str] = None,
    ) -> Request:
        now = pd.Timestamp("now", tz="utc")
        # same as in flightlistbyaerodrome but will crash if start is None
        if start is not None:
            start = pd.Timestamp(start, tz="utc")

        if stop is not None:
            stop = pd.Timestamp(stop, tz="utc")
        else:
            stop = start + pd.Timedelta("1H")

        fields = (
            list(default_regulation_fields.union(fields))
            if fields is not None
            else list(default_regulation_fields)
        )
        _reasons = {"reasons": _itemize(reasons)} if reasons is not None else {}
        _fields = (
            {"requestedRegulationFields": _itemize(fields)}
            if fields is not None
            else {}
        )
        _states = {"regulationStates": _itemize(states)} if states is not None else {}
        _regulations = {"refulations": regulations} if regulations is not None else {}
        _traffic_volumes = (
            {"tvId": traffic_volumes} if traffic_volumes is not None else {}
        )

        request: RegulationListRequest = {  # type: ignore
            "sendTime": f"{now:%Y-%m-%d %H:%M:%S}",
            "dataset": {"type": "OPERATIONAL"},
            "queryPeriod": {
                "wef": f"{start:%Y-%m-%d %H:%M}",
                "unt": f"{stop:%Y-%m-%d %H:%M}",
            },
            **_reasons,
            **_fields,
            **_states,
            **_regulations,
            **_traffic_volumes,
        }
        return {
            "fw:RegulationListRequest": {
                "@xmlns:fw": "eurocontrol/cfmu/b2b/FlowServices",
                **request,
            }
        }


def _itemize(items: list[str]) -> dict[str, str]:
    return {"item": item for item in items}
