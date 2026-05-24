from pydantic import BaseModel, HttpUrl

class ProfileCreate(BaseModel):

    target_role: str
    domain: str
    current_level: str

    github_url: str
    leetcode_url: str
    codeforces_url: str

    target_company: str