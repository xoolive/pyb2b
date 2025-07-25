from typing import TYPE_CHECKING, Literal, TypedDict, Union

from . import airspace, common

if TYPE_CHECKING:
    from . import flight

CountsCalculationType = Literal["ENTRY", "OCCUPANCY"]


class CountsInterval(TypedDict, total=False):
    duration: common.DurationHourMinute
    step: common.DurationHourMinute


OtmvStatus = Literal["PEAK", "SUSTAINED"]

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


class HotspotId(TypedDict, total=False):
    applicabilityPeriod: common.DateTimeMinutePeriod
    trafficVolume: airspace.TrafficVolumeId
    duration: common.DurationHourMinute


class FlightAtfcmMeasureLocation(TypedDict, total=False):
    trafficVolumeLocationInfo: airspace.TrafficVolumeLocationInfo
    measureSubType: MeasureSubType
    hotspotId: HotspotId
    mcdmState: MCDMState


HotspotStatus = Literal["DRAFT", "ACTIVE", "SOLVED", "ACCEPTABLE"]

HotspotSeverity = Literal["HIGH", "MEDIUM", "LOW"]


class Hotspot(TypedDict, total=False):
    hotspotId: HotspotId
    severity: HotspotSeverity
    status: HotspotStatus
    remark: str
    trafficVolumeDescription: str


class FlightHotspotLocation(TypedDict, total=False):
    hotspot: Hotspot
    referenceLocation: airspace.ReferenceLocation


RegulationId = str


class FlightRegulationLocation(TypedDict, total=False):
    regulationId: RegulationId
    referenceLocation: airspace.ReferenceLocation
    toConfirm: Literal["true", "false"]


ReroutingId = str

GroupReroutingIndicator = Literal[
    "NO_REROUTING", "UNINTERESTING", "INTERESTING", "OPPORTUNITY", "EXECUTED"
]


class GroupReroutingSummary(TypedDict, total=False):
    groupReroutingIndicator: GroupReroutingIndicator
    reroutingId: ReroutingId
    deltaCost: common.Cost
    deltaDelay: common.SignedDurationHourMinuteSecond


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

RegulationLocationCategory = Literal["ARRIVAL", "DEPARTURE", "ENROUTE"]


class RegulationCause(TypedDict, total=False):
    reason: RegulationReason
    locationCategory: RegulationLocationCategory
    iataDelayCode: str


FlowRoleSelection = Literal[
    "INCLUDED", "EXCLUDED", "EXEMPTED", "INCLUDED_AND_EXEMPTED"
]

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


FlowId = str

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


class MeasureId(TypedDict, total=False):
    REGULATION: RegulationId
    REROUTING: ReroutingId


class FlightMCDMInfo(TypedDict, total=False):
    leastAdvancedMCDMMeasure: MeasureId
    nrAssociatedMCDMRegulations: str
    nrAssociatedMCDMReroutings: str
    leastAdvancedMCDMState: MCDMState


class MeasureListRequest(common.Request):
    dataset: common.Dataset
    queryPeriod: common.DateTimeMinutePeriod
    tvs: Union[
        airspace.TrafficVolumeIdWildcard, list[airspace.TrafficVolumeIdWildcard]
    ]
    tvSets: Union[
        airspace.TrafficVolumeSetIdWildcard,
        list[airspace.TrafficVolumeSetIdWildcard],
    ]


RegulationIdWildcard = str


class RegulationOrMCDMOnlyListRequest(MeasureListRequest):
    regulations: Union[RegulationIdWildcard, list[RegulationIdWildcard]]
    reasons: Union[RegulationReason, list[RegulationReason]]


RegulationState = Literal[
    "APPLYING", "APPLIED", "CANCELLING", "CANCELLED", "TERMINATED"
]

RegulationField = Literal[
    "applicability",
    "autolink",
    "measureCherryPicked",
    "calculationType",
    "initialConstraints",
    "occupancyConstraints",
    "linkedRegulations",
    "location",
    "protectedLocation",
    "reason",
    "remark",
    "regulationState",
    "supplementaryConstraints",
    "lastUpdate",
    "noDelayWindow",
    "occupancyDuration",
    "updateCapacityRequired",
    "updateTVActivationRequired",
    "externallyEditable",
    "subType",
    "delayTVSet",
    "createdByFMP",
    "sourceHotspot",
    "mcdmRequired",
    "dataId",
    "scenarioReference",
    "delayConfirmationThreshold",
]


class RegulationListRequest(RegulationOrMCDMOnlyListRequest):
    requestedRegulationFields: Union[RegulationField, list[RegulationField]]
    regulationStates: Union[RegulationState, list[RegulationState]]


