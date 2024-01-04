from typing import TypedDict

import httpx

import pandas as pd

from ....mixins import DataFrameMixin, JSONMixin
from ....types.generated.flight import (
    FlightField,
    FlightListByMeasureMode,
    FlightListByMeasureReply,
    FlightListByMeasureRequest,
)
from ....types.generated.flow import MeasureId, RegulationId, ReroutingId

Request = TypedDict(
    "Request", {"fl:FlightListByMeasureRequest": FlightListByMeasureRequest}
)
Reply = TypedDict(
    "Reply", {"fl:FlightListByMeasureReply": FlightListByMeasureReply}
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


class FlightListByMeasure(DataFrameMixin, JSONMixin[FlightListByMeasureReply]):
    ...


class _FlightListByMeasure:
    def flightlistbymeasure(
        self,
        regulation: None | RegulationId = None,
        rerouting: None | ReroutingId = None,
        mode: FlightListByMeasureMode = "CONCERNED_BY_MEASURE",
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: list[FlightField] = default_fields,
    ) -> FlightListByMeasure:
        """Returns requested information about flights matching a criterion.

        :param measure: the identifier of a measure
        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later
        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.

        **Example usage:**

        .. jupyter-execute::

            # Get all flights in Bordeaux ACC
            b2b.flightlistbyairspace(airspace="LFBBBDX")

        """
        request = self._flightlistbymeasure_request(
            regulation,
            rerouting,
            mode,
            start,
            stop,
            include_proposal,
            include_forecast,
            fields,
        )
        reply = self.post(request)  # type: ignore
        return FlightListByMeasure(reply["fl:FlightListByMeasureReply"])

    async def async_flightlistbymeasure(
        self,
        client: httpx.AsyncClient,
        regulation: None | RegulationId = None,
        rerouting: None | ReroutingId = None,
        mode: FlightListByMeasureMode = "CONCERNED_BY_MEASURE",
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: list[FlightField] = default_fields,
    ) -> FlightListByMeasure:
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
        request = self._flightlistbymeasure_request(
            regulation,
            rerouting,
            mode,
            start,
            stop,
            include_proposal,
            include_forecast,
            fields,
        )
        reply = await self.async_post(client, request)  # type: ignore
        return FlightListByMeasure(reply["fl:FlightListByMeasureReply"])

    def _flightlistbymeasure_request(
        self,
        regulation: None | RegulationId,
        rerouting: None | ReroutingId,
        mode: FlightListByMeasureMode,
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

        msg = "One of regulation and rerouting must be defined"
        if regulation is None and rerouting is None:
            raise AttributeError(msg)

        measure: MeasureId
        if regulation is not None:
            if rerouting is not None:
                raise AttributeError(msg)
            measure = {"REGULATION": regulation}
        elif rerouting is not None:
            measure = {"REROUTING": rerouting}
        else:
            raise ValueError("regulation or rerouting must be set.")

        # Many fields specified as necessary but cause errors 🤷‍♂️
        request: FlightListByMeasureRequest = {  # type: ignore
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
            "measure": measure,
            "mode": mode,
        }
        return {
            "fl:FlightListByMeasureRequest": {  # type: ignore
                "@xmlns:fl": "eurocontrol/cfmu/b2b/FlightServices",
                **request,
            }
        }
