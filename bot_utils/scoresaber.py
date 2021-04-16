import requests
import json
import asyncio
from config import api_request_cooldown
from time import time
from math import ceil

api_cooldown = [0]
request_cache = {}
user_agent = {'User-agent': 'scoresaber_dc_announcer_Klappson#0110'}
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
        url=profile_id.format(player_id),
        retries=retries
    )


async def search_player(player_name, retries=2) -> list[dict]:
    api_respo = await api_request(
        url=profile_name_url.format(player_name),
        retries=retries
    )
    return api_respo["players"]


def check_cache(url: str):
    if url not in request_cache:
        print(f"{url} is not cached")
        return None
    cache_tupel = request_cache[url]
    cache_age = int(time()) - cache_tupel[0]

    if cache_age > 60:
        print(f"{url} is cached but to old ({cache_age}s)")
        return None

    print(f"{url} is still cached ({cache_age}s)")
    return cache_tupel[1]


async def api_request(url: str, retries=0) -> dict:
    cache_result = check_cache(url)
    if cache_result is not None:
        return cache_result

    since_last_request = int(time()) - api_cooldown[0]
    if since_last_request < api_request_cooldown:
        sleep_time = ceil(api_request_cooldown - since_last_request)
        print(f"Waiting {sleep_time} seconds before next api-request")
        await asyncio.sleep(sleep_time)

    async def retry(ex_msg=""):
        if ex_msg != "":
            print(ex_msg)
        if retries > 0:
            print(f"Request Failed! Retrying... {retries}")
            await asyncio.sleep(10)
            return await api_request(url, (retries - 1))
        else:
            raise IOError(f"Ran out of retries for {url}")

    try:
        print(f"Requesting: {url}")
        request_result = requests.get(url, headers=user_agent)
        api_cooldown[0] = int(time())

        if request_result.status_code != 200:
            return await retry("HTTP-Code is not 200")

        clean_result = request_result.text.replace("'", "`")
        retu = json.loads(clean_result)
        request_cache[url] = (int(time()), retu)
        return retu
    except Exception as e:
        return await retry(repr(e))
