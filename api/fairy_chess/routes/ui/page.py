from __future__ import annotations as _annotations

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent

class FairyChessPage:
    def __init__(self, *components: list[AnyComponent], title: str, user_riot_id: str | None,) -> None:
        self.title = title
        self.components = components
        self.user_riot_id = user_riot_id

    def navbar(self) -> list[AnyComponent]:
        profile = c.Link(
            components=[c.Button(text='Profile')],
            on_click=GoToEvent(url='/ui/user/profile'),
            active='startswith:/ui/user/profile',
        )
        login = c.Link(
            components=[c.Button(text='Login')],
            on_click=GoToEvent(url='/ui/user/auth'),
        )
        logout = c.Link(
            components=[c.Button(text='Logout')],
            on_click=GoToEvent(url='/ui/user/logout'),
        )
        navbar_links = [
            c.Link(
                components=[c.Text(text='Contests')],
                on_click=GoToEvent(url='/ui/contest/'),
                active='startswith:/ui/contest',
            ),
            c.Link(
                components=[c.Text(text='Rules')],
                on_click=GoToEvent(url='/rules'),
                active='startswith:/rules',
            ),
            c.Link(
                components=[c.Text(text='About')],
                on_click=GoToEvent(url='/about'),
                active='startswith:/about',
            ),
        ]
        return c.Navbar(
            title='Fairy Chess',
            title_event=GoToEvent(url='/'),
            start_links=navbar_links,
            end_links=[profile, logout] if self.user_riot_id else [login]
        )

    def footer(self) -> list[AnyComponent]:
        return c.Footer(
            extra_text='TFT Tournments',
            links=[
                c.Link(components=[c.Image(
                    src='https://i.ibb.co/PrZW1zm/fairychess-logo-v0-1.png',
                    alt='Pydantic Logo',
                    width=75,
                    height=75,
                    loading='lazy',
                    referrer_policy='no-referrer',
                ),], on_click=GoToEvent(url='https://github.com/ratopythonista/fairy-chess/tree/dev'))
            ]
        )

    def render(self) -> list[AnyComponent]:
        return [   
            c.PageTitle(text=f'Fairy Chess — {self.title}'),
            self.navbar(),
            c.Page(
                components=[
                    *(c.Heading(text=self.title),),
                    *self.components,
                ],
            ),
            self.footer(),
        ]