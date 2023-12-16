from typing import Literal, TypedDict, Union
from . import airspace
from . import common


CountsCalculationType = Literal["ENTRY", "OCCUPANCY"]

class CountsInterval(TypedDict, total=False):
    duration: common.DurationHourMinute
    step: common.DurationHourMinute

GroupReroutingIndicator = Literal["NO_REROUTING", "UNINTERESTING", "INTERESTING", "OPPORTUNITY", "EXECUTED"]

ReroutingId = str

class GroupReroutingSummary(TypedDict, total=False):
    groupReroutingIndicator: GroupReroutingIndicator
    reroutingId: ReroutingId
    deltaCost: common.Cost
    deltaDelay: common.SignedDurationHourMinuteSecond

RegulationId = str

class MeasureId(TypedDict, total=False):
    REGULATION: RegulationId
    REROUTING: ReroutingId

MCDMState = Literal["DRAFT", "PROPOSED", "COORDINATED", "IMPLEMENTING", "IMPLEMENTED", "ABANDONED", "INTERRUPTED", "FINISHED"]

class FlightMCDMInfo(TypedDict, total=False):
    leastAdvancedMCDMMeasure: MeasureId
    nrAssociatedMCDMRegulations: str
    nrAssociatedMCDMReroutings: str
    leastAdvancedMCDMState: MCDMState

class HotspotId(TypedDict, total=False):
    applicabilityPeriod: common.DateTimeMinutePeriod
    trafficVolume: airspace.TrafficVolumeId
    duration: common.DurationHourMinute

HotspotSeverity = Literal["HIGH", "MEDIUM", "LOW"]

HotspotStatus = Literal["DRAFT", "ACTIVE", "SOLVED", "ACCEPTABLE"]

class Hotspot(TypedDict, total=False):
    hotspotId: HotspotId
    severity: HotspotSeverity
    status: HotspotStatus
    remark: str
    trafficVolumeDescription: str

class FlightHotspotLocation(TypedDict, total=False):
    hotspot: Hotspot
    referenceLocation: airspace.ReferenceLocation

ScenarioTrafficVolumeMatchingKind = Literal["SAME_TRAFFIC_VOLUME", "SAME_REFERENCE_LOCATION", "OVERLAPPING_REFERENCE_LOCATION", "INDIRECT_OFFLOAD"]

ScenarioId = str

class TrafficVolumeScenarios(TypedDict, total=False):
    solutionTrafficVolumeId: airspace.TrafficVolumeId
    trafficVolumeMatchingKind: ScenarioTrafficVolumeMatchingKind
    scenarios: Union[ScenarioId, list[ScenarioId]]

MeasureSubType = Literal["GROUND_DELAY", "TAKE_OFF_NOT_BEFORE", "TAKE_OFF_NOT_AFTER", "MINIMUM_DEPARTURE_INTERVAL", "MILES_MINUTES_IN_TRAIL", "GROUND_LEVEL_CAP", "AIRBORNE_LEVEL_CAP", "GROUND_HORIZONTAL_REROUTING", "AIRBORNE_HORIZONTAL_REROUTING", "TERMINAL_PROCEDURE_CHANGE", "OTHER_KIND_OF_STAM_MEASURE"]

class FlightAtfcmMeasureLocation(TypedDict, total=False):
    trafficVolumeLocationInfo: airspace.TrafficVolumeLocationInfo
    measureSubType: MeasureSubType
    hotspotId: HotspotId
    mcdmState: MCDMState

FlowId = str

FlowRoleSelection = Literal["INCLUDED", "EXCLUDED", "EXEMPTED", "INCLUDED_AND_EXEMPTED"]

CountsValue = str

class ScenarioImpact(TypedDict, total=False):
    totalCommonFlightCount: CountsValue
    totalOtherFlightCount: CountsValue
    scenarioTrafficVolumeEntryPeriod: common.DateTimeMinutePeriod

FlowType = Literal["LINKED", "ASSOCIATED", "SCENARIO"]

class Flow(TypedDict, total=False):
    id: FlowId
    type: FlowType
    role: FlowRoleSelection
    applicableScenarios: TrafficVolumeScenarios
    scenarioImpact: ScenarioImpact

class FlightRegulationLocation(TypedDict, total=False):
    regulationId: RegulationId
    referenceLocation: airspace.ReferenceLocation
    toConfirm: Literal['true', 'false']

OtmvStatus = Literal["PEAK", "SUSTAINED"]

RegulationReason = Literal["ACCIDENT_INCIDENT", "ATC_CAPACITY", "AERODROME_SERVICES", "AERODROME_CAPACITY", "ATC_INDUSTRIAL_ACTION", "NON_ATC_INDUSTRIAL_ACTION", "WEATHER", "AIRSPACE_MANAGEMENT", "SPECIAL_EVENT", "ATC_ROUTINGS", "ATC_STAFFING", "ATC_EQUIPMENT", "ENVIRONMENTAL_ISSUES", "OTHERS"]

RegulationLocationCategory = Literal["ARRIVAL", "DEPARTURE", "ENROUTE"]

class RegulationCause(TypedDict, total=False):
    reason: RegulationReason
    locationCategory: RegulationLocationCategory
    iataDelayCode: str

