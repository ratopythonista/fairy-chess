from flet import Page, RouteChangeEvent

from fairy_chess.views.login import LoginPage
from fairy_chess.views.user_page import UserPage
from fairy_chess.views.registration import RegistrationPage
 
page_mapping = {
    "/login": LoginPage,
    "/registration": RegistrationPage,
    "/user": UserPage
}

def web_view(page: Page):
    page.title = "Fairy Chess - TFT Tournment - Registration"
    page.padding = 0
    LoginPage(page)
    def route_change(e: RouteChangeEvent):
        page.clean()
        page_mapping[e.route](page)

    page.on_route_change = route_change
    page.update()
