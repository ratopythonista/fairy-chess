from flet import Page

from fairy_chess.views.registration import RegistrationPage
 
def web_view(page: Page):
    page.title = "Fairy Chess - TFT Tournment - Registration"
    page.padding = 0
    RegistrationPage(page)
    page.update()
