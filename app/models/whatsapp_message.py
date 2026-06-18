from sqlalchemy import (
Column,
Integer,
String,
DateTime
)

from sqlalchemy.sql import (
func
)

from app.db.database import (
Base
)

class WhatsAppMessage(Base):

    __tablename__ = (
        "whatsapp_messages"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    message_id = Column(
        String(255),
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

