from typing import Literal, TypedDict, Union

from . import airspace, common, flow


class FlightPlanListRequest(common.Request):
    aircraftId: str
    aerodromeOfDeparture: str
    nonICAOAerodromeOfDeparture: Literal["true", "false"]
    airFiled: Literal["true", "false"]
    aerodromeOfDestination: str
    nonICAOAerodromeOfDestination: Literal["true", "false"]
    estimatedOffBlockTime: common.DateTimeMinutePeriod


IFPLId = str

ExtendedAircraftICAOId = str


class FlightKeys(TypedDict, total=False):
    aircraftId: ExtendedAircraftICAOId
    aerodromeOfDeparture: airspace.AerodromeICAOId
    nonICAOAerodromeOfDeparture: Literal["true", "false"]
    airFiled: Literal["true", "false"]
    aerodromeOfDestination: airspace.AerodromeICAOId
    nonICAOAerodromeOfDestination: Literal["true", "false"]
    estimatedOffBlockTime: common.DateTimeMinute


class FlightIdentificationOutput(TypedDict, total=False):
    id: IFPLId
    keys: FlightKeys


FlightPlanStatus = Literal[
    "FILED",
    "AIRBORNE",
    "SUSPENDED",
    "CLOSED",
    "BACKUP",
    "TACT_DELETED",
    "TERMINATED",
    "OFFBLOCKS",
]


class FlightPlanSummary(TypedDict, total=False):
    id: FlightIdentificationOutput
    status: FlightPlanStatus


FlightPlanMessageType = Literal[
    "FPL",
    "CHG",
    "CNL",
    "DLA",
    "DEP",
    "ARR",
    "RQP",
    "RQS",
    "FNM",
    "MFS",
    "APL",
    "ACH",
    "AFP",
]

FlightPlanMessageStatus = Literal[
    "INVALID", "REJECTED", "REFERRED", "DELETED", "DISCARD", "MULTIPLE"
]


class InvalidFiling(TypedDict, total=False):
    filingTime: common.DateTimeSecond
    invalidMessageType: FlightPlanMessageType
    invalidMessageStatus: FlightPlanMessageStatus
    keys: FlightKeys


class FlightPlanOrInvalidFiling(TypedDict, total=False):
    lastValidFlightPlan: FlightPlanSummary
    currentInvalid: InvalidFiling


class FlightPlanListReplyData(TypedDict, total=False):
    summaries: Union[FlightPlanOrInvalidFiling, list[FlightPlanOrInvalidFiling]]


class FlightPlanListReply(common.Reply):
    data: FlightPlanListReplyData


FlightField = Literal[
    "divertedAerodromeOfDestination",
    "readyEstimatedOffBlockTime",
    "cdmEstimatedOffBlockTime",
    "calculatedOffBlockTime",
    "actualOffBlockTime",
    "aircraftType",
    "estimatedTakeOffTime",
    "calculatedTakeOffTime",
    "actualTakeOffTime",
    "ctotShiftAlreadyAppliedByTower",
    "taxiTime",
    "currentDepartureTaxiTimeAndProcedure",
    "revisionTimes",
    "estimatedTimeOfArrival",
    "calculatedTimeOfArrival",
    "actualTimeOfArrival",
    "requestedFlightLevel",
    "timeAtReferenceLocationEntry",
    "timeAtReferenceLocationExit",
    "flightLevelAtReferenceLocationEntry",
    "flightLevelAtReferenceLocationExit",
    "trendAtReferenceLocationEntry",
    "trendAtReferenceLocationExit",
    "trendAtReferenceLocationMiddle",
    "lateFiler",
    "lateUpdater",
    "suspensionStatus",
    "suspensionInfo",
    "exclusionFromRegulations",
    "famStatus",
    "readyStatus",
    "aircraftOperator",
    "operatingAircraftOperator",
    "reroutingIndicator",
    "newRouteMinShiftDelayImprovement",
    "reroutable",
    "cdm",
    "slotIssued",
    "proposalInformation",
    "bestReroutingIndicator",
    "exemptedFromRegulations",
    "delay",
    "delayCharacteristics",
    "mostPenalisingRegulation",
    "hasOtherRegulations",
    "regulationLocations",
    "atfcmMeasureLocations",
    "lastATFMMessageType",
    "lastATFMMessageReceivedOrSent",
    "runwayVisualRange",
    "confirmedCTFM",
    "requestedInitialFlightLevel",
    "requestedInitialSpeed",
    "estimatedElapsedTime",
    "filingRule",
    "initialFPLMessageOriginator",
    "lastFPLMessageOriginator",
    "icaoRoute",
    "routeLength",
    "defaultReroutingRequestedFlightLevel",
    "defaultReroutingRequestedSpeed",
    "departureTolerance",
    "mostPenalisingRegulationCause",
    "lastATFMMessageOriginator",
    "ftfmPointProfile",
    "rtfmPointProfile",
    "ctfmPointProfile",
    "ftfmAirspaceProfile",
    "rtfmAirspaceProfile",
    "ctfmAirspaceProfile",
    "ftfmRequestedFlightLevels",
    "rtfmRequestedFlightLevels",
    "ctfmRequestedFlightLevels",
    "flightHistory",
    "operationalLog",
    "equipmentCapabilityAndStatus",
    "ftfmRestrictionProfile",
    "rtfmRestrictionProfile",
    "ctfmRestrictionProfile",
    "cfmuFlightType",
    "ccamsSSRCode",
    "filedRegistrationMark",
    "isProposalFlight",
    "hasBeenForced",
    "caughtInHotspots",
    "hotspots",
    "mcdmInfo",
    "worstLoadStateAtReferenceLocation",
    "compareWithOtherTrafficType",
    "ctotLimitReason",
    "profileValidity",
    "targetTimeOverFix",
    "flightState",
    "lastKnownPosition",
    "highestModelPointProfile",
    "highestModelAirspaceProfile",
    "highestModelRestrictionProfile",
    "highestModelTrafficVolumeProfile",
    "slotSwapCounter",
    "slotSwapCandidateList",
    "aircraftAddress",
    "arrivalInformation",
    "slotZone",
    "flightDataVersionNr",
    "applicableScenarios",
    "apiSubmissionRules",
    "avoidedRegulations",
    "routeChargeIndicator",
    "fuelConsumptionIndicator",
    "excludedRegulations",
    "yoyoFlightForLocation",
    "turnFlightForLocation",
    "minimumRequestedRVR",
    "wakeTurbulenceCategory",
    "alternateAerodromes",
    "flightCriticality",
    "oceanicReroute",
    "visibility",
    "iataFlightDesignator",
    "activeACDMAlerts",
    "highestModelRouteChargeIndicator",
    "highestModelFuelConsumptionIndicator",
    "aoReroutingFeedbacks",
]

