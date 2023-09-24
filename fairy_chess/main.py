import flet

# from fairy_chess.views import ViewStack
from fairy_chess.views import web_view
from fairy_chess.models import psql_db
from fairy_chess.models.user import UserModel

psql_db.connect()
psql_db.create_tables([UserModel])

# def main(page: flet.Page):
#     ViewStack(page)

flet.app(target=web_view, view=flet.WEB_BROWSER)