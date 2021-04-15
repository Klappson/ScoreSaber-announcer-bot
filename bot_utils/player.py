import scoresaber as ss
import db_handler as dbh
from os.path import join

get_player_sql = open(join("sql", "get_player.sql"), "r").read()
insert_player_sql = open(join("sql", "insert_player.sql"), "r").read()
update_player_sql = open(join("sql", "update_player.sql"), "r").read()


class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def is_in_db(self) -> bool:
        db_retu = dbh.get().send_statm(get_player_sql.format(self.player_id))

        if len(db_retu) == 1:
            return True
        return False

    def get(self):
        db_retu = dbh.get().send_statm(get_player_sql.format(
            self.player_id
        ))
        self.player_name = db_retu[0][1]
        self.total_play_count = db_retu[0][2]
        self.last_announced_song_id = db_retu[0][3]

    async def update(self):
        score_player = await ss.get_full_profile(self.player_id)
        dbh.get().send_statm(update_player_sql.format(
            score_player["playerInfo"]["playerName"],
            score_player["scoreStats"]["totalPlayCount"],
            await ss.get_latest_song(self.player_id)["scoreId"],
            self.player_id
        ))

    async def insert(self):
        score_player = await ss.get_full_profile(self.player_id)
        dbh.get().send_statm(insert_player_sql.format(
            self.player_id,
            score_player["playerInfo"]["playerName"],
            score_player["scoreStats"]["totalPlayCount"],
            await ss.get_latest_song(self.player_id)["scoreId"]
        ))