FlightDataset = Literal["flightPlan", "flightPlanHistory", "flight"]

AircraftIATAId = str


class IATAFlightKeys(TypedDict, total=False):
    flightDesignator: AircraftIATAId
    estimatedOffBlockTime: common.DateTimeMinute


class FlightIdentificationInput(TypedDict, total=False):
    id: IFPLId
    keys: FlightKeys
    iataKeys: IATAFlightKeys


class FlightRetrievalRequest(common.Request):
    dataset: common.Dataset
    includeProposalFlights: Literal["true", "false"]
    flightId: FlightIdentificationInput
    requestedFlightDatasets: Union[FlightDataset, list[FlightDataset]]
    requestedFlightFields: Union[FlightField, list[FlightField]]


ReroutableStatus = Literal[
    "CANNOT_BE_REROUTED", "TRY_ALLOWED", "TRY_AND_APPLY_ALLOWED"
]

ProfileValidityKind = Literal["VIOLATIONS", "NO_VIOLATIONS", "UNKNOWN"]


class ProfileValidity(TypedDict, total=False):
    profileValidityKind: ProfileValidityKind
    lastValidEOBT: common.DateTimeMinute


AircraftOperatorICAOId = str

FlightDataVersionNumber = str

TurnFlightForLocationKind = Literal[
    "NO_SHARP_TURN",
    "CRITICAL_SHARP_TURN",
    "INTERESTING_SHARP_TURN",
    "UNINTERESTING_SHARP_TURN",
    "CRITICAL_ELSEWHERE",
    "INTERESTING_ELSEWHERE",
    "UNINTERESTING_ELSEWHERE",
    "CRITICAL_INSIDE",
    "INTERESTING_INSIDE",
    "UNINTERESTING_INSIDE",
]


class TurnFlightForLocation(TypedDict, total=False):
    ftfmTurn: TurnFlightForLocationKind
    locationModelTurnKind: TurnFlightForLocationKind


FilingRule = Literal[
    "NOT_AUTHORISED", "OPERATOR_MUST_REFILE", "FILING_ALLOWED_BY_AO_CFMU"
]


class ExclusionFromRegulations(TypedDict, total=False):
    onTrafficVolume: Literal["true", "false"]
    count: str
    all: Literal["true", "false"]
    hasBeenExcluded: Literal["true", "false"]


FlightTrend = Literal["CRUISE", "CLIMB", "DESCENT", "NONE"]


class FlightAirspace(TypedDict, total=False):
    airspaceId: airspace.AirspaceId
    airspaceType: airspace.AirspaceType
    firstEntryTime: common.DateTimeSecond
    firstEntryFlightLevel: airspace.FlightLevel
    lastExitFlightLevel: airspace.FlightLevel
    firstEntryTrend: FlightTrend
    middleTrend: FlightTrend
    firstEntryDistance: common.DistanceNM
    lastExitTime: common.DateTimeSecond
    lastExitTrend: FlightTrend
    lastExitDistance: common.DistanceNM
    occupancyDuration: common.DurationHourMinuteSecond
    occupancyDistance: common.DistanceNM
    activated: Literal["true", "false"]


class RequestedFlightLevel(TypedDict, total=False):
    flightLevel: airspace.FlightLevel
    segmentSequenceNumber: str
    relativeDistance: str


SSRCode = str

DelayCharacteristics = Literal[
    "EXCEEDS_DELAY_CONFIRMATION", "ADJUSTED_TO_CLOCK"
]


class SlotZone(TypedDict, total=False):
    beforeCTO: common.DurationMinute
    afterCTO: common.DurationMinute


class ReadyStatus(TypedDict, total=False):
    readyForImprovement: Literal["true", "false"]
    readyToDepart: Literal["true", "false"]
    revisedTaxiTime: common.DurationHourMinute


FlightCriticalityKind = Literal[
    "CRITICAL_DUE_TO_AIRPORT_CLOSURE",
    "CRITICAL_DUE_TO_NOISE_ABATEMENT",
    "CRITICAL_DUE_TO_CREW_TIME",
    "CRITICAL_DUE_TO_PASSENGER_CONNECTIONS",
    "CRITICAL_DUE_TO_TURNAROUND_CRITICAL",
    "CRITICAL_DUE_TO_AIRFRAME_UTILISATION",
    "CRITICAL_DUE_TO_PASSENGER_DELAY_COMPENSATION",
    "CRITICAL_DUE_TO_OTHER_REASONS",
]


class FlightCriticalityIndicator(TypedDict, total=False):
    kind: FlightCriticalityKind
    comment: str


FlightState = Literal[
    "PLANNED",
    "PLANNED_SLOT_ALLOCATED",
    "PLANNED_REROUTED",
    "PLANNED_SLOT_ALLOCATED_REROUTED",
    "FILED",
    "FILED_SLOT_ALLOCATED",
    "FILED_SLOT_ISSUED",
    "TACT_ACTIVATED",
    "ATC_ACTIVATED",
    "CANCELLED",
    "TERMINATED",
]

FlightEventType = Literal[
    "ACH",
    "ADI",
    "AFI",
    "APL",
    "APR",
    "ATT",
    "AXT",
    "CAL",
    "CDI",
    "CEO",
    "CMC",
    "CMN",
    "CNC",
    "CPR",
    "CPT",
    "XCR",
    "CRL",
    "CRQ",
    "CSC",
    "CSU",
    "EDI",
    "EMR",
    "FCM",
    "FDI",
    "FLS",
    "FSA",
    "FUM",
    "IAR",
    "ICA",
    "ICH",
    "IDE",
    "IDL",
    "IFP",
    "MET",
    "MSG",
    "NEV",
    "OAR",
    "OCA",
    "ODA",
    "OEX",
    "OIC",
    "ORX",
    "PTX",
    "REA",
    "RFR",
    "RJT",
    "PFI",
    "RRM",
    "RSI",
    "RSU",
    "SCA",
    "SCM",
    "SIP",
    "SIT",
    "SMM",
    "SPA",
    "SRJ",
    "SSC",
    "SSM",
    "SSR",
    "SUS",
    "TAC",
    "TAM",
    "TDE",
    "TDI",
    "TPF",
    "TRC",
    "TRM",
    "TSA",
    "TSC",
    "TTE",
    "UFA",
    "UXC",
    "UCD",
    "SSP",
    "OCM",
    "DAU",
    "OAI",
    "TAI",
    "GAI",
    "PDI",
    "ADT",
    "RSF",
    "RRF",
    "RPU",
    "UAA",
    "UFC",
]


