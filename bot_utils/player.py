import bot_utils.scoresaber as ss
import bot_utils.db_handler as dbh
from os.path import join

get_player_sql = open(join("sql", "get_player.sql"), "r").read()
insert_player_sql = open(join("sql", "insert_player.sql"), "r").read()
update_player_sql = open(join("sql", "update_player.sql"), "r").read()


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.loaded = False

    def is_in_db(self) -> bool:
        db_retu = dbh.get().get_data(get_player_sql.format(self.player_id))

        if len(db_retu) == 1:
            return True
        return False

    async def get_unannounced_scores(self) -> list[dict]:
        self.load()
        retu = []
        page_counter = 1

        while True:
            result_page = await ss.get_score_page(self.player_id, page_counter)

            for score_dict in result_page:
                if str(score_dict["scoreId"]) == self.last_announced_song_id:
                    await self.update()
                    return retu
                retu.append(score_dict)

            page_counter += 1

    async def has_new_scores(self) -> bool:
        self.load()
        score_player = await ss.get_full_profile(self.player_id)
        api_total_playcount = score_player["scoreStats"]["totalPlayCount"]

        if self.total_play_count == api_total_playcount:
            return False
        return True

    def load(self):
        if self.loaded:
            return

        db_retu = dbh.get().get_data(get_player_sql.format(
            self.player_id
        ))
        self.player_name = db_retu[0][1]
        self.total_play_count = db_retu[0][2]
        self.last_announced_song_id = db_retu[0][3]

    async def update(self):
        score_player = await ss.get_full_profile(self.player_id)
        latest_song = await ss.get_latest_song(self.player_id)
        dbh.get().send_statm(update_player_sql.format(
            score_player["playerInfo"]["playerName"],
            score_player["scoreStats"]["totalPlayCount"],
            latest_song["scoreId"],
            self.player_id
        ))

    async def insert(self):
        score_player = await ss.get_full_profile(self.player_id)
        latest_song = await ss.get_latest_song(self.player_id)
        dbh.get().send_statm(insert_player_sql.format(
            self.player_id,
            score_player["playerInfo"]["playerName"],
            score_player["scoreStats"]["totalPlayCount"],
            latest_song["scoreId"]
        ))

