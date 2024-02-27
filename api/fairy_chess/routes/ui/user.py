from __future__ import annotations as _annotations

import json
from typing import Annotated

from fastapi import APIRouter, Header
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import AuthEvent, PageEvent
from fastui.forms import fastui_form
from pydantic import BaseModel, EmailStr, Field, SecretStr

from fairy_chess.routes.ui.page import FairyChessPage
from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.user import UserController

from fairy_chess.database.models.user import UserRepository

user_router = APIRouter(prefix="/user", tags=["ui"])

@user_router.get('/auth', response_model=FastUI, response_model_exclude_none=True)
def auth_login_content() -> list[AnyComponent]:
    return FairyChessPage(
            c.ModelForm(model=LoginForm, submit_url='/api/ui/user/login', display_mode='page'),
            title='Login',
            user_riot_id=None,
    ).render()


class LoginForm(BaseModel):
    email: EmailStr = Field(title='Email', description='Entre com seu email')
    password: SecretStr = Field(title='Password', description='Entre com sua senha')


@user_router.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]) -> list[AnyComponent]:
    token = UserController().login(form.email, form.password.get_secret_value())
    return [c.FireEvent(event=AuthEvent(token=token, url='/ui/user/profile'))]


@user_router.get('/profile', response_model=FastUI, response_model_exclude_none=True)
async def profile(authorization: Annotated[str, Header()] = '') -> list[AnyComponent]:
    user_id = decode_token(authorization.split()[1])
    user = UserRepository().find_by_id(user_id)
    return FairyChessPage(
        c.Paragraph(text=f'You are logged in as "{user.email}".'),
        c.Button(text='Logout', on_click=PageEvent(name='submit-form')),
        c.Heading(text='User Data:', level=3),
        c.Text(text=json.dumps(user_id, indent=2)),
        title='Profile',
        user_riot_id=user.riot_id,
    ).render()

@user_router.post('/logout', response_model=FastUI, response_model_exclude_none=True)
async def logout_form_post() -> list[AnyComponent]:
    return [c.FireEvent(event=AuthEvent(token=False, url='/auth/login/password'))]
