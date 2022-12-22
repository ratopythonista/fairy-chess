
from datetime import datetime
from uuid import UUID, uuid4
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    email = Optional(str)
    name = Required(str)
    password = Required(str)
    summoner = Required('Summoner')


class Summoner(db.Entity):
    id = PrimaryKey(str, 78)
    summoner_id = Required(str, 63)
    account_id = Required(str, 56)
    user = Optional(User)
    summoner_matchs = Set('SummonerMatch')
    name = Required(str)
    profile_icon = Required(int)
    revision_date = Required(datetime)


class Match(db.Entity):
    id = PrimaryKey(str, 26, auto=True)
    schedule_time = Required(datetime)
    end_time = Optional(datetime)
    summoner_matchs = Set('SummonerMatch')
    lobby = Required('Lobby')


class SummonerMatch(db.Entity):
    id = PrimaryKey(int, auto=True)
    placement = Optional(str)
    damage = Optional(int)
    summoner = Required(Summoner)
    match = Required(Match)
    augments = Set('Augment')
    traits = Set('Trait')
    units = Set('Unit')


class Augment(db.Entity):
    id = PrimaryKey(int, auto=True)
    icon = Optional(str)
    summoner_matchs = Set(SummonerMatch)


class Trait(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    icon = Required(str)
    style = Required(int)
    summoner_matchs = Set(SummonerMatch)


class Item(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    icon = Required(str)
    units = Set('Unit')


class Unit(db.Entity):
    id = PrimaryKey(int, auto=True)
    items = Optional(Item)
    rarity = Required(int)
    tier = Required(int)
    icon = Required(str)
    summoner_matchs = Set(SummonerMatch)


class Lobby(db.Entity):
    id = PrimaryKey(int, auto=True)
    points = Required(str)
    qtd_matches = Required(int)
    qtd_classified = Required(int)
    start_date = Required(datetime)
    tournament = Required('Tournament')
    matchs = Set(Match)
    next_lobby = Optional('Lobby', reverse='next_lobby')


class Tournament(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    start_date = Required(datetime)
    lobbys = Set(Lobby)



db.generate_mapping()