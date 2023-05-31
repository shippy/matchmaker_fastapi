from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import os
from typing import Mapping, Union
from app.core.security import create_access_token, verify_password
from app.models.questionnaire import User, UserBase
from app.core.database import Session, get_session

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


@router.post("/oauth/google")
async def login_with_google(
    jwt_info: Mapping[str, Union[str, int]],
    session = Depends(get_session),
) -> Mapping[str, str]:
    user = session.query(User).filter(User.email == jwt_info["email"]).first()
    if not user:
        user = UserBase(
            email=jwt_info["email"],
            name=jwt_info["name"],
        )
        session.add(user)
        session.commit()