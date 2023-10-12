from flet import Page, TextField, ElevatedButton, Column, Image, ImageFit

from fairy_chess.controllers.user import UserController


class LoginPage:
    def __init__(self, page: Page):
        self.page = page   

        self.logo = Image(
            src="https://i.ibb.co/bbBSyLC/fairychess-logo-v0.png",
            width=100,
            height=100,
            fit=ImageFit.CONTAIN,
        )
        self.username = TextField(label="Username")
        self.password = TextField(label="Password", password=True, can_reveal_password=True)
        self.login_button = ElevatedButton(text="Entrar", on_click=self.login)
        self.submit_button = ElevatedButton(text="Registrar", on_click=self.go_registration)

        self.page.add(Column(controls=[self.logo, self.username, self.password, self.login_button, self.submit_button]))     

    def go_registration(self, e):
        self.page.route = "/registration"
        self.page.update()

    def login(self, e):    
        if user := UserController.login(self.username.value, self.password.value):
            summoner, validated, icon = user
            self.page.session.set("icon", icon)
            self.page.session.set("summoner", summoner)
            self.page.session.set("validated", validated)
            self.page.route = "/user"
            self.page.update()
        
