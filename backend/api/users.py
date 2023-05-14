from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Mapping
from backend.core.security import create_access_token, verify_password
from backend.models.questionnaire import User
from backend.core.database import Session, get_session

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Mapping[str, str]:
    user = session.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    user.access_token = access_token
    session.add(user)
    session.commit()
    return {"access_token": access_token, "token_type": "bearer"}