class FlightEvent(TypedDict, total=False):
    timestamp: common.DateTimeSecond
    type: FlightEventType
    resultingState: FlightState
    resultingOffBlockTime: common.DateTimeMinute
    efdSent: Literal["true", "false"]
    fumSent: Literal["true", "false"]


FlightOperationalLogEntryType = Literal[
    "UNDEFINED",
    "INCOMING_MESSAGE",
    "ERRONEOUS_INCOMING_MESSAGE",
    "OUTGOING_MESSAGE",
    "VIOLATION",
    "HISTORY",
    "WARNING",
    "PROCESS_ERROR",
    "ERROR_MESSAGE",
    "ENVIRONMENT_MESSSAGE",
    "USER_COMMAND",
    "TEXT_MESSAGE",
]


class FlightOperationalLogEntry(TypedDict, total=False):
    timestamp: common.DateTimeSecond
    type: FlightOperationalLogEntryType
    etfmsId: str
    ifplId: IFPLId
    issuer: str
    message: str
    summaryFields: str


EquipmentStatus = Literal["EQUIPPED", "NOT_EQUIPPED"]


class EquipmentCapabilityAndStatus(TypedDict, total=False):
    gbas: EquipmentStatus
    lpv: EquipmentStatus
    loranC: EquipmentStatus
    dme: EquipmentStatus
    fmcWprAcars: EquipmentStatus
    dFisAcars: EquipmentStatus
    pdcAcars: EquipmentStatus
    adf: EquipmentStatus
    gnss: EquipmentStatus
    hfRtf: EquipmentStatus
    inertialNavigation: EquipmentStatus
    cpdlcAtnVdlMode2: EquipmentStatus
    cpdlcFans1AHFDL: EquipmentStatus
    cpdlcFans1AVdlModeA: EquipmentStatus
    cpdlcFans1AVdlMode2: EquipmentStatus
    cpdlcFans1ASatcomInmarsat: EquipmentStatus
    cpdlcFans1ASatcomMtsat: EquipmentStatus
    cpdlcFans1ASatcomIridium: EquipmentStatus
    mls: EquipmentStatus
    ils: EquipmentStatus
    atcRtfSatcomInmarsat: EquipmentStatus
    atcRtfSatcomMtsat: EquipmentStatus
    atcRtfSatcomIridium: EquipmentStatus
    vor: EquipmentStatus
    rcp1: EquipmentStatus
    rcp2: EquipmentStatus
    rcp3: EquipmentStatus
    rcp4: EquipmentStatus
    rcp5: EquipmentStatus
    rcp6: EquipmentStatus
    rcp7: EquipmentStatus
    rcp8: EquipmentStatus
    rcp9: EquipmentStatus
    pbnApproved: EquipmentStatus
    standard: EquipmentStatus
    tacan: EquipmentStatus
    uhfRtf: EquipmentStatus
    vhfRtf: EquipmentStatus
    rvsm: EquipmentStatus
    mnps: EquipmentStatus
    khz833: EquipmentStatus
    other: EquipmentStatus


TaxiTimeSource = Literal["ENV", "FPL", "RWY", "REA", "CDM"]


class TaxiTimeAndProcedure(TypedDict, total=False):
    taxiTime: common.DurationHourMinute
    taxiTimeSource: TaxiTimeSource
    terminalProcedure: airspace.TerminalProcedure


IntervalPosition = Literal["BEFORE", "INSIDE", "AFTER"]


class ActualTimeAtTarget(TypedDict, total=False):
    estimatedActualTimeAtTarget: common.DateTimeMinute
    targetTimeCompliance: IntervalPosition


class TargetTime(TypedDict, total=False):
    regulationId: flow.RegulationId
    targetTime: common.DateTimeSecond
    targetLevel: airspace.FlightLevel
    aerodromeICAOId: airspace.AerodromeICAOId
    point: airspace.ICAOPoint
    flightPlanPoint: Literal["true", "false"]
    coveredDistance: common.DistanceNM
    actualTimeAtTarget: ActualTimeAtTarget


YoYoFlightForLocationKind = Literal[
    "NO_YOYO",
    "CRITICAL_YOYO",
    "NON_CRITICAL_YOYO",
    "CRITICAL_ELSEWHERE",
    "NON_CRITICAL_ELSEWHERE",
    "CRITICAL_COMPLETELY_INSIDE",
    "NON_CRITICAL_COMPLETELY_INSIDE",
    "LOCATION_INSIDE_CRITICAL",
    "LOCATION_INSIDE_NON_CRITICAL",
    "CRITICAL_STARTS_INSIDE",
    "NON_CRITICAL_STARTS_INSIDE",
    "CRITICAL_ENDS_INSIDE",
    "NON_CRITICAL_ENDS_INSIDE",
]


class YoYoFlightForLocation(TypedDict, total=False):
    ftfmYoYo: YoYoFlightForLocationKind
    locationModelYoYoKind: YoYoFlightForLocationKind


ReroutingState = Literal[
    "PRODUCED", "EXECUTED", "TIMED_OUT", "REJECTED", "REVOKED", "NO_MATCH"
]

ReroutingReason = Literal[
    "ATFM_EXECUTED",
    "AO",
    "ATFCM_PURPOSE_PROPOSAL",
    "ATC_PURPOSE_PROPOSAL",
    "FLIGHT_EFFICIENCY_PURPOSE_PROPOSAL",
    "STAM_PURPOSE_PROPOSAL",
    "CDR_OPPORTUNITY_PROPOSAL",
]


class ReroutingIndicator(TypedDict, total=False):
    rerouted: Literal["true", "false"]
    reason: ReroutingReason
    state: ReroutingState


class MessageOriginator(TypedDict, total=False):
    airNavigationUnitId: common.AirNavigationUnitId
    address: airspace.NetworkAddress


