import requests
import json
import asyncio
from config import api_request_cooldown
from time import time, sleep
from math import ceil

api_cooldown = [0]
user_agent = {'User-agent': 'private_score_saber_dc_bot_Klappson#0110'}
profile_name_url = "https://new.scoresaber.com/api/players/by-name/{0}"
profile_id = "https://new.scoresaber.com/api/player/{0}/full"
scores_id_page = "https://new.scoresaber.com/api/player/{0}/scores/recent/{1}"


async def get_score_page(player_id, page, retries=2) -> list[dict]:
    api_respo = await api_request(
        url=scores_id_page.format(player_id, page),
        retries=retries
    )
    return api_respo["scores"]


async def get_latest_song(player_id):
    scores = await get_score_page(player_id, 1)

    if len(scores) < 0:
        return None
    return scores[0]


async def get_full_profile(player_id, retries=2) -> dict:
    return await api_request(
        url=profile_name_url.format(player_id),
        retries=retries
    )


async def search_player(player_name, retries=2) -> list[dict]:
    api_respo = await api_request(
        url=profile_name_url.format(player_name),
        retries=retries
    )
    return api_respo["players"]


async def api_request(url: str, retries=0) -> dict:
    since_last_request = int(time()) - api_cooldown[0]

    if since_last_request < api_request_cooldown:
        sleep_time = ceil(api_request_cooldown - since_last_request)
        print(f"Waiting {sleep_time} seconds before next api-request")
        await asyncio.sleep(sleep_time)

    def retry(ex_msg=""):
        if retries > 0:
            print(f"Request Failed! Retrying... {retries}")
            await asyncio.sleep(10)
            return await api_request(url, (retries - 1))
        else:
            if ex_msg != "":
                print(ex_msg)
            raise IOError(f"Ran out of retries for {url}")

    try:
        print(f"Requesting: {url}")
        request_result = requests.get(url, headers=user_agent)
        api_cooldown[0] = int(time())

        if request_result.status_code != 200:
            retry("HTTP-Code is not 200")

        clean_result = request_result.text.replace("'", "`")
        return json.loads(clean_result)
    except Exception as e:
        retry(repr(e))