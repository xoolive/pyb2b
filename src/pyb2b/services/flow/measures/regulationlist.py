from __future__ import annotations

from typing import Any, ClassVar, TypedDict, cast

import httpx

import pandas as pd

from ....mixins import DataFrameMixin, JSONMixin
from ....types.generated.flow import (
    Regulation,
    RegulationField,
    RegulationListReply,
    RegulationListRequest,
    RegulationReason,
    RegulationState,
)

Request = TypedDict(
    "Request", {"fw:RegulationListRequest": RegulationListRequest}
)
Reply = TypedDict("Reply", {"fw:RegulationListReply": RegulationListReply})

default_fields: list[RegulationField] = list(
    field
    for field in RegulationField.__args__  # type: ignore
    if field not in []
)


class RegulationList(DataFrameMixin, JSONMixin[RegulationListReply]):
    """
    A list of regulations.
    """

    columns_options: ClassVar[None | dict[str, dict[str, Any]]] = dict(
        regulationId=dict(style="blue bold"),
        title=dict(),
        status=dict(),
        startDate=dict(),
        endDate=dict(),
    )

    def __init__(
        self,
        json: RegulationListReply,
        parent: None | _RegulationList = None,
    ):
        self.parent = parent
        self.json = json

    @property
    def data(self) -> pd.DataFrame:
        item = self.json["data"]["regulations"]["item"]  # type: ignore
        if not isinstance(item, list):
            item = [item]
        return pd.DataFrame.from_records(
            {
                "regulation": e["regulationId"],
                "from": pd.Timestamp(e["applicability"]["wef"], tz="utc"),
                "until": pd.Timestamp(e["applicability"]["unt"], tz="utc"),
                "update": pd.Timestamp(e["lastUpdate"]["eventTime"], tz="utc"),
                "reason": e.get("reason", ""),
                "type": e.get("subType", ""),
                "location": e["location"]["id"],
                "tv": e.get("delayTVSet", ""),
                "state": e["regulationState"],
            }
            for entry in item
            if (e := cast(Regulation, entry))
        )


class _RegulationList:
    def regulationlist(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *,
        traffic_volumes: None | list[str] = None,
        regulations: None | str | list[str] = None,
        reasons: None | RegulationReason | list[RegulationReason] = None,
        states: None | RegulationState | list[RegulationState] = None,
    ) -> RegulationList:
        request = self._regulationlist_request(
            start=start,
            stop=stop,
            traffic_volumes=traffic_volumes,
            regulations=regulations,
            reasons=reasons,
            states=states,
        )
        reply: Reply = self.post(request)  # type: ignore
        return RegulationList(reply["fw:RegulationListReply"], parent=self)

    async def async_regulationlist(
        self,
        client: httpx.AsyncClient,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *,
        traffic_volumes: None | list[str] = None,
        regulations: None | str | list[str] = None,
        reasons: None | RegulationReason | list[RegulationReason] = None,
        states: None | RegulationState | list[RegulationState] = None,
    ) -> RegulationList:
        request = self._regulationlist_request(
            start=start,
            stop=stop,
            traffic_volumes=traffic_volumes,
            regulations=regulations,
            reasons=reasons,
            states=states,
        )
        reply: Reply = await self.async_post(client, request)  # type: ignore
        return RegulationList(reply["fw:RegulationListReply"], parent=self)

    def _regulationlist_request(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *,
        traffic_volumes: None | list[str] = None,
        regulations: None | str | list[str] = None,
        reasons: None | RegulationReason | list[RegulationReason] = None,
        states: None | RegulationState | list[RegulationState] = None,
    ) -> Request:
        if start is None:
            start = pd.Timestamp.now(tz="utc")
        elif isinstance(start, str):
            start = pd.Timestamp(start, tz="utc")

        if stop is not None:
            stop = pd.Timestamp(stop, tz="utc")
        else:
            stop = start + pd.Timedelta("1h")

        now = pd.Timestamp.now(tz="utc")
        request: RegulationListRequest = {
            "sendTime": f"{now:%Y-%m-%d %H:%M:%S}",
            "dataset": {"type": "OPERATIONAL"},
            "queryPeriod": {
                "wef": f"{start:%Y-%m-%d %H:%M}",
                "unt": f"{stop:%Y-%m-%d %H:%M}",
            },
            "reasons": {"item": reasons} if reasons else [],  # type: ignore
            "regulations": {"item": regulations} if regulations else [],  # type: ignore
            "tvs": {"item": traffic_volumes} if traffic_volumes else [],  # type: ignore
            "tvSets": [],
            "requestedRegulationFields": {"item": default_fields},  # type: ignore
            "regulationStates": {"item": states} if states else [],  # type: ignore
        }

        return {
            "fw:RegulationListRequest": {  # type: ignore
                "@xmlns:fw": "eurocontrol/cfmu/b2b/FlowServices",
                **request,
            }
        }
