from app.utils.validators import (
    is_valid_name,
    is_valid_email,
    is_valid_phone
)


class ChatService:

    def __init__(
        self,
        rag_service,
        session_repository,
        lead_repository,
        message_repository
    ):

        self.rag_service = rag_service

        self.session_repository = (
            session_repository
        )

        self.lead_repository = (
            lead_repository
        )

        self.message_repository = (
            message_repository
        )

    def create_session(self, db):

        session = (
            self.session_repository.create(
                db
            )
        )

        reply = (
            "Welcome to ZenFuture Technologies. "
            "May I know your name?"
        )

        self.message_repository.create(
            db=db,
            session_id=session.id,
            role="assistant",
            content=reply
        )

        return {
            "session_id": session.id,
            "reply": reply,
            "state": session.state
        }

    def process_message(
        self,
        db,
        session_id: int,
        message: str
    ):

        session = (
            self.session_repository.get_by_id(
                db,
                session_id
            )
        )

        if not session:

            raise ValueError(
                "Invalid session"
            )

        self.message_repository.create(
            db=db,
            session_id=session.id,
            role="user",
            content=message
        )

        pending_data = dict(
            session.pending_data or {}
        )

        # ==================================================
        # ASK_NAME
        # ==================================================

        if session.state == "ASK_NAME":

            if not is_valid_name(message):

                reply = (
                    "Please enter a valid name."
                )

                self.message_repository.create(
                    db=db,
                    session_id=session.id,
                    role="assistant",
                    content=reply
                )

                return {
                    "reply": reply,
                    "state": "ASK_NAME"
                }

            pending_data["name"] = message

            self.session_repository.update_pending_data(
                db,
                session,
                pending_data
            )

            self.session_repository.update_state(
                db,
                session,
                "ASK_EMAIL"
            )

            reply = (
                "Please provide your email address."
            )

            self.message_repository.create(
                db=db,
                session_id=session.id,
                role="assistant",
                content=reply
            )

            return {
                "reply": reply,
                "state": "ASK_EMAIL"
            }

        # ==================================================
        # ASK_EMAIL
        # ==================================================

        if session.state == "ASK_EMAIL":

            if not is_valid_email(message):

                reply = (
                    "Please enter a valid email address."
                )

                self.message_repository.create(
                    db=db,
                    session_id=session.id,
                    role="assistant",
                    content=reply
                )

                return {
                    "reply": reply,
                    "state": "ASK_EMAIL"
                }

            pending_data["email"] = message

            self.session_repository.update_pending_data(
                db,
                session,
                pending_data
            )

            self.session_repository.update_state(
                db,
                session,
                "ASK_PHONE"
            )

            reply = (
                "Please provide your phone number."
            )

            self.message_repository.create(
                db=db,
                session_id=session.id,
                role="assistant",
                content=reply
            )

            return {
                "reply": reply,
                "state": "ASK_PHONE"
            }

        # ==================================================
        # ASK_PHONE
        # ==================================================

        if session.state == "ASK_PHONE":

            if not is_valid_phone(message):

                reply = (
                    "Please enter a valid phone number."
                )

                self.message_repository.create(
                    db=db,
                    session_id=session.id,
                    role="assistant",
                    content=reply
                )

                return {
                    "reply": reply,
                    "state": "ASK_PHONE"
                }

            pending_data["phone"] = message

            self.session_repository.update_pending_data(
                db,
                session,
                pending_data
            )

            lead = (
                self.lead_repository.create(
                    db=db,
                    name=pending_data["name"],
                    email=pending_data["email"],
                    phone=pending_data["phone"],
                    source="website"
                )
            )

            self.session_repository.attach_lead(
                db,
                session,
                lead.id
            )

            self.session_repository.update_pending_data(
                db,
                session,
                {}
            )

            self.session_repository.update_state(
                db,
                session,
                "READY"
            )

            reply = (
                "Thank you. Your details have been recorded. "
                "How can I help you today?"
            )

            self.message_repository.create(
                db=db,
                session_id=session.id,
                role="assistant",
                content=reply
            )

            return {
                "reply": reply,
                "state": "READY"
            }

        # ==================================================
        # READY
        # ==================================================

        if session.state == "READY":

            rag_response = (
                self.rag_service.ask(
                    question=message
                )
            )

            answer = (
                rag_response["answer"]
            )

            self.message_repository.create(
                db=db,
                session_id=session.id,
                role="assistant",
                content=answer
            )

            sources = []

            seen_urls = set()

            for chunk in rag_response["sources"]:

                url = chunk.get(
                    "url"
                )

                if not url:
                    continue

                if url in seen_urls:
                    continue

                seen_urls.add(
                    url
                )

                sources.append(
                    {
                        "title": chunk.get(
                            "title",
                            ""
                        ),
                        "url": url
                    }
                )

            return {
                "reply": answer,
                "state": "READY",
                "sources": sources
            }

        raise ValueError(
            f"Unknown state: {session.state}"
        )
    def stream_message(
        self,
        db,
        session_id: int,
        message: str
    ):

        session = (
            self.session_repository
            .get_by_id(
                db,
                session_id
            )
        )

        if not session:

            yield "Invalid session"

            return

        self.message_repository.create(
            db=db,
            session_id=session.id,
            role="user",
            content=message
        )

        if session.state != "READY":

            yield (
                "Streaming is available "
                "only after lead collection."
            )

            return

        answer_parts = []

        for token in (
            self.rag_service
            .stream_ask(
                question=message
            )
        ):

            answer_parts.append(
                token
            )

            yield token

        full_answer = "".join(
            answer_parts
        )

        self.message_repository.create(
            db=db,
            session_id=session.id,
            role="assistant",
            content=full_answer
        )
    def get_history(
        self,
        db,
        session_id: int
    ):

        messages = (
            self.message_repository
            .get_by_session(
                db,
                session_id
            )
        )

        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in messages
        ]
    
    def clear_history(
        self,
        db,
        session_id: int
    ):

        session = (
            self.session_repository
            .get_by_id(
                db,
                session_id
            )
        )

        if not session:

            raise ValueError(
                "Invalid session"
            )

        self.message_repository.delete_by_session(
            db,
            session_id
        )

        return {
            "success": True
        }