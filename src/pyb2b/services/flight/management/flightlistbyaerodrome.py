from typing import TypedDict

import httpx

import pandas as pd

from ....mixins import DataFrameMixin, JSONMixin
from ....types.generated.airspace import AerodromeICAOId
from ....types.generated.flight import (
    AerodromeRole,
    FlightField,
    FlightListByAerodromeReply,
    FlightListByAerodromeRequest,
)

Request = TypedDict(
    "Request", {"fl:FlightListByAerodromeRequest": FlightListByAerodromeRequest}
)
Reply = TypedDict(
    "Reply", {"fl:FlightListByAerodromeReply": FlightListByAerodromeReply}
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


class FlightList(DataFrameMixin, JSONMixin[FlightListByAerodromeReply]):
    ...


class _FlightListByAerodrome:
    def flightlistbyaerodrome(
        self,
        aerodrome: AerodromeICAOId,
        aerodrome_role: AerodromeRole = "GLOBAL",
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: list[FlightField] = default_fields,
    ) -> FlightList:
        """Returns requested information about flights matching a criterion.

        :param aerodrome: flying from or to a given airport (ICAO code)
        :param aerodrome_role: DEPARTURE, ARRIVAL, GLOBAL or ALTERNATE
        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later
        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.

        **Example usage:**

        .. jupyter-execute::

            # Get all flights scheduled out of Paris CDG
            b2b.flightlistbyaerodrome(aerodrome="LFPG")

        """
        request = self._flightlistbyaerodrome_request(
            aerodrome,
            aerodrome_role,
            start,
            stop,
            include_proposal,
            include_forecast,
            fields,
        )
        reply = self.post(request)  # type: ignore
        return FlightList(reply["fl:FlightListByAerodromeReply"])

    async def async_flightlistbyaerodrome(
        self,
        client: httpx.AsyncClient,
        aerodrome: AerodromeICAOId,
        aerodrome_role: AerodromeRole = "GLOBAL",
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: list[FlightField] = default_fields,
    ) -> FlightList:
        """Returns requested information about flights matching a criterion.

        :param aerodrome: flying from or to a given airport (ICAO code)
        :param aerodrome_role:
        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later
        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.

        **Example usage:**

        .. jupyter-execute::

            # Get all flights scheduled out of Paris CDG
            b2b.flight_list(aerodrome="LFPG")

        """
        request = self._flightlistbyaerodrome_request(
            aerodrome,
            aerodrome_role,
            start,
            stop,
            include_proposal,
            include_forecast,
            fields,
        )
        reply = await self.async_post(client, request)  # type: ignore
        return FlightList(reply["fl:FlightListByAerodromeReply"])

    def _flightlistbyaerodrome_request(
        self,
        aerodrome: AerodromeICAOId,
        aerodrome_role: AerodromeRole,
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
        request: FlightListByAerodromeRequest = {  # type: ignore
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
            "aerodrome": aerodrome,
            "aerodromeRole": aerodrome_role,
        }
        return {
            "fl:FlightListByAerodromeRequest": {  # type: ignore
                "@xmlns:fl": "eurocontrol/cfmu/b2b/FlightServices",
                **request,
            }
        }