CTOTLimitReason = Literal[
    "SLOT_TIME_NOT_LIMITED",
    "FORCED_BY_TOWER",
    "FORCED_BY_NMOC",
    "WAS_FORCED_BY_NMOC",
    "FORCED_BY_CHAMAN",
    "FORCED_BY_STAM_MEASURE",
    "LIMITED_BY_VIOLATION",
    "LIMITED_BY_VIOLATION_THEN_ZERO_RATE_OR_RVR",
    "SLOT_EXTENSION",
]


class FlightPoint(TypedDict, total=False):
    timeOver: common.DateTimeSecond
    flightLevel: airspace.FlightLevel
    entryTrend: FlightTrend
    exitTrend: FlightTrend
    associatedRouteOrTerminalProcedure: airspace.RouteOrTerminalProcedure
    coveredDistance: common.DistanceNM
    isVisible: Literal["true", "false"]
    aerodrome: airspace.AerodromeICAOId
    point: airspace.ICAOPoint
    flightPlanPoint: Literal["true", "false"]


WakeTurbulenceCategory = Literal["LIGHT", "MEDIUM", "HEAVY", "SUPER"]

FlightVisibility = Literal[
    "NO_VISIBILITY",
    "VISIBLE",
    "INVISIBLE",
    "INVISIBLE_BEFORE_VISIBLE",
    "VISIBLE_AFTER_INVISIBLE",
    "VISIBLE_BEFORE_INVISIBLE",
    "VISIBLE_BETWEEN_INVISIBLE",
    "VISIBLE_WITH_SKIPOUT",
]

AircraftRegistrationMark = str

AircraftTypeICAOId = str

DepartureAirportType = Literal["STANDARD", "ADVANCED_ATC_TWR", "CDM"]

CDMStatus = Literal[
    "DEPARTING_FROM_STANDARD_AIRPORT",
    "DEPARTING_FROM_CDM_AIRPORT",
    "ESTIMATED",
    "TARGETED",
    "PRE_SEQUENCED",
    "ACTUAL_OFFBLOCK",
    "PREDICTED",
]

OtherAircraftTypeDesignation_DataType = str


class AircraftType(TypedDict, total=False):
    icaoId: AircraftTypeICAOId
    otherDesignation: OtherAircraftTypeDesignation_DataType


TerminalOrApronStandName = str

ATVFlightStatusOutbound = Literal[
    "SCH",
    "INI",
    "BRD",
    "BRC",
    "RDY",
    "OBK",
    "DEP",
    "CNX",
    "RTN",
    "RET",
    "RPO",
    "RDI",
    "DEI",
    "TXD",
]

AircraftICAOId = str

ReasonForDPICancellation = Literal[
    "NO_AIRPORT_SLOT",
    "TOBT_UNKNOWN_OR_EXPIRED",
    "TSAT_EXPIRED",
    "RETURN_TO_STAND",
    "FLIGHT_PLAN_INVALID",
    "FLIGHT_CANCEL_IN_AODB",
    "OTHER",
    "UNDEFINED",
    "UNDO_ADPI",
]

AircraftTypeIATAId = str

DepartureStatus = Literal["OK", "DEICING"]


class CDMInfo(TypedDict, total=False):
    turnaroundTargetTakeOffTime: common.DateTimeMinute
    earliestTargetTakeOffTime: common.DateTimeMinute
    consolidatedTargetTakeOffTime: common.DateTimeMinute
    atcTargetTakeOffTime: common.DateTimeMinute
    taxiTime: common.DurationHourMinuteSecond
    offBlockTimeDiscrepancy: Literal["true", "false"]
    flightStatusOutbound: ATVFlightStatusOutbound
    departureProc: airspace.TerminalProcedure
    departureRunway: airspace.RunwayId
    departureTerminal: TerminalOrApronStandName
    departureApronStand: TerminalOrApronStandName
    aircraftTypeDiscrepancy: Literal["true", "false"]
    aircraftType: AircraftType
    aircraftTypeIATA: AircraftTypeIATAId
    registrationMark: AircraftRegistrationMark
    registrationMarkDiscrepancy: Literal["true", "false"]
    departureStatus: DepartureStatus
    targetOffBlockTime: common.DateTimeMinute
    targetStartupApprovalTime: common.DateTimeMinute
    aircraftIdInbound: AircraftICAOId
    ifplIdInbound: IFPLId
    registrationMarkInbound: AircraftRegistrationMark
    cancelReason: ReasonForDPICancellation
    iataFlightDesignator: AircraftIATAId
    iataFlightDesignatorDiscrepancy: Literal["true", "false"]


class CDM(TypedDict, total=False):
    status: CDMStatus
    airportType: DepartureAirportType
    info: CDMInfo


Latitude = str

Longitude = str


class Position(TypedDict, total=False):
    latitude: Latitude
    longitude: Longitude


class FourDPosition(TypedDict, total=False):
    timeOver: common.DateTimeSecond
    position: Position
    level: airspace.FlightLevel


class RevisionTimes(TypedDict, total=False):
    timeToInsertInSequence: common.DurationHourMinute
    timeToRemoveFromSequence: common.DurationHourMinute


class DepartureTolerance(TypedDict, total=False):
    toleranceWindow: common.TimeHourMinutePeriod
    extended: Literal["true", "false"]


class APISubmissionRules(TypedDict, total=False):
    latestSubmissionTargetTakeOffAPI: common.DateTimeMinute
    earliestSubmissionTargetTimeOverAPI: common.DateTimeMinute


SuspensionStatus = Literal[
    "NOT_SUSPENDED",
    "SLOT_MISSED",
    "REGULATION_CONFIRMATION",
    "DELAY_CONFIRMATION",
    "TRAFFIC_VOLUMES_CONDITION",
    "NOT_REPORTED_AS_AIRBORNE",
    "FLIGHT_PLAN_REVALIDATION",
    "MANUAL_SUSPENSION",
    "AIRPORT_SUSPENSION",
    "V_MANUAL_SUSPENSION",
]

ATFMMessageType = Literal[
    "DES",
    "ERR",
    "FCM",
    "FUM",
    "FLS",
    "REA",
    "RFI",
    "RJT",
    "RRN",
    "RRP",
    "SAM",
    "SIP",
    "SLC",
    "SMM",
    "SPA",
    "SRJ",
    "SRM",
    "SWM",
    "UNK",
]


