from typing import TypedDict

import httpx

import pandas as pd

from ....mixins import DataFrameMixin, JSONMixin
from ....types.generated.airspace import AirspaceId
from ....types.generated.flight import (
    FlightField,
    FlightListByAirspaceReply,
    FlightListByAirspaceRequest,
)

Request = TypedDict(
    "Request", {"fl:FlightListByAirspaceRequest": FlightListByAirspaceRequest}
)
Reply = TypedDict(
    "Reply", {"fl:FlightListByAirspaceReply": FlightListByAirspaceReply}
)

default_fields: list[FlightField] = [
    "actualOffBlockTime",
    "actualTakeOffTime",
    "actualTimeOfArrival",
    "aircraftAddress",
    "aircraftType",
    "atfcmMeasureLocations",
    "calculatedTakeOffTime",
    "calculatedTimeOfArrival",
    "divertedAerodromeOfDestination",
    "estimatedTakeOffTime",
    "estimatedTimeOfArrival",
    "mostPenalisingRegulation",
    "requestedFlightLevel",
    "wakeTurbulenceCategory",
]


class FlightListByAirspace(
    DataFrameMixin, JSONMixin[FlightListByAirspaceReply]
):
    ...


class _FlightListByAirspace:
    def flightlistbyairspace(
        self,
        airspace: AirspaceId,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: list[FlightField] = default_fields,
    ) -> FlightListByAirspace:
        """Returns requested information about flights matching a criterion.

        :param airspace: the identifier of an airspace
        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later
        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.

        **Example usage:**

        .. jupyter-execute::

            # Get all flights in Bordeaux ACC
            b2b.flightlistbyairspace(airspace="LFBBBDX")

        """
        request = self._flightlistbyairspace_request(
            airspace,
            start,
            stop,
            include_proposal,
            include_forecast,
            fields,
        )
        reply = self.post(request)  # type: ignore
        return FlightListByAirspace(reply["fl:FlightListByAirspaceReply"])

    async def async_flightlistbyairspace(
        self,
        client: httpx.AsyncClient,
        airspace: AirspaceId,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: list[FlightField] = default_fields,
    ) -> FlightListByAirspace:
        """Returns requested information about flights matching a criterion.

        :param airspace: the identifier of an airspace
        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later
        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.

        **Example usage:**

        .. jupyter-execute::

            # Get all flights scheduled out of Paris CDG
            b2b.flight_list(aerodrome="LFPG")

        """
        request = self._flightlistbyairspace_request(
            airspace,
            start,
            stop,
            include_proposal,
            include_forecast,
            fields,
        )
        reply = await self.async_post(client, request)  # type: ignore
        return FlightListByAirspace(reply["fl:FlightListByAirspaceReply"])

    def _flightlistbyairspace_request(
        self,
        airspace: AirspaceId,
        start: None | str | pd.Timestamp,
        stop: None | str | pd.Timestamp,
        include_proposal: bool,
        include_forecast: bool,
        fields: list[FlightField],
    ) -> Request:
        now = pd.Timestamp("now", tz="utc")
        if start is not None:
            start = pd.Timestamp(start, tz="utc")

        if stop is not None:
            stop = pd.Timestamp(stop, tz="utc")
        else:
            stop = start + pd.Timedelta("1H")

        # Many fields specified as necessary but cause errors 🤷‍♂️
        request: FlightListByAirspaceRequest = {  # type: ignore
            "sendTime": f"{now:%Y-%m-%d %H:%M:%S}",
            "dataset": {"type": "OPERATIONAL"},
            "includeProposalFlights": "true" if include_proposal else "false",
            "includeForecastFlights": "true" if include_forecast else "false",
            "trafficType": "DEMAND",
            "trafficWindow": {
                "wef": f"{start:%Y-%m-%d %H:%M}",
                "unt": f"{stop:%Y-%m-%d %H:%M}",
            },
            "requestedFlightFields": fields,
            "countsInterval": {"duration": "0001", "step": "0001"},
            #  "worstLoadStateAtReferenceLocationType": "ENTRY",
            #  "compareWithOtherTrafficType": "LOAD",
            "calculationType": "ENTRY",
            "airspace": airspace,
        }
        return {
            "fl:FlightListByAirspaceRequest": {  # type: ignore
                "@xmlns:fl": "eurocontrol/cfmu/b2b/FlightServices",
                **request,
            }
        }
