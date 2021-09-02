from datetime import timedelta
from typing import Any
from fastapi.responses import HTMLResponse,Response
from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from fastapi.templating import Jinja2Templates
from app.core import read_json
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from .Repositories import repositories

router = APIRouter()
templates = Jinja2Templates(directory="templates")
words = read_json.ReadJson()
rpos_context = repositories.Rpos()

@router.get("/login", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def login(request: Request):
    """
    response login html page
    :param request: request
    :type request: Request
    :return: HTML template
    :rtype: HTMLResponse
    """
    smaple = rpos_context.get_contex_login()
    smaple.update({"request": request})
    return templates.TemplateResponse(
        "login.html",
        context=smaple
    )

@router.post("/login/access-token", response_model=schemas.Token, response_class=HTMLResponse)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    response access token and id in cookie
    :param db: database object of session local
    :type db: Session
    :param form_data: password of user
    :type form_data: OAuth2PasswordRequestForm
    :return: response contain cookie
    :rtype: HTMLResponse
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    res = Response(status_code=status.HTTP_200_OK)
    res.set_cookie(key="Authorization", value=f'Bearer {security.create_access_token(user.id, expires_delta= access_token_expires)}')
    res.set_cookie(key="id", value=f'{user.id}')
    return res


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token complete later
    :param current_user:
    :return:
    """
    return current_user


