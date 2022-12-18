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
                        dbc.Label("Email", html_for="email", width=2),
                        dbc.Col(dbc.Input(type="email", id="email"), width=10),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Password", html_for="password", width=2),
                        dbc.Col(dbc.Input(type="password", id="password",), width=10),
                    ],
                    
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Button("Entrar", id="login", color="success")),
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
        dbc.Row([dbc.Col(html.Div(main_card)), html.Div(id='message')],
        justify="center",
    ),
    style={"margin": "2rem 20rem"}
)