class LoadStateAtReferenceLocation(TypedDict, total=False):
    ENTRY: airspace.LoadState
    OCCUPANCY: flow.OtmvStatus


class SlotSwapCandidate(TypedDict, total=False):
    ifplId: IFPLId
    subjectDeltaDelayMinutes: str
    candidateDeltaDelayMinutes: str
    swapDecideByTime: common.DateTimeMinute


ICAOAircraftAddress = str

AircraftIdDataSource = Literal["DDR", "API", "DPI", "FPM"]


class AircraftIATAIdFromDataSource(TypedDict, total=False):
    id: AircraftIATAId
    dataSource: AircraftIdDataSource


ACDMAlertSeverity = Literal["HIGH", "MEDIUM", "LOW"]

ACDMAlertCode = str


class ACDMAlertData(TypedDict, total=False):
    alertCode: ACDMAlertCode
    timestamp: common.DateTimeMinute
    inconsistencyDetected: str
    actionToTake: str
    consequencesNote: str
    severity: ACDMAlertSeverity


CfmuFlightType = Literal[
    "MFD", "IFPL", "ACT", "TACT_ACTIVATED", "TERMINATED", "PREDICTED_FLIGHT"
]

ImpactSeverityIndicator = Literal["OT", "E", "EI", "L", "LI", "LIP"]

ATVFlightStatusInbound = Literal[
    "AIR",
    "CNX",
    "DBC",
    "DBR",
    "DIV",
    "FIR",
    "FNL",
    "GOA",
    "IBK",
    "IDH",
    "INI",
    "SCH",
    "TMA",
    "TXI",
]


class ArrivalInformation(TypedDict, total=False):
    flightStatusInbound: ATVFlightStatusInbound
    registrationMark: AircraftRegistrationMark
    aircraftType: AircraftTypeICAOId
    aircraftIATAId: AircraftIATAId
    arrivalTaxiTime: common.DurationHourMinute
    apiArrivalProcedure: airspace.TerminalProcedure
    nmArrivalProcedure: airspace.TerminalProcedure
    initialApproachFix: airspace.PublishedPointId
    arrivalRunway: airspace.RunwayId
    arrivalTerminal: TerminalOrApronStandName
    arrivalApronStand: TerminalOrApronStandName
    minimumTurnaroundTime: common.DurationHourMinute
    landingTime: common.DateTimeMinute
    scheduledInBlockTime: common.DateTimeMinute
    inBlockTime: common.DateTimeMinute
    airportSlotArrival: common.DateTimeMinute
    impactSeverityIndicator: ImpactSeverityIndicator
    coordinationFix: airspace.AerodromeOrPublishedPointId
    targetTimeOver: common.DateTimeMinute
    earliestTargetTimeOver: common.DateTimeMinute
    consolidatedTargetTimeOver: common.DateTimeMinute
    calculatedTimeOver: common.DateTimeMinute
    regulationId: flow.RegulationId
    minCalculatedTimeOver: common.DateTimeMinute
    maxCalculatedTimeOver: common.DateTimeMinute
    estimatedOrActualTimeOver: common.DateTimeMinute


ProposalKind = Literal["SIP", "RVR", "RRP", "STAM_SLOT", "DELAY_CONF"]

StandardRouteId = TypedDict(
    "StandardRouteId",
    {
        "from": "airspace.AerodromeICAOId",
        "to": "airspace.AerodromeICAOId",
        "seqNr": "str",
    },
    total=False,
)

ReroutingRouteType = Literal["GENERATED", "STANDARD", "USER", "VERTICAL"]


class ReroutingRouteId(TypedDict, total=False):
    routeType: ReroutingRouteType
    standardRouteId: StandardRouteId


class ProposalInformation(TypedDict, total=False):
    proposalKind: ProposalKind
    responseBy: common.DateTimeMinute
    proposedCTOT: common.DateTimeMinute
    routeId: ReroutingRouteId
    deltaCost: common.Cost
    deltaDelay: common.SignedDurationHourMinuteSecond
    reroutingId: flow.ReroutingId


TrafficType = Literal["DEMAND", "REGULATED_DEMAND", "LOAD"]


class TimeAndModel(TypedDict, total=False):
    model: TrafficType
    dateTime: common.DateTimeSecond


class SlotSwapCounter(TypedDict, total=False):
    currentCounter: str
    maxLimit: str


EntryExit = Literal["ENTRY", "EXIT"]


class FlightRestriction(TypedDict, total=False):
    timeOver: common.DateTimeSecond
    coveredDistance: common.DistanceNM
    flightPlanProcessing: airspace.FlightPlanProcessing
    restrictionId: airspace.RestrictionId
    event: EntryExit
    position: common.Position
    flightLevel: airspace.FlightLevel


class FlightTrafficVolume(TypedDict, total=False):
    trafficVolumeId: airspace.TrafficVolumeId
    entryTime: common.DateTimeSecond
    entryFlightLevel: airspace.FlightLevel
    entryTrend: FlightTrend
    middleTrend: FlightTrend
    exitTime: common.DateTimeSecond
    exitFlightLevel: airspace.FlightLevel
    exitTrend: FlightTrend
    activated: Literal["true", "false"]
    exempted: Literal["true", "false"]
    flows: Union[flow.Flow, list[flow.Flow]]


ReroutingFeedbackReason = Literal[
    "TOTAL_COST",
    "FUEL_SAVINGS",
    "ROUTE_CHARGES",
    "ATFM_DELAY_VALUE",
    "DISTANCE",
    "FLYING_TIME",
    "OBT_VALIDITY",
    "AO_INTERNAL_REASONS",
    "OTHER",
]

ReroutingFeedbackKind = Literal["LIKE", "DISLIKE"]


class ReroutingFeedback(TypedDict, total=False):
    kind: ReroutingFeedbackKind
    icaoRoute: str
    reason: ReroutingFeedbackReason
    comment: str
    reroutingId: flow.ReroutingId


IntruderKind = Literal[
    "NON_INTRUDER", "HORIZONTAL_INTRUDER", "VERTICAL_INTRUDER", "MIXED_INTRUDER"
]


class DeltaEntry(TypedDict, total=False):
    intruderKind: IntruderKind
    originOfIntruder: airspace.AirspaceId
    deltaMinutes: str
    deltaFlightLevel: str
    deltaPosition: common.DistanceNM


