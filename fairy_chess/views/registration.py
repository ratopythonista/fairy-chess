from flet import Page, TextField, ElevatedButton, Column, Image, ImageFit

from fairy_chess.controllers.user import UserController


class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page          

        self.logo = Image(
            src="https://i.ibb.co/bbBSyLC/fairychess-logo-v0.png",
            width=100,
            height=100,
            fit=ImageFit.CONTAIN,
        )
        self.username = TextField(label="Username")
        self.email = TextField(label="Email")
        self.password = TextField(label="Password", password=True, can_reveal_password=True)
        self.summoner_name = TextField(label="Summoner Name")
        self.submit_button = ElevatedButton(text="Registrar", on_click=self.submit_registration)

        self.page.add(Column(controls=[self.logo, self.username, self.email, self.password, self.summoner_name, self.submit_button]))     
                 
    def submit_registration(self, e):
        UserController.register(self.username.value, self.email.value, self.password.value, self.summoner_name.value)
        self.page.route = "/login"
        self.page.update()