from typing import Literal, TypedDict, Union

from ...common import Status, TimeRequest


class FlightPlanKeys(TypedDict):
    aircraftId: str
    aerodromeOfDeparture: str
    nonICAOAerodromeOfDeparture: Literal["true", "false"]
    airFiled: Literal["true", "false"]
    aerodromeOfDestination: str
    nonICAOAerodromeOfDestination: Literal["true", "false"]
    estimatedOffBlockTime: str


class InvalidFlightPlan(TypedDict):
    filingTime: str
    invalidMessageType: Literal["CHG", "DLA", "CNL", "FPL"]
    invalidMessageStatus: Literal["REJECTED"]
    keys: FlightPlanKeys


class FlightPlanID(TypedDict):
    id: str
    keys: FlightPlanKeys


class LastValidFlightPlan(TypedDict):
    id: FlightPlanID
    status: Literal["AIRBORNE", "BACKUP", "CLOSED", "SUSPENDED", "TERMINATED"]


class _Entry(TypedDict, total=False):
    currentInvalid: InvalidFlightPlan
    lastValidFlightPlan: LastValidFlightPlan


class _Data(TypedDict):
    summaries: list[_Entry]


class _FlightPlanListReply(TypedDict):
    requestReceptionTime: str
    requestID: str
    sendTime: str
    status: Status
    data: _Data


FlightPlanListReply = TypedDict(
    "FlightPlanListReply",
    {"fl:FlightPlanListReply": _FlightPlanListReply},
)


class _FlightPlanListRequest(TypedDict):
    sendTime: str
    aircraftId: str
    aerodromeOfDeparture: str
    nonICAOAerodromeOfDeparture: Literal["true", "false"]
    airFiled: Literal["true", "false"]
    aerodromeOfDestination: str
    nonICAOAerodromeOfDestination: Literal["true", "false"]
    estimatedOffBlockTime: Union[str, TimeRequest]


FlightPlanListRequest = TypedDict(
    "FlightPlanListRequest",
    {"fl:FlightPlanListRequest": _FlightPlanListRequest},
)
