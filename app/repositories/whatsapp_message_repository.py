from app.models.whatsapp_message import WhatsAppMessage

class WhatsAppMessageRepository:

    
    def exists(
        self,
        db,
        message_id: str
    ):

        return (
            db.query(
                WhatsAppMessage
            )
            .filter(
                WhatsAppMessage.message_id
                == message_id
            )
            .first()
            is not None
        )

    def create(
        self,
        db,
        message_id: str
    ):

        item = (
            WhatsAppMessage(
                message_id=
                    message_id
            )
        )

        db.add(
            item
        )

        db.commit()

        db.refresh(
            item
        )

        return item
    
