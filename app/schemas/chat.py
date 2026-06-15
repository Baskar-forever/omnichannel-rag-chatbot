from pydantic import BaseModel


class SourceResponse(
    BaseModel
):

    title: str

    url: str


class ChatRequest(
    BaseModel
):

    session_id: int

    message: str


class ChatResponse(
    BaseModel
):

    reply: str

    state: str

    sources: list[SourceResponse] = []