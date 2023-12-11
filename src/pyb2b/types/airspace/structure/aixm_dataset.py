from typing import TypedDict

from ...common import Status


class AIRACId(TypedDict):
    airacId: str


class File(TypedDict):
    id: str
    type: str
    releaseTime: str
    fileLength: str


class _Entry(TypedDict):
    updateId: str
    publicationDate: str
    sourceAIRACs: AIRACId | list[AIRACId]
    files: list[File]


class _Data(TypedDict):
    datasetSummaries: list[_Entry]


class _CompleteAIXMDatasetReply(TypedDict):
    requestReceptionTime: str
    requestId: str
    sendTime: str
    status: Status
    data: _Data


CompleteAIXMDatasetReply = TypedDict(
    "CompleteAIXMDatasetReply",
    {"as:CompleteAIXMDatasetReply": _CompleteAIXMDatasetReply},
)
