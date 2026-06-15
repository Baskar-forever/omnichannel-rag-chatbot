from app.models.message import Message


class MessageRepository:

    def create(
        self,
        db,
        session_id: int,
        role: str,
        content: str
    ):

        message = Message(
            session_id=session_id,
            role=role,
            content=content
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return message

    def get_by_session(
        self,
        db,
        session_id: int
    ):

        return (
            db.query(Message)
            .filter(
                Message.session_id == session_id
            )
            .order_by(
                Message.created_at.asc()
            )
            .all()
        )