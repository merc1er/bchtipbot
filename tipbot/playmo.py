"""This module interacts with playmo.gg's API"""
import datetime
import requests


BASE_URL = "https://playmo.gg"


def init_session():
    """Get mandatory session_id and session_key"""
    session = requests.Session()
    r = session.post(
        BASE_URL + "/v2/init_session",
        json={"utm_source": "https://merc1er.com"},
    )
    keys = r.json()
    return keys


def get_game_overview(game_id):
    keys = init_session()
    data = {
        "game_id": [game_id],
        "session_id": keys.get("session_id"),
        "session_key": keys.get("session_key"),
    }

    r = requests.post(BASE_URL + "/playmo/v1/get_game_details", json=data)
    game_details = r.json()

    #################################################
    # Extract main game data from the json response #
    #################################################
    # Game title
    title = game_details.get("details")[0].get("mod_inputs").get("title")
    # Entrance fee (in mo)
    entrance_fee = round(
        game_details.get("details")[0].get("mod_inputs").get("bet_size") / 1000
    )
    # Cutoff time
    start = game_details.get("details")[0].get("mod_inputs").get("start")
    # Number of players
    players = len(
        game_details.get("details")[0].get("mod_inputs").get("outcome")
    )
    max_players = game_details.get("details")[0].get("mod_inputs")\
        .get("max_players")

    return {
        "title": title,
        "entrance_fee": entrance_fee,
        "start": start,
        "players": players,
        "max_players": max_players,
    }


def game_countdown(dt):
    """Calculate the time left before a game"""
    start = datetime.datetime.fromisoformat(dt[:-1])
    now = datetime.datetime.utcnow()
    td = start - now
    return days_hours_minutes(td)


def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60
