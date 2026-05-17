from sqlalchemy import Column, Integer, Text, ForeignKey
from app.database.db import Base

class Resume(Base):

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    extracted_text = Column(Text)