FAMStatus = Literal[
    "AIRBORNE_WHEN_SUSPENDED_BY_FAM",
    "AIRBORNE_WHEN_SHIFTED_BY_FAM",
    "SUBJECT_TO_FAM",
    "WAS_SUBJECT_TO_FAM",
    "NOT_UNDER_FAM",
    "SHIFTED_BY_FAM",
    "WAS_SHIFTED_BY_FAM",
    "SUSPENDED_BY_FAM",
    "WAS_SUSPENDED_BY_FAM",
]


class Flight(TypedDict, total=False):
    flightId: FlightIdentificationOutput
    divertedAerodromeOfDestination: airspace.AerodromeICAOId
    aircraftType: AircraftTypeICAOId
    readyEstimatedOffBlockTime: common.DateTimeMinute
    cdmEstimatedOffBlockTime: common.DateTimeMinute
    calculatedOffBlockTime: common.DateTimeMinute
    actualOffBlockTime: common.DateTimeMinute
    revisionTimes: RevisionTimes
    estimatedTakeOffTime: common.DateTimeMinute
    calculatedTakeOffTime: common.DateTimeMinute
    actualTakeOffTime: common.DateTimeMinute
    ctotShiftAlreadyAppliedByTower: common.ShiftHourMinute
    requestedFlightLevel: airspace.FlightLevel
    taxiTime: common.DurationHourMinute
    currentDepartureTaxiTimeAndProcedure: TaxiTimeAndProcedure
    estimatedTimeOfArrival: common.DateTimeMinute
    calculatedTimeOfArrival: common.DateTimeMinute
    actualTimeOfArrival: common.DateTimeMinute
    lateFiler: Literal["true", "false"]
    lateUpdater: Literal["true", "false"]
    suspensionStatus: SuspensionStatus
    suspensionInfo: str
    famStatus: FAMStatus
    readyStatus: ReadyStatus
    aircraftOperator: AircraftOperatorICAOId
    operatingAircraftOperator: AircraftOperatorICAOId
    reroutingIndicator: ReroutingIndicator
    newRouteMinShiftDelayImprovement: common.DurationHourMinute
    reroutable: ReroutableStatus
    cdm: CDM
    slotIssued: Literal["true", "false"]
    proposalInformation: ProposalInformation
    bestReroutingIndicator: flow.GroupReroutingSummary
    timeAtReferenceLocationEntry: TimeAndModel
    timeAtReferenceLocationExit: TimeAndModel
    flightLevelAtReferenceLocationEntry: airspace.FlightLevel
    flightLevelAtReferenceLocationExit: airspace.FlightLevel
    trendAtReferenceLocationEntry: FlightTrend
    trendAtReferenceLocationExit: FlightTrend
    trendAtReferenceLocationMiddle: FlightTrend
    exemptedFromRegulations: Literal["true", "false"]
    delay: common.DurationHourMinute
    delayCharacteristics: DelayCharacteristics
    mostPenalisingRegulation: flow.RegulationId
    hasOtherRegulations: Literal["true", "false"]
    regulationLocations: Union[
        flow.FlightRegulationLocation, list[flow.FlightRegulationLocation]
    ]
    atfcmMeasureLocations: Union[
        flow.FlightAtfcmMeasureLocation, list[flow.FlightAtfcmMeasureLocation]
    ]
    lastATFMMessageType: ATFMMessageType
    lastATFMMessageReceivedOrSent: common.ReceivedOrSent
    runwayVisualRange: common.DistanceM
    minimumRequestedRVR: common.DistanceM
    confirmedCTFM: common.DistanceNM
    exclusionFromRegulations: ExclusionFromRegulations
    requestedInitialFlightLevel: airspace.FlightLevel
    requestedInitialSpeed: airspace.AirSpeed
    estimatedElapsedTime: common.DurationHourMinute
    filingRule: FilingRule
    initialFPLMessageOriginator: MessageOriginator
    lastFPLMessageOriginator: MessageOriginator
    icaoRoute: str
    routeLength: common.DistanceNM
    defaultReroutingRequestedFlightLevel: airspace.FlightLevel
    defaultReroutingRequestedSpeed: airspace.AirSpeed
    departureTolerance: DepartureTolerance
    mostPenalisingRegulationCause: flow.RegulationCause
    lastATFMMessageOriginator: MessageOriginator
    ftfmPointProfile: Union[FlightPoint, list[FlightPoint]]
    rtfmPointProfile: Union[FlightPoint, list[FlightPoint]]
    ctfmPointProfile: Union[FlightPoint, list[FlightPoint]]
    ftfmAirspaceProfile: Union[FlightAirspace, list[FlightAirspace]]
    rtfmAirspaceProfile: Union[FlightAirspace, list[FlightAirspace]]
    ctfmAirspaceProfile: Union[FlightAirspace, list[FlightAirspace]]
    ftfmTrafficVolumeProfile: Union[
        FlightTrafficVolume, list[FlightTrafficVolume]
    ]
    rtfmTrafficVolumeProfile: Union[
        FlightTrafficVolume, list[FlightTrafficVolume]
    ]
    ctfmTrafficVolumeProfile: Union[
        FlightTrafficVolume, list[FlightTrafficVolume]
    ]
    ftfmRequestedFlightLevels: Union[
        RequestedFlightLevel, list[RequestedFlightLevel]
    ]
    rtfmRequestedFlightLevels: Union[
        RequestedFlightLevel, list[RequestedFlightLevel]
    ]
    ctfmRequestedFlightLevels: Union[
        RequestedFlightLevel, list[RequestedFlightLevel]
    ]
    flightHistory: Union[FlightEvent, list[FlightEvent]]
    operationalLog: Union[
        FlightOperationalLogEntry, list[FlightOperationalLogEntry]
    ]
    equipmentCapabilityAndStatus: EquipmentCapabilityAndStatus
    ftfmRestrictionProfile: Union[FlightRestriction, list[FlightRestriction]]
    rtfmRestrictionProfile: Union[FlightRestriction, list[FlightRestriction]]
    ctfmRestrictionProfile: Union[FlightRestriction, list[FlightRestriction]]
    cfmuFlightType: CfmuFlightType
    ccamsSSRCode: SSRCode
    filedRegistrationMark: AircraftRegistrationMark
    isProposalFlight: Literal["true", "false"]
    hasBeenForced: Literal["true", "false"]
    caughtInHotspots: str
    hotspots: Union[
        flow.FlightHotspotLocation, list[flow.FlightHotspotLocation]
    ]
    mcdmInfo: flow.FlightMCDMInfo
    worstLoadStateAtReferenceLocation: LoadStateAtReferenceLocation
    compareWithOtherTrafficType: DeltaEntry
    ctotLimitReason: CTOTLimitReason
    profileValidity: ProfileValidity
    targetTimeOverFix: TargetTime
    flightState: FlightState
    lastKnownPosition: FourDPosition
    slotSwapCounter: SlotSwapCounter
    slotSwapCandidateList: Union[SlotSwapCandidate, list[SlotSwapCandidate]]
    aircraftAddress: ICAOAircraftAddress
    arrivalInformation: ArrivalInformation
    slotZone: SlotZone
    flightDataVersionNr: FlightDataVersionNumber
    applicableScenarios: Union[
        flow.TrafficVolumeScenarios, list[flow.TrafficVolumeScenarios]
    ]
    apiSubmissionRules: APISubmissionRules
    avoidedRegulations: Union[flow.RegulationId, list[flow.RegulationId]]
    routeChargeIndicator: str
    fuelConsumptionIndicator: str
    excludedRegulations: Union[flow.RegulationId, list[flow.RegulationId]]
    yoyoFlightForLocation: YoYoFlightForLocation
    turnFlightForLocation: TurnFlightForLocation
    wakeTurbulenceCategory: WakeTurbulenceCategory
    alternateAerodromes: Union[
        airspace.AerodromeICAOId, list[airspace.AerodromeICAOId]
    ]
    flightCriticality: FlightCriticalityIndicator
    oceanicReroute: Literal["true", "false"]
    visibility: FlightVisibility
    iataFlightDesignator: AircraftIATAIdFromDataSource
    activeACDMAlerts: Union[ACDMAlertData, list[ACDMAlertData]]
    aoReroutingFeedbacks: Union[ReroutingFeedback, list[ReroutingFeedback]]


