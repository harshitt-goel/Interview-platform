from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database.db import Base

class Profile(Base):

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    target_role = Column(String)

    domain = Column(String)

    current_level = Column(String)

    github_url = Column(String)

    leetcode_url = Column(String)

    codeforces_url = Column(String)

    target_company = Column(String)