class RegulationOccupancyConstraint(TypedDict, total=False):
    constraintPeriod: common.DateTimeMinutePeriod
    sustainedCapacity: str
    peakCapacity: str
    pendingCapacityPercentage: str


class MeasureFromScenarioRepository(TypedDict, total=False):
    scenarioId: ScenarioId
    measureId: MeasureId


MCDMUserCategory = Literal[
    "IMPACTED_FMP", "ALL_FMP", "TOWER", "AIRCRAFT_OPERATOR", "NMOC"
]

MCDMRole = Literal[
    "INFO", "ROLE_INFO", "APPROVAL", "IMPLEMENTER", "INITIATOR", "NOT_INVOLVED"
]

MCDMCoordinationLevel = Literal["FLIGHT", "MEASURE"]


class MCDMRoleUserCategory(TypedDict, total=False):
    category: MCDMUserCategory
    coordinationLevel: MCDMCoordinationLevel
    role: MCDMRole


EhelpDeskOtherTicketType = Literal[
    "SUSPENDED_WHAT_TO_DO",
    "DEACTIVATE_MY_FLIGHT",
    "PROFILE_INCORRECT_CAPTURE",
    "MILITARY_FORMATION_DIFFERENT_CTOT",
    "QUERY_COMPETITORS_CTOT",
    "REQUEST_REROUTING_PROPOSAL",
]

MCDMTopicId = str

EhelpDeskRuleType = Literal[
    "SIT1_REQUEST_REJECTION",
    "DUPLICATE_REQUEST_REJECTION",
    "SLOT_EXTENSION",
    "SLOT_EXTENSION_CDM",
    "NOT_SUITABLE_FOR_MANUAL_IMPROVEMENT",
    "REGULATION_SLOT_IMPROVEMENT_MINIMUM_DELAY",
    "GENERAL_AUTO_RESPONSE",
    "NOT_REGULATED",
    "MOST_PENALISING_REGULATION_CHANGED",
    "FLIGHT_STATUS_REJECTION",
    "FLIGHT_CHANGED_REJECTION",
    "XSD_OR_RESTRICTION_VIOLATION",
    "SLOT_SWAP_REJECTION",
    "FORCE_REJECTION",
    "UNFORCE_REJECTION",
    "EXCLUDE_REJECTION",
    "RE_INCLUDE_REJECTION",
]


class EhelpDeskTicketFlightInfo(TypedDict, total=False):
    estimatedOffBlockTime: common.DateTimeMinute
    ctot: common.DateTimeMinute
    mostPenalisingRegulation: RegulationId


class EhelpDeskTicketResponseDetails(TypedDict, total=False):
    state: MCDMState
    responseFlightInfo: EhelpDeskTicketFlightInfo
    generalInterest: Literal["true", "false"]
    responseText: str
    automatedResponseRule: EhelpDeskRuleType
    supersededByRequest: MCDMTopicId


class EhelpDeskTicketRequestDetails(TypedDict, total=False):
    inResponseTo: EhelpDeskTicketFlightInfo
    requestText: str
    creationTime: common.DateTimeSecond
    lastModificationTime: common.DateTimeSecond


class EhelpDeskTicket(TypedDict, total=False):
    flightKeys: "flight.FlightKeys"
    ifplId: "flight.IFPLId"
    updateMCDMTopicId: MCDMTopicId
    requestDetails: EhelpDeskTicketRequestDetails
    responseDetails: EhelpDeskTicketResponseDetails


class EhelpDeskOtherTicket(EhelpDeskTicket):
    subType: EhelpDeskOtherTicketType


EhelpDeskImproveSlotInRegulationType = Literal[
    "MAINTAIN_SCHEDULE",
    "LATE_REVIEW_TO_CTOT",
    "LATE_REVIEW_TO_CTOT_ON_TAXI_TRACK",
    "CREW_TIME",
    "AIRPORT_CLOSURE",
    "AIRPORT_CLOSURE_NOISE",
    "CONNECTING_PASSENGER",
    "VIP_FLIGHT",
    "LIVE_STOCK",
    "SICK_PASSENGER",
    "RELIGIOUS_REASON",
    "DIVERSION",
    "DISPROPORTIONATE_DELAY_LATE_FILER_BUSINESS_JET",
    "DISPROPORTIONATE_DELAY_LATE_UPDATER",
    "NO_REASON",
]


class EhelpDeskImproveSlotInRegulation(EhelpDeskTicket):
    subType: EhelpDeskImproveSlotInRegulationType
    minRequestedCto: common.DateTimeMinute
    minRequestedCtot: common.DateTimeMinute


EhelpDeskSwapSlotsInRegulationType = Literal[
    "SAME_AIRCRAFT_OPERATORS", "DIFFERENT_AIRCRAFT_OPERATORS"
]


class EhelpDeskSwapSlotsInRegulation(EhelpDeskTicket):
    otherFlightKeys: "flight.FlightKeys"
    subType: EhelpDeskSwapSlotsInRegulationType


class EhelpDeskRemoveFlightsFromFmpStamRerouting(TypedDict, total=False):
    reroutingId: ReroutingId
    flights: Union["flight.FlightKeys", list["flight.FlightKeys"]]
    unsuccessfullyUpdatedFlights: str


EhelpDeskInformationTicketType = Literal[
    "OPERATIONAL_TEL_NUMBERS",
    "UNCLEAR_HEADLINE_NEWS",
    "CONTACT_CREW",
    "CANNOT_FIND_FLIGHT",
    "OTHER_INFO_REQUEST",
]


class EhelpDeskInformationTicket(EhelpDeskTicket):
    subType: EhelpDeskInformationTicketType


class EhelpDeskAddFlightInFmpStamRerouting(EhelpDeskTicket): ...


class EhelpDeskAddFlightsInFmpStamRerouting(TypedDict, total=False):
    reroutingId: ReroutingId
    flights: Union[
        EhelpDeskAddFlightInFmpStamRerouting,
        list[EhelpDeskAddFlightInFmpStamRerouting],
    ]


class EhelpDeskUnforceFlightInRegulation(EhelpDeskTicket): ...


class EhelpDeskUnforceFlightsInRegulation(TypedDict, total=False):
    flights: Union[
        EhelpDeskUnforceFlightInRegulation,
        list[EhelpDeskUnforceFlightInRegulation],
    ]


class EhelpDeskForceFlightInRegulation(EhelpDeskTicket):
    newCto: common.DateTimeMinute
    newCtot: common.DateTimeMinute


class EhelpDeskForceFlightsInRegulation(TypedDict, total=False):
    mostPenalisingRegulation: RegulationId
    flights: Union[
        EhelpDeskForceFlightInRegulation, list[EhelpDeskForceFlightInRegulation]
    ]


class EhelpDeskExcludeReIncludeFlightInRegulation(EhelpDeskTicket):
    regulations: Union[RegulationId, list[RegulationId]]


EhelpDeskExtendSlotInRegulationType = Literal[
    "LATE_PASSENGER",
    "PASSENGER_REMOVAL",
    "LOST_BAG",
    "BAG_REMOVAL",
    "CREW_REPLACEMENT",
    "SICK_OR_LATE_CREW",
    "UNWANTED_LATE_IMPROVEMENT",
    "ATC_WILL_NOT_RELEASE",
    "DEICING",
    "TECHNICAL_PROBLEM",
    "LATE_INBOUND_AIRCRAFT",
    "NO_REASON",
]


class EhelpDeskExtendSlotInRegulation(EhelpDeskTicket):
    subType: EhelpDeskExtendSlotInRegulationType


class EhelpDeskTicketChoice(TypedDict, total=False):
    forceFlightsInRegulation: EhelpDeskForceFlightsInRegulation
    unforceFlightsInRegulation: EhelpDeskUnforceFlightsInRegulation
    excludeFlightFromRegulation: EhelpDeskExcludeReIncludeFlightInRegulation
    reIncludeFlightInRegulation: EhelpDeskExcludeReIncludeFlightInRegulation
    improveSlotInRegulation: EhelpDeskImproveSlotInRegulation
    extendSlotInRegulation: EhelpDeskExtendSlotInRegulation
    swapSlotsInRegulation: EhelpDeskSwapSlotsInRegulation
    addFlightsInFmpStamRerouting: EhelpDeskAddFlightsInFmpStamRerouting
    removeFlightsFromFmpStamRerouting: (
        EhelpDeskRemoveFlightsFromFmpStamRerouting
    )
    information: EhelpDeskInformationTicket
    other: EhelpDeskOtherTicket


MCDMApprovalState = Literal["UNKNOWN", "APPROVED", "REJECTED", "ACKNOWLEDGED"]


class MCDMUserRoleAndApprovalState(TypedDict, total=False):
    user: common.AirNavigationUnitId
    role: MCDMRole
    approvalState: MCDMApprovalState


class MCDMTopic(TypedDict, total=False):
    topicId: MCDMTopicId
    dataId: common.PlanDataId


class MCDMStatefulTopic(MCDMTopic):
    measureId: MeasureId
    state: MCDMState
    initiator: common.AirNavigationUnitId
    initiatorIsImplementer: Literal["true", "false"]
    userRolesAndApprovalStates: Union[
        MCDMUserRoleAndApprovalState, list[MCDMUserRoleAndApprovalState]
    ]