class Relative4DPoint(TypedDict, total=False):
    cumulativeDistance: common.DistanceM
    altitude: common.FlightLevelM
    elapsedTime: common.Duration


class PointDAL(TypedDict, total=False):
    point: airspace.ICAOPoint
    cumulativeDistance: common.DistanceM


class AerodromeDAL(TypedDict, total=False):
    aerodrome: airspace.AerodromeICAOId
    cumulativeDistance: common.DistanceM


class DistanceAtLocation(TypedDict, total=False):
    adesDAL: AerodromeDAL
    dalPoints: Union[PointDAL, list[PointDAL]]


class BasicTrajectoryData(TypedDict, total=False):
    takeOffWeight: common.WeightKg
    topOfClimb: Union[Relative4DPoint, list[Relative4DPoint]]
    topOfDescent: Union[Relative4DPoint, list[Relative4DPoint]]
    bottomOfClimb: Union[Relative4DPoint, list[Relative4DPoint]]
    bottomOfDescent: Union[Relative4DPoint, list[Relative4DPoint]]
    distanceAtLocationInfo: DistanceAtLocation


class DepartureData(TypedDict, total=False):
    taxiTime: common.DurationMinute


AlternateAerodrome_DataType = str


class ModeSCapabilities(TypedDict, total=False):
    aircraftIdentification: EquipmentStatus
    pressureAltitude: EquipmentStatus
    extendedSquitterADSB: EquipmentStatus
    enhancedSurveillance: EquipmentStatus


class SurveillanceEquipment(TypedDict, total=False):
    modeA: EquipmentStatus
    modeAAndC: EquipmentStatus
    modeS: EquipmentStatus
    modeSCapabilities: ModeSCapabilities
    adsb1900Out: EquipmentStatus
    adsb1900OutIn: EquipmentStatus
    adsbOutUAT: EquipmentStatus
    adsbOutInUAT: EquipmentStatus
    adsbOutVDL4: EquipmentStatus
    adsbOutInVDL4: EquipmentStatus
    adscFans: EquipmentStatus
    adscAtn: EquipmentStatus


AirportSlot = str


class EstimatedElapsedTimeAtLocation(TypedDict, total=False):
    elapsedTime: common.DurationHourMinute
    fir: airspace.FIRICAOId
    point: airspace.ICAOPoint
    latitude: common.Latitude
    longitude: common.Longitude


class FlightPlanOriginator(TypedDict, total=False):
    address: str
    phone: str
    otherInformation: str


DataLinkCapabilities_DataType = str


class DatalinkCapabilities(TypedDict, total=False):
    value: DataLinkCapabilities_DataType


SelectiveCallingCode = str


class ReclearanceInFlight(TypedDict, total=False):
    icaoRoute: str
    aerodrome: airspace.AerodromeICAOId


EURSTSIndicator = Literal["EXM833", "PROTECTED", "RNAVX", "RNAVINOP", "CPDLCX"]

ICAOSTSIndicator = Literal[
    "ALTRV",
    "ATFMX",
    "FFR",
    "FLTCK",
    "HAZMAT",
    "HEAD",
    "HOSP",
    "HUM",
    "MARSA",
    "MEDEVAC",
    "NONRVSM",
    "SAR",
    "STATE",
]


class SpecialHandlingIndicators(TypedDict, total=False):
    icaoSTSIndicators: Union[ICAOSTSIndicator, list[ICAOSTSIndicator]]
    eurSTSIndicators: Union[EURSTSIndicator, list[EURSTSIndicator]]


AircraftOperatorName_DataType = str

AircraftPerformanceCategory = Literal[
    "CAT_A", "CAT_B", "CAT_C", "CAT_D", "CAT_E", "CAT_H"
]

PerformanceBasedNavigationCode = Literal[
    "RNAV_10",
    "RNAV_5_ALL",
    "RNAV_5_GNSS",
    "RNAV_5_DME_DME",
    "RNAV_5_VOR_DME",
    "RNAV_5_INS_OR_IRS",
    "RNAV_5_LORAN_C",
    "RNAV_2_ALL",
    "RNAV_2_GNSS",
    "RNAV_2_DME_DME",
    "RNAV_2_DME_DME_IRU",
    "RNAV_1_ALL",
    "RNAV_1_GNSS",
    "RNAV_1_DME_DME",
    "RNAV_1_DME_DME_IRU",
    "RNP_4",
    "BASIC_RNP_1_ALL",
    "BASIC_RNP_1_GNSS",
    "BASIC_RNP_1_DME_DME",
    "BASIC_RNP_1_DME_DME_IRU",
    "RNP_APCH",
    "RNP_APCH_BARO_VNAV",
    "RNP_AR_APCH_RF",
    "RNP_AR_APCH_NO_RF",
]


