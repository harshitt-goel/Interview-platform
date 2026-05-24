from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.utils.current_user import get_current_user

from app.models.profile_model import Profile
from app.schemas.profile_schema import ProfileCreate

router = APIRouter()

@router.post("/create-profile")
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    new_profile = Profile(
        user_id=current_user.id,

        target_role=profile.target_role,
        domain=profile.domain,
        current_level=profile.current_level,

        github_url=profile.github_url,
        leetcode_url=profile.leetcode_url,
        codeforces_url=profile.codeforces_url,

        target_company=profile.target_company
    )

    db.add(new_profile)
    db.commit()

    return {
        "message": "Profile created successfully"
    }