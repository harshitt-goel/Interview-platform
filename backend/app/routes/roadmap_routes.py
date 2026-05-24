from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import json

from app.database.dependencies import get_db
from app.utils.current_user import get_current_user

from app.models.profile_model import Profile
from app.models.roadmap_model import Roadmap

router = APIRouter()

@router.post("/generate-roadmap")
def generate_roadmap(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).order_by(Profile.id.desc()).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    print("==== PROFILE FETCHED ====")
    print(profile.target_role)

    role = profile.target_role.strip().lower()

    print("==== NORMALIZED ROLE ====")
    print(role)

    if role == "backend developer":

        with open(
            "app/roadmaps/backend_developer.json",
            "r"
        ) as file:

            roadmap_json = json.load(file)

    else:

        print("==== ROLE DID NOT MATCH ====")
        print(role)

        raise HTTPException(
            status_code=400,
            detail=f"Roadmap not available for role: {role}"
        )

    new_roadmap = Roadmap(
        user_id=current_user.id,
        role=profile.target_role,
        roadmap_data=json.dumps(roadmap_json)
    )

    db.add(new_roadmap)
    db.commit()

    return roadmap_json