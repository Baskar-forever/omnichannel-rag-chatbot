from app.models.chat_session import ChatSession


class SessionRepository:

    def create(self, db):

        session = ChatSession()

        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    def get_by_id(self, db, session_id: int):

        return (
            db.query(ChatSession)
            .filter(
                ChatSession.id == session_id
            )
            .first()
        )

    def update_state(
        self,
        db,
        session: ChatSession,
        state: str
    ):

        session.state = state

        db.commit()
        db.refresh(session)

        return session

    def update_pending_data(
        self,
        db,
        session,
        pending_data
    ):

        session.pending_data = dict(
            pending_data
        )

        db.commit()
        db.refresh(session)

        return session

    def attach_lead(
        self,
        db,
        session: ChatSession,
        lead_id: int
    ):

        session.lead_id = lead_id

        db.commit()
        db.refresh(session)

        return session
    
    def get_by_phone_number(
        self,
        db,
        phone_number: str
    ):

        return (
            db.query(ChatSession)
            .filter(
                ChatSession.phone_number
                == phone_number
            )
            .first()
        )
    
    def create_whatsapp_session(
        self,
        db,
        phone_number: str
    ):

        session = ChatSession(
            phone_number=phone_number,
            state="ASK_NAME"
        )

        db.add(session)

        db.commit()

        db.refresh(session)

        return session