from typing import TypedDict

import httpx

import pandas as pd

from ....mixins import JSONMixin
from ....types.generated.flight import (
    FlightField,
    FlightRetrievalReply,
    FlightRetrievalRequest,
)

Request = TypedDict(
    "Request", {"fl:FlightRetrievalRequest": FlightRetrievalRequest}
)
Reply = TypedDict("Reply", {"fl:FlightRetrievalReply": FlightRetrievalReply})


class FlightRetrieval(JSONMixin[FlightRetrievalReply]):
    @property
    def callsign(self) -> str:
        return self.json["data"]["flight"]["flightId"]["keys"]["aircraftId"]

    @property
    def origin(self) -> str:
        return self.json["data"]["flight"]["flightId"]["keys"][
            "aerodromeOfDeparture"
        ]

    @property
    def destination(self) -> str:
        return self.json["data"]["flight"]["flightId"]["keys"][
            "aerodromeOfDestination"
        ]

    @property
    def icaoRoute(self) -> str:
        return self.json["data"]["flight"]["icaoRoute"]

    def time_indicators(self) -> pd.DataFrame:
        flight = self.json["data"]["flight"]
        return (
            pd.DataFrame.from_dict(
                {
                    "key": [
                        "EOBT",
                        "ETOT",
                        "ETOA",
                        "COBT",
                        "CTOT",
                        "CTOA",
                        "AOBT",
                        "ATOT",
                        "ATOA",
                    ],
                    "value": [
                        flight["flightId"]["keys"]["estimatedOffBlockTime"],
                        flight.get("estimatedTakeOffTime", None),
                        flight.get("estimatedTimeOfArrival", None),
                        flight.get("calculatedOffBlockTime", None),
                        flight.get("calculatedTakeOffTime", None),
                        flight.get("calculatedTimeOfArrival", None),
                        flight.get("actualOffBlockTime", None),
                        flight.get("actualTakeOffTime", None),
                        flight.get("actualTimeOfArrival", None),
                    ],
                }
            )
            .dropna()
            .eval("value = @pd.to_datetime(value, utc=True)")
        )


default_fields: list[FlightField] = list(
    field
    for field in FlightField.__args__  # type: ignore
    if field
    not in [
        # NM 27.0.0 - not a valid value of union type 'FlightField'
        "highestModelTrafficVolumeProfile",
        "highestModelRouteChargeIndicator",
        "highestModelFuelConsumptionIndicator",
        # INVALID_ATTRIBUTE_VALUE:
        # Flight field is not supported by FlightRetrieval
        "worstLoadStateAtReferenceLocation",
        "compareWithOtherTrafficType",
        "slotSwapCandidateList",
        # SERVICE_UNAVAILABLE: read access
        # to resource '/operational/hotspots?kind=PROBLEM' is disabled
        "caughtInHotspots",
        "hotspots",
    ]
)


class _FlightRetrieval:
    def flightretrieval(
        self,
        EOBT: str | pd.Timestamp,
        callsign: str,
        origin: str,
        destination: str,
    ) -> FlightRetrieval:
        """Returns full information about a given flight.

        This method requires all parameters:

        :param EOBT: Estimated off-block time
        :param callsign: **NO** wildcard accepted
        :param origin: flying from a given airport (ICAO 4 letter code).
        :param destination: flying to a given airport (ICAO 4 letter code).
        """

        request = self._flightretrieval_request(
            EOBT=EOBT,
            callsign=callsign,
            origin=origin,
            destination=destination,
        )
        reply = self.post(request)  # type: ignore
        return FlightRetrieval(reply["fl:FlightRetrievalReply"])

    async def async_flightretrieval(
        self,
        client: httpx.AsyncClient,
        EOBT: str | pd.Timestamp,
        callsign: str,
        origin: str,
        destination: str,
    ) -> FlightRetrieval:
        """Returns full information about a given flight.

        This method requires all parameters:

        :param EOBT: Estimated off-block time
        :param callsign: **NO** wildcard accepted
        :param origin: flying from a given airport (ICAO 4 letter code).
        :param destination: flying to a given airport (ICAO 4 letter code).
        """

        request = self._flightretrieval_request(
            EOBT=EOBT,
            callsign=callsign,
            origin=origin,
            destination=destination,
        )
        reply = await self.async_post(client, request)  # type: ignore
        return FlightRetrieval(reply["fl:FlightRetrievalReply"])

    def _flightretrieval_request(
        self,
        EOBT: str | pd.Timestamp,
        callsign: str,
        origin: str,
        destination: str,
    ) -> Request:
        if isinstance(EOBT, str):
            EOBT = pd.Timestamp(EOBT, tz="utc")
        now = pd.Timestamp("now", tz="utc")

        request: FlightRetrievalRequest = {
            "sendTime": f"{now:%Y-%m-%d %H:%M:%S}",
            "dataset": {"type": "OPERATIONAL"},
            "includeProposalFlights": "false",
            "flightId": {
                "keys": {
                    "aircraftId": f"{callsign}",
                    "aerodromeOfDeparture": f"{origin}",
                    "nonICAOAerodromeOfDeparture": "false",
                    "airFiled": "false",
                    "aerodromeOfDestination": f"{destination}",
                    "nonICAOAerodromeOfDestination": "false",
                    "estimatedOffBlockTime": f"{EOBT:%Y-%m-%d %H:%M}",
                }
            },
            "requestedFlightDatasets": "flight",
            "requestedFlightFields": default_fields,
        }
        return {
            "fl:FlightRetrievalRequest": {  # type: ignore
                "@xmlns:fl": "eurocontrol/cfmu/b2b/FlightServices",
                **request,
            }
        }