class OtherInformation(TypedDict, total=False):
    selCalCode: SelectiveCallingCode
    nameOfOperator: AircraftOperatorName_DataType
    reasonForSpecialHandling: SpecialHandlingIndicators
    aircraftPerformanceData: AircraftPerformanceCategory
    communicationEquipment: str
    datalinkCapabilities: DatalinkCapabilities
    navigationEquipment: str
    performanceBasedNavigationCodes: Union[
        PerformanceBasedNavigationCode, list[PerformanceBasedNavigationCode]
    ]
    otherSurveillanceEquipments: str
    replacementFlightPlanIndicator: str
    runwayVisualRange: common.DistanceM
    reclearanceInFlight: ReclearanceInFlight
    otherRemarks: str


StayInformation_DataType = str

SSRMode = Literal["A"]


class SSRInfo(TypedDict, total=False):
    code: SSRCode
    mode: SSRMode


class AircraftIdentification(TypedDict, total=False):
    aircraftId: AircraftICAOId
    registrationMark: AircraftRegistrationMark
    aircraftAddress: ICAOAircraftAddress
    ssrInfo: SSRInfo


NumberOfDinghies_DataType = str

TotalCapacity_DataType = str


class Dinghies(TypedDict, total=False):
    numberOfDinghies: NumberOfDinghies_DataType
    totalCapacity: TotalCapacity_DataType
    areCovered: Literal["true", "false"]
    colours: common.Colours


FrequencyOnAircraft = Literal["UHF", "VHF", "ELT"]

LifeJacketEquipment = Literal["LIGHTS", "FLUORESCEIN", "UHF", "VHF"]

SurvivalEquipment = Literal["POLAR", "DESERT", "MARITIME", "JUNGLE"]


class SupplementaryInformation(TypedDict, total=False):
    fuelEndurance: common.DurationHourMinute
    numberOfPersons: str
    frequencyAvailability: Union[FrequencyOnAircraft, list[FrequencyOnAircraft]]
    survivalEquipment: Union[SurvivalEquipment, list[SurvivalEquipment]]
    otherSurvivalEquipment: str
    lifeJacketEquipment: Union[LifeJacketEquipment, list[LifeJacketEquipment]]
    dinghiesInformation: Dinghies
    aircraftColourAndMarkings: str
    pilotInCommand: str


AtsUnitId_DataType = str


class AirFiledData(TypedDict, total=False):
    atsUnitId: AtsUnitId_DataType
    startingPoint: airspace.ICAOPoint
    clearedLevel: airspace.FlightLevel
    estimatedTimeOver: common.DateTimeSecond


AerodromeName_DataType = str


class OtherAerodromeDesignation(TypedDict, total=False):
    aerodromeName: AerodromeName_DataType
    aerodromeLocation: airspace.NonPublishedPoint
    firstLastRoutePoint: airspace.ICAOPoint


class Aerodrome(TypedDict, total=False):
    icaoId: airspace.AerodromeICAOId
    otherDesignation: OtherAerodromeDesignation


FlightType = Literal[
    "SCHEDULED", "NOT_SCHEDULED", "GENERAL", "MILITARY", "OTHER"
]

AerodromeNameLocationDescription_DataType = str


class AlternateAerodrome(TypedDict, total=False):
    icaoId: airspace.AerodromeICAOId
    nameLocationDescription: AerodromeNameLocationDescription_DataType


class AerodromesOfDestination(TypedDict, total=False):
    aerodromeOfDestination: Aerodrome
    alternate1: AlternateAerodrome
    alternate2: AlternateAerodrome


class EnrouteDelay(TypedDict, total=False):
    delay: common.DurationHourMinute
    point: airspace.ICAOPoint


FlightRules = Literal["VFR_THEN_IFR", "IFR_THEN_VFR", "VFR", "IFR"]


class FlightPlan(TypedDict, total=False):
    ifplId: IFPLId
    airFiledData: AirFiledData
    aerodromeOfDeparture: Aerodrome
    aerodromesOfDestination: AerodromesOfDestination
    enrouteAlternateAerodromes: AlternateAerodrome_DataType
    takeOffAlternateAerodromes: AlternateAerodrome_DataType
    aircraftId: AircraftIdentification
    whatIfRerouteReference: str
    numberOfAircraft: str
    aircraftType: AircraftType
    totalEstimatedElapsedTime: common.DurationHourMinute
    eetsToLocations: Union[
        EstimatedElapsedTimeAtLocation, list[EstimatedElapsedTimeAtLocation]
    ]
    wakeTurbulenceCategory: WakeTurbulenceCategory
    flightType: FlightType
    flightRules: FlightRules
    estimatedOffBlockTime: common.DateTimeMinute
    icaoRoute: str
    stayInformation: Union[
        StayInformation_DataType, list[StayInformation_DataType]
    ]
    enrouteDelays: Union[EnrouteDelay, list[EnrouteDelay]]
    equipmentCapabilityAndStatus: EquipmentCapabilityAndStatus
    surveillanceEquipment: SurveillanceEquipment
    otherInformation: OtherInformation
    supplementaryInformation: SupplementaryInformation
    iataFlightNumber: AircraftIATAId
    arrivalAirportSlot: AirportSlot
    departureAirportSlot: AirportSlot
    flightPlanOriginator: FlightPlanOriginator


class StructuredFlightPlan(TypedDict, total=False):
    flightPlan: FlightPlan
    basicTrajectoryData: BasicTrajectoryData
    departureData: DepartureData


class FlightPlanHistoryInfo(TypedDict, total=False):
    timeStamp: common.DateTimeSecond
    checkPoint: str
    mode: str
    msgIn: str
    msgOut: str
    addresses: str
    detail: str


class FlightPlanHistory(TypedDict, total=False):
    infos: Union[FlightPlanHistoryInfo, list[FlightPlanHistoryInfo]]


class FlightRetrievalReplyData(TypedDict, total=False):
    structuredFlightPlan: StructuredFlightPlan
    flightPlanHistory: FlightPlanHistory
    flight: Flight


class FlightRetrievalReply(common.Reply):
    data: FlightRetrievalReplyData
