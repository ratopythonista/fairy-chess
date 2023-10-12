import flet

from fairy_chess.views import web_view


flet.app(target=web_view, view=flet.WEB_BROWSER, port=8080)