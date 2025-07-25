from __future__ import annotations

from typing import Any, ClassVar, TypedDict

import httpx

import pandas as pd

from ....mixins import DataFrameMixin, JSONMixin
from ....types.generated.flight import (
    FlightPlanListReply,
    FlightPlanListRequest,
    FlightPlanOrInvalidFiling,
)
from .flightretrieval import FlightRetrieval

Request = TypedDict(
    "Request", {"fl:FlightPlanListRequest": FlightPlanListRequest}
)
Reply = TypedDict("Reply", {"fl:FlightPlanListReply": FlightPlanListReply})


class FlightPlanList(DataFrameMixin, JSONMixin[FlightPlanListReply]):
    columns_options: ClassVar[None | dict[str, dict[str, Any]]] = dict(
        flightId=dict(style="blue bold"),
        callsign=dict(),
        origin=dict(),
        destination=dict(),
        EOBT=dict(),
        status=dict(),
    )

    def __init__(
        self,
        json: FlightPlanListReply,
        parent: None | _FlightPlanList = None,
    ):
        self.parent = parent
        self.json = json

    @property
    def data(self) -> pd.DataFrame:
        def eobt(entry: FlightPlanOrInvalidFiling) -> str:
            if lfvp := entry.get("lastValidFlightPlan", None):
                return lfvp["id"]["keys"]["estimatedOffBlockTime"]
            return ""

        summaries = self.json["data"]["summaries"]
        if not isinstance(summaries, list):
            summaries = [summaries]
        summaries = sorted(summaries, key=eobt)
        return pd.DataFrame.from_records(
            {
                "flightId": lvfp["id"]["id"],
                "callsign": lvfp["id"]["keys"]["aircraftId"],
                "origin": lvfp["id"]["keys"]["aerodromeOfDeparture"],
                "destination": lvfp["id"]["keys"]["aerodromeOfDestination"],
                "EOBT": pd.Timestamp(eobt_str, tz="utc")
                if (eobt_str := eobt(entry))
                else pd.Timestamp("NaT"),
                "status": lvfp["status"],
            }
            for entry in summaries
            if (lvfp := entry.get("lastValidFlightPlan", None))
        )

    def __getitem__(self, item: str) -> None | FlightRetrieval:
        handle = next(
            (df for _, df in self.data.iterrows() if df.flightId == item), None
        )
        if handle is None:
            return None
        return self.parent.flightretrieval(  # type: ignore
            EOBT=handle.EOBT,
            callsign=handle.callsign,
            origin=handle.origin,
            destination=handle.destination,
        )


class _FlightPlanList:
    def flightplanlist(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *,
        callsign: None | str = None,
        origin: None | str = None,
        destination: None | str = None,
    ) -> FlightPlanList:
        """Returns a **minimum set of information** about flights.

        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later

        The method must take at least one of:

        :param callsign: (wildcard accepted)
        :param origin: flying from a given airport (ICAO 4 letter code).
        :param destination: flying to a given airport (ICAO 4 letter code).

        **Example usage:**

        .. jupyter-execute::

            # All KLM flights bound for Amsterdam Schiphol
            b2b.flight_search(destination="EHAM", callsign="KLM*")

        """
        request = self._flightplanlist_request(
            start=start,
            stop=stop,
            callsign=callsign,
            origin=origin,
            destination=destination,
        )
        reply: Reply = self.post(request)  # type: ignore
        return FlightPlanList(reply["fl:FlightPlanListReply"], parent=self)

    async def async_flightplanlist(
        self,
        client: httpx.AsyncClient,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *,
        callsign: None | str = None,
        origin: None | str = None,
        destination: None | str = None,
    ) -> FlightPlanList:
        """Returns a **minimum set of information** about flights.

        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later

        The method must take at least one of:

        :param callsign: (wildcard accepted)
        :param origin: flying from a given airport (ICAO 4 letter code).
        :param destination: flying to a given airport (ICAO 4 letter code).

        **Example usage:**

        .. jupyter-execute::

            # All KLM flights bound for Amsterdam Schiphol
            b2b.flight_search(destination="EHAM", callsign="KLM*")

        """
        request = self._flightplanlist_request(
            start=start,
            stop=stop,
            callsign=callsign,
            origin=origin,
            destination=destination,
        )
        reply: Reply = await self.async_post(client, request)  # type: ignore
        return FlightPlanList(reply["fl:FlightPlanListReply"], parent=self)

    def _flightplanlist_request(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *,
        callsign: None | str = None,
        origin: None | str = None,
        destination: None | str = None,
    ) -> Request:
        if start is not None:
            start = pd.Timestamp(start, tz="utc")

        if stop is not None:
            stop = pd.Timestamp(stop, tz="utc")
        else:
            stop = start + pd.Timedelta("1h")
        now = pd.Timestamp("now", tz="utc")
        request: FlightPlanListRequest = {
            "sendTime": f"{now:%Y-%m-%d %H:%M:%S}",
            "aircraftId": callsign if callsign is not None else "*",
            "aerodromeOfDeparture": origin if origin is not None else "*",
            "nonICAOAerodromeOfDeparture": "false",
            "airFiled": "false",
            "aerodromeOfDestination": destination
            if destination is not None
            else "*",
            "nonICAOAerodromeOfDestination": "false",
            "estimatedOffBlockTime": {
                "wef": f"{start:%Y-%m-%d %H:%M}",
                "unt": f"{stop:%Y-%m-%d %H:%M}",
            },
        }

        return {
            "fl:FlightPlanListRequest": {  # type: ignore
                "@xmlns:fl": "eurocontrol/cfmu/b2b/FlightServices",
                **request,
            }
        }
