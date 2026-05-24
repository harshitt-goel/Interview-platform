from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)

from app.database.db import Base

class Roadmap(Base):

    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    role = Column(String)

    roadmap_data = Column(Text)