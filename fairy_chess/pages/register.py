import dash
from dash import html, Input, Output
import dash_bootstrap_components as dbc



dash.register_page(__name__)

main_card = dbc.Card(
    [
        dbc.CardHeader("Login - Fairy Chess"),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Label("Nome", html_for="name", width=2),
                        dbc.Col(dbc.Input(type="text", id="name"), width=10),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Summoner", html_for="summoner", width=2),
                        dbc.Col(dbc.Input(type="text", id="summoner"), width=10),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Email", html_for="new-email", width=2),
                        dbc.Col(dbc.Input(type="email", id="new-email"), width=10),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Password", html_for="new-password", width=2),
                        dbc.Col(dbc.Input(type="password", id="new-password",), width=10),
                    ],
                    
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Button("Cadastrar", id="register", color="success")),
                    ], 
                    justify="center"
                ),
            ]
        ),
        html.Div(id='message')
        
    ],
    class_name="text-center"
)


layout = html.Div(
        dbc.Row([dbc.Col(html.Div(main_card)), html.Div(id='register-message')],
        justify="center",
    ),
    style={"margin": "2rem 20rem"}
)