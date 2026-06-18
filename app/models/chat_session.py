from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON

from sqlalchemy.sql import func

from app.db.database import Base
from sqlalchemy.ext.mutable import MutableDict


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True)

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=True
    )

    state = Column(
        String(50),
        nullable=False,
        default="ASK_NAME"
    )

    pending_data = Column(
        MutableDict.as_mutable(JSON),
        nullable=False,
        default=dict
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    phone_number = Column(
    String(20),
    nullable=True,
    unique=True
)