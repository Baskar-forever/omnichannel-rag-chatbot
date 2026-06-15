from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_chat_service
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.schemas.session import (
    SessionResponse
)
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)


@router.post(
    "/session",
    response_model=SessionResponse
)
def create_session(
    db: Session = Depends(get_db),
    chat_service=Depends(
        get_chat_service
    )
):

    return (
        chat_service.create_session(
            db
        )
    )


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    chat_service=Depends(
        get_chat_service
    )
):

    try:

        return (
            chat_service.process_message(
                db=db,
                session_id=request.session_id,
                message=request.message
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
@router.post(
    "/chat/stream"
)
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    chat_service=Depends(
        get_chat_service
    )
):

    return StreamingResponse(
        chat_service.stream_message(
            db=db,
            session_id=request.session_id,
            message=request.message
        ),
        media_type="text/plain"
    )