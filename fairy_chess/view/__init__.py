from flet import Page

from fairy_chess.view.registration import RegistrationPage
 
def web_view(page: Page):
    page.title = "Fairy Chess - TFT Tournment - Registration"
    page.padding = 0
    RegistrationPage(page)
    page.update()
