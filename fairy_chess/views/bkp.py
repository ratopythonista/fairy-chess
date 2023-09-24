from flet import Page, View
from loguru import logger

from fairy_chess.views.login import LoginPage
from fairy_chess.views.registration import RegistrationPage

class ViewStack:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.title = "Fairy Chess - TFT Tournment - Registration"
        self.page.padding = 0

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        logger.debug(self.page.route)
        self.page.go(self.page.route)

    def route_change(self, route: str):
        self.page.views.clear()
        self.page.views.append(View("/", [LoginPage(self.page)]))
        if self.page.route == "/registration":
            self.page.views.append(View("/registration", [RegistrationPage(self.page)]))
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        
