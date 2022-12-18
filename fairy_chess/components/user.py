from dash import html
import dash_bootstrap_components as dbc

from fairy_chess.services.riot import Riot

login_bar = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Button("Entrar", id="login", href="login", color="success"), width="auto"),
                dbc.Col(dbc.Button("Cadastrar", id="register", href="/register", color="secondary"), width="auto"),
            ]
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)


def build_user_bar(user_info: dict):
    summoner_info: dict = user_info.get("summoner")
    icon = Riot().get_icon(summoner_info.get("profileIconId"))
    return [
            html.Div(
                html.A(html.Img(src='/assets/logout.svg', height="30px"), id="logout"),
                className="nav-item d-none d-md-flex"
            ),
            html.Div(
                [
                    html.Img(className="avatar avatar-sm", src=icon),
                    html.Div(
                        [html.Div(user_info.get("name")), html.Div(summoner_info.get("name"), className="mt-1 small text-muted")],
                        className="d-none d-xl-block ps-2"
                    )
                ],
                className="nav-link d-flex lh-1 text-reset p-0"
            ),
        ]