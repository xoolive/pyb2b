from typing import Literal, TypedDict, Union

DateTimeSecond = str

AirNavigationUnitId = str


class Request(TypedDict, total=False):
    endUserId: str
    onBehalfOfUnit: AirNavigationUnitId
    sendTime: DateTimeSecond


DateYearMonthDay = str


class DateYearMonthDayPeriod(TypedDict, total=False):
    wef: DateYearMonthDay
    unt: DateYearMonthDay


FileId = str

FileType = str


class File(TypedDict, total=False):
    id: FileId
    type: FileType
    releaseTime: DateTimeSecond
    fileLength: str


ServiceGroup = Literal[
    "COMMON", "GENERAL_INFORMATION", "AIRSPACE", "FLOW", "FLIGHT", "FFICE"
]


class Error(TypedDict, total=False):
    attributes: str
    group: ServiceGroup
    category: str
    type: str
    parameters: str
    message: str


ReplyStatus = Literal[
    "OK",
    "INVALID_INPUT",
    "INVALID_OUTPUT",
    "INTERNAL_ERROR",
    "SERVICE_UNAVAILABLE",
    "RESOURCE_OVERLOAD",
    "REQUEST_COUNT_QUOTA_EXCEEDED",
    "PARALLEL_REQUEST_COUNT_QUOTA_EXCEEDED",
    "REQUEST_OVERBOOKING_REJECTED",
    "BANDWIDTH_QUOTAS_EXCEEDED",
    "NOT_AUTHORISED",
    "OBJECT_NOT_FOUND",
    "TOO_MANY_RESULTS",
    "OBJECT_EXISTS",
    "OBJECT_OUTDATED",
    "CONFLICTING_UPDATE",
    "INVALID_DATASET",
]


class Reply(TypedDict, total=False):
    requestReceptionTime: DateTimeSecond
    requestId: str
    sendTime: DateTimeSecond
    status: ReplyStatus
    inputValidationErrors: Union[Error, list[Error]]
    outputValidationErrors: Union[Error, list[Error]]
    warnings: Union[Error, list[Error]]
    slaError: Error
    reason: str


DurationHourMinute = str

SimulationState = Literal["INITIAL", "CURRENT"]

DatasetType = Literal["FORECAST", "OPERATIONAL", "SIMULATION"]

SimulationId = str

SimulationType = Literal[
    "STANDALONE_SIMEX", "NMOC_MANAGED_SIMULATION", "USER_MANAGED_SIMULATION"
]


class SimulationIdentifier(TypedDict, total=False):
    simulationType: SimulationType
    simulationId: SimulationId


class Dataset(TypedDict, total=False):
    type: DatasetType
    simulationIdentifier: SimulationIdentifier
    simulationState: SimulationState


DateTimeMinute = str


class DateTimeMinutePeriod(TypedDict, total=False):
    wef: DateTimeMinute
    unt: DateTimeMinute


DistanceNM = str

TimeHourMinute = str


class TimeHourMinutePeriod(TypedDict, total=False):
    wef: TimeHourMinute
    unt: TimeHourMinute


ReceivedOrSent = Literal["RECEIVED", "SENT", "UNKNOWN"]

SignedDurationHourMinuteSecond = str

Cost = str

DurationHourMinuteSecond = str

DistanceM = str

LatitudeSide = Literal["NORTH", "SOUTH"]


class Latitude(TypedDict, total=False):
    angle: str
    side: LatitudeSide


LongitudeSide = Literal["EAST", "WEST"]


class Longitude(TypedDict, total=False):
    angle: str
    side: LongitudeSide


class Position(TypedDict, total=False):
    latitude: Latitude
    longitude: Longitude


DurationMinute = str

Sign = Literal["PLUS", "MINUS"]


class ShiftHourMinute(TypedDict, total=False):
    sign: Sign
    value: DurationHourMinute


Colours = str

FlightLevelM = str

Duration = str

WeightKg = str
