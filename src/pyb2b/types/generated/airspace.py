from typing import Literal, TypedDict, Union
from . import common


AIRACId = str

class AiracIdentifier(TypedDict, total=False):
    airacId: AIRACId
    airacSequenceNumber: str

class CompleteDatasetQueryCriteria(TypedDict, total=False):
    airac: AiracIdentifier
    date: common.DateYearMonthDay
    publicationPeriod: common.DateYearMonthDayPeriod

class CompleteAIXMDatasetRequest(common.Request):
    queryCriteria: CompleteDatasetQueryCriteria

class AIXMFile(common.File): ...

AirspaceDataUpdateId = str

class CompleteDatasetSummary(TypedDict, total=False):
    updateId: AirspaceDataUpdateId
    publicationDate: common.DateYearMonthDay
    sourceAIRACs: Union[AiracIdentifier, list[AiracIdentifier]]
    files: Union[AIXMFile, list[AIXMFile]]

class CompleteAIXMDatasetReplyData(TypedDict, total=False):
    datasetSummaries: Union[CompleteDatasetSummary, list[CompleteDatasetSummary]]

class CompleteAIXMDatasetReply(common.Reply):
    data: CompleteAIXMDatasetReplyData

AerodromeICAOId = str

FlightLevel_DataType = str

FlightLevelUnit = Literal["F", "A", "S", "M", "SM", "MM"]

class FlightLevel(TypedDict, total=False):
    unit: FlightLevelUnit
    level: FlightLevel_DataType
    ground: Literal['true', 'false']
    ceiling: Literal['true', 'false']

AirspaceId = str

AirspaceType = Literal["REG", "FIR", "AUA", "ES", "CS", "ERSA", "CRSA", "CDA", "AUAG", "AREA", "NAS", "IFPZ", "AOI", "AOP", "CLUS", "CRAS", "ERAS"]

NetworkAddress_DataType = str

Network = Literal["AFTN", "SITA", "OTHER"]

class NetworkAddress(TypedDict, total=False):
    network: Network
    address: NetworkAddress_DataType

class NonPublishedPoint(TypedDict, total=False): ...

PublishedPointId = str

class ICAOPoint(TypedDict, total=False):
    pointId: PublishedPointId
    nonPublishedPoint: NonPublishedPoint

AerodromeIATAOrICAOId = str

RouteId = str

class TerminalProcedureIdentifier(TypedDict, total=False):
    id: RouteId
    aerodromeId: AerodromeIATAOrICAOId

class RouteOrTerminalProcedure(TypedDict, total=False):
    DCT: str
    route: RouteId
    SID: TerminalProcedureIdentifier
    STAR: TerminalProcedureIdentifier

TrafficVolumeId = str

ReferenceLocationType = Literal["AERODROME", "AERODROME_SET", "AIRSPACE", "PUBLISHED_POINT", "DBE_POINT"]

class ReferenceLocation(TypedDict, total=False):
    type: ReferenceLocationType

class TerminalProcedure(TypedDict, total=False):
    id: RouteId
    DCT: str
    pointId: PublishedPointId

SpeedUnit = Literal["UNDEFINED", "KNOTS", "KILOMETERS_PER_HOUR", "MACH_NUMBER", "FEET_PER_MINUTE"]

AirSpeed_DataType = str

class AirSpeed(TypedDict, total=False):
    speed: AirSpeed_DataType
    unit: SpeedUnit

RestrictionId = str

FlightPlanProcessing = Literal["RAD", "PROFILE_TUNING", "AERODROME_FLIGHT_RULE", "TP_AIRCRAFT_TYPE_CLASSIFICATION", "DCT_LIMIT", "SSR_CODE_ALLOCATION", "FRA_DCT_LIMIT"]

class TrafficVolumeLocationInfo(TypedDict, total=False):
    trafficVolumeId: TrafficVolumeId
    referenceLocation: ReferenceLocation

LoadState = Literal["NORMAL", "LOW_THRESHOLD", "HIGH_THRESHOLD", "OVERLOAD", "UNDEFINED"]

RunwayId = str

class AerodromeOrPublishedPointId(TypedDict, total=False):
    aerodrome: AerodromeICAOId
    point: PublishedPointId

FIRICAOId = str