class MCDMFlightTopic(MCDMStatefulTopic):
    flightKeys: "flight.FlightKeys"
    ifplId: "flight.IFPLId"
    ticket: EhelpDeskTicketChoice


class MCDMDeadlines(TypedDict, total=False):
    timeToCoordinate: common.DateTimeMinute
    timeToStartImplement: common.DateTimeMinute
    timeToImplement: common.DateTimeMinute


class MCDMUserAndRole(TypedDict, total=False):
    user: common.AirNavigationUnitId
    role: MCDMRole


class MCDMMeasureTopic(MCDMStatefulTopic):
    userCategories: Union[MCDMRoleUserCategory, list[MCDMRoleUserCategory]]
    deadlines: MCDMDeadlines
    flightTopics: Union[MCDMFlightTopic, list[MCDMFlightTopic]]
    predefinedUsersForFlightCoordinationLevel: Union[
        MCDMUserAndRole, list[MCDMUserAndRole]
    ]
    remark: str
    proposalNote: str
    proposalFeedback: str


LifeCycleEventType = Literal["CREATION", "UPDATE", "DELETION"]


class LifeCycleEvent(TypedDict, total=False):
    eventTime: common.DateTimeSecond
    userUpdateEventTime: common.DateTimeSecond
    userUpdateType: LifeCycleEventType
    userId: common.UserId


class Measure(TypedDict, total=False):
    dataId: common.PlanDataId
    applicability: common.DateTimeMinutePeriod
    measureCherryPicked: Literal["true", "false"]
    lastUpdate: LifeCycleEvent
    externallyEditable: Literal["true", "false"]
    subType: MeasureSubType
    createdByFMP: Literal["true", "false"]
    mcdmRequired: Literal["true", "false"]
    sourceHotspot: HotspotId
    scenarioReference: MeasureFromScenarioRepository
    mcdmInfo: MCDMMeasureTopic


class RegulationExceptionalConstraint(TypedDict, total=False):
    runwayVisualRange: common.DistanceM
    fcmMandatory: Literal["true", "false"]
    shift: Literal["true", "false"]


class RegulationInitialConstraint(TypedDict, total=False):
    constraintPeriod: common.DateTimeMinutePeriod
    normalRate: str
    pendingRate: str
    equipmentRate: str
    exceptionalConstraint: RegulationExceptionalConstraint


class RegulationSupplementaryConstraint(TypedDict, total=False):
    constraintPeriod: common.DateTimeMinutePeriod
    supplementaryRate: str


class Location(TypedDict, total=False): ...


class TrafficVolumeLocation(Location):
    referenceLocation: airspace.ReferenceLocation
    id: airspace.TrafficVolumeId
    flightLevels: airspace.FlightLevelRange
    description: str
    setIds: Union[
        airspace.TrafficVolumeSetId, list[airspace.TrafficVolumeSetId]
    ]


class RegulationOrMCDMOnly(Measure):
    regulationId: RegulationId
    reason: RegulationReason
    location: TrafficVolumeLocation
    protectedLocation: airspace.ReferenceLocation
    calculationType: CountsCalculationType
    initialConstraints: Union[
        RegulationInitialConstraint, list[RegulationInitialConstraint]
    ]
    supplementaryConstraints: Union[
        RegulationSupplementaryConstraint,
        list[RegulationSupplementaryConstraint],
    ]
    occupancyConstraints: Union[
        RegulationOccupancyConstraint, list[RegulationOccupancyConstraint]
    ]
    remark: str
    autolink: Literal["true", "false"]
    linkedRegulations: Union[RegulationId, list[RegulationId]]
    noDelayWindow: common.DurationHourMinute
    occupancyDuration: common.DurationHourMinute
    updateCapacityRequired: Literal["true", "false"]
    updateTVActivationRequired: Literal["true", "false"]
    delayTVSet: airspace.TrafficVolumeSetId
    delayConfirmationThreshold: common.DurationHourMinute


class Regulation(RegulationOrMCDMOnly):
    regulationState: RegulationState


class MeasureListReplyData(TypedDict, total=False):
    planTransferred: Literal["true", "false"]
    planCutOffReached: Literal["true", "false"]
    dataset: common.Dataset


class RegulationOrMCDMOnlyListReplyData(MeasureListReplyData): ...


class RegulationListReplyData(RegulationOrMCDMOnlyListReplyData):
    regulations: Union[Regulation, list[Regulation]]


class RegulationListReply(common.Reply):
    data: RegulationListReplyData
