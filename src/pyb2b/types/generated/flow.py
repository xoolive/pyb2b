from typing import Literal, TypedDict, Union

from . import airspace, common

HotspotStatus = Literal["DRAFT", "ACTIVE", "SOLVED", "ACCEPTABLE"]

HotspotSeverity = Literal["HIGH", "MEDIUM", "LOW"]


class HotspotId(TypedDict, total=False):
    applicabilityPeriod: common.DateTimeMinutePeriod
    trafficVolume: airspace.TrafficVolumeId
    duration: common.DurationHourMinute


class Hotspot(TypedDict, total=False):
    hotspotId: HotspotId
    severity: HotspotSeverity
    status: HotspotStatus
    remark: str
    trafficVolumeDescription: str


class FlightHotspotLocation(TypedDict, total=False):
    hotspot: Hotspot
    referenceLocation: airspace.ReferenceLocation


ScenarioId = str

ScenarioTrafficVolumeMatchingKind = Literal[
    "SAME_TRAFFIC_VOLUME",
    "SAME_REFERENCE_LOCATION",
    "OVERLAPPING_REFERENCE_LOCATION",
    "INDIRECT_OFFLOAD",
]


class TrafficVolumeScenarios(TypedDict, total=False):
    solutionTrafficVolumeId: airspace.TrafficVolumeId
    trafficVolumeMatchingKind: ScenarioTrafficVolumeMatchingKind
    scenarios: Union[ScenarioId, list[ScenarioId]]


RegulationId = str

MCDMState = Literal[
    "DRAFT",
    "PROPOSED",
    "COORDINATED",
    "IMPLEMENTING",
    "IMPLEMENTED",
    "ABANDONED",
    "INTERRUPTED",
    "FINISHED",
]

ReroutingId = str


class MeasureId(TypedDict, total=False):
    REGULATION: RegulationId
    REROUTING: ReroutingId


class FlightMCDMInfo(TypedDict, total=False):
    leastAdvancedMCDMMeasure: MeasureId
    nrAssociatedMCDMRegulations: str
    nrAssociatedMCDMReroutings: str
    leastAdvancedMCDMState: MCDMState


GroupReroutingIndicator = Literal[
    "NO_REROUTING", "UNINTERESTING", "INTERESTING", "OPPORTUNITY", "EXECUTED"
]


class GroupReroutingSummary(TypedDict, total=False):
    groupReroutingIndicator: GroupReroutingIndicator
    reroutingId: ReroutingId
    deltaCost: common.Cost
    deltaDelay: common.SignedDurationHourMinuteSecond


class FlightRegulationLocation(TypedDict, total=False):
    regulationId: RegulationId
    referenceLocation: airspace.ReferenceLocation
    toConfirm: Literal["true", "false"]


OtmvStatus = Literal["PEAK", "SUSTAINED"]

MeasureSubType = Literal[
    "GROUND_DELAY",
    "TAKE_OFF_NOT_BEFORE",
    "TAKE_OFF_NOT_AFTER",
    "MINIMUM_DEPARTURE_INTERVAL",
    "MILES_MINUTES_IN_TRAIL",
    "GROUND_LEVEL_CAP",
    "AIRBORNE_LEVEL_CAP",
    "GROUND_HORIZONTAL_REROUTING",
    "AIRBORNE_HORIZONTAL_REROUTING",
    "TERMINAL_PROCEDURE_CHANGE",
    "OTHER_KIND_OF_STAM_MEASURE",
]


class FlightAtfcmMeasureLocation(TypedDict, total=False):
    trafficVolumeLocationInfo: airspace.TrafficVolumeLocationInfo
    measureSubType: MeasureSubType
    hotspotId: HotspotId
    mcdmState: MCDMState


FlowId = str

FlowType = Literal["LINKED", "ASSOCIATED", "SCENARIO"]

FlowRoleSelection = Literal[
    "INCLUDED", "EXCLUDED", "EXEMPTED", "INCLUDED_AND_EXEMPTED"
]

CountsValue = str


class ScenarioImpact(TypedDict, total=False):
    totalCommonFlightCount: CountsValue
    totalOtherFlightCount: CountsValue
    scenarioTrafficVolumeEntryPeriod: common.DateTimeMinutePeriod


class Flow(TypedDict, total=False):
    id: FlowId
    type: FlowType
    role: FlowRoleSelection
    applicableScenarios: TrafficVolumeScenarios
    scenarioImpact: ScenarioImpact


RegulationLocationCategory = Literal["ARRIVAL", "DEPARTURE", "ENROUTE"]

RegulationReason = Literal[
    "ACCIDENT_INCIDENT",
    "ATC_CAPACITY",
    "AERODROME_SERVICES",
    "AERODROME_CAPACITY",
    "ATC_INDUSTRIAL_ACTION",
    "NON_ATC_INDUSTRIAL_ACTION",
    "WEATHER",
    "AIRSPACE_MANAGEMENT",
    "SPECIAL_EVENT",
    "ATC_ROUTINGS",
    "ATC_STAFFING",
    "ATC_EQUIPMENT",
    "ENVIRONMENTAL_ISSUES",
    "OTHERS",
]


class RegulationCause(TypedDict, total=False):
    reason: RegulationReason
    locationCategory: RegulationLocationCategory
    iataDelayCode: str
