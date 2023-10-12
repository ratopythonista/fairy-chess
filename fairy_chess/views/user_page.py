from flet import Page, Text, Column, Image, ImageFit, Row, Container, alignment, colors


class UserPage:
    def __init__(self, page: Page):
        self.page = page          


        self.logo = Image(
            src="https://i.ibb.co/bbBSyLC/fairychess-logo-v0.png",
            width=100,
            height=100,
            fit=ImageFit.CONTAIN,
        )
        
        self.row = Row(controls=[
            Container(
                content = Image(
                    src=self.page.session.get("icon"),
                    width=100,
                    height=100,
                    fit=ImageFit.CONTAIN,
                ),
                margin=10,
                padding=10,
                alignment=alignment.center,
                bgcolor=colors.BLUE_GREY_100,
                width=150,
                height=150,
                border_radius=10,
            ),
            Container(
                content = Text(self.page.session.get("summoner")),
                margin=10,
                padding=10,
                alignment=alignment.center,
                bgcolor=colors.BLUE_GREY_100,
                width=150,
                height=150,
                border_radius=10,
            ),
            Container(
                content = Text("Validar!" if not self.page.session.get("validated") else "MEU ELO"),
                margin=10,
                padding=10,
                alignment=alignment.center,
                bgcolor=colors.BLUE_GREY_100,
                width=150,
                height=150,
                border_radius=10,
            ),
        ])
        self.page.add(Column(controls=[self.logo, self.row]))     