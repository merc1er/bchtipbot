"""This module interacts with playmo.gg's API"""
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
    # Entrance fee (in mo and USD)
    entrance_fee = round(
        game_details.get("details")[0].get("mod_inputs").get("bet_size") / 1000
    )
    # entrance_fee_usd = entrance_fee * bch_rate / 100000

    return {"title": title, "entrance_fee": entrance_fee}
