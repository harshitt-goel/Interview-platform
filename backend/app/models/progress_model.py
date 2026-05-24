from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from app.database.db import Base

class Progress(Base):

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    role = Column(String)

    task_name = Column(String)

    completed = Column(Boolean, default=False)