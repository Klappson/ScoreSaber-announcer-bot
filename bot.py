import discord
import bot_utils.db_handler as dbh
from os.path import join
from asyncio import sleep, run
from bot_utils.player import Player
from config import dc_token, channel_id, monitored_players

scoresaber_icon_url = "https://pbs.twimg.com/profile_images/1346980795513139201/rYiHR2pu_400x400.png"
song_picture = "http://new.scoresaber.com/api/static/covers/{0}.png"
db_setup_sql = open(join("sql", "db_setup.sql"), "r").read()


class BotInstance:
    def __init__(self):
        self.commands = []

        self.loop_running = False
        inte = discord.Intents.default()

        self.dc = discord.Client(intents=inte)
        self.setup_discord()

    def register_command_event(self):
        @self.dc.event
        async def on_message(message: discord.Message):
            print(message.content)

        @self.dc.event
        async def on_ready():
            await announce_loop(self)

    def setup_discord(self):
        try:
            print("Connecting to discord...")

            self.register_command_event()
            self.dc.run(dc_token)
        except Exception as e:
            print("Unable to connect to discord-api. " +
                  "Make sure that the api is currently available " +
                  "and your key is correct")
            raise e


async def announce_loop(bot: BotInstance):
    if bot.loop_running:
        print("Somehow a second loop tried to start")
        return
    bot.loop_running = True

    while True:
        await announce_new_scores(bot)
        print(5)
        await sleep(60)
        print(4)
        await sleep(60)
        print(3)
        await sleep(60)
        print(2)
        await sleep(60)
        print(1)
        await sleep(60)
        print(0)


def pretty_difficulty(difficulty_raw):
    diff_parts = difficulty_raw.split("_")
    try:
        return diff_parts[1]
    except IndexError as ie:
        return difficulty_raw


def get_embed(score_data, player_name):
    embed = discord.Embed(title=score_data["songName"], color=0xc20000)
    embed.set_author(name="New Score bc {0}".format(player_name),
                     icon_url=scoresaber_icon_url)
    embed.set_thumbnail(url=song_picture.format(score_data["songHash"]))
    embed.add_field(name="Score", value=score_data["score"], inline=True)
    embed.add_field(name="PP", value=score_data["pp"], inline=True)
    embed.add_field(name="Time Set", value=score_data["timeSet"], inline=False)
    embed.add_field(name="Diffuculty",
                    value=pretty_difficulty(score_data["difficultyRaw"]),
                    inline=True)
    return embed


async def announce_new_scores(bot: BotInstance):
    print("Announcing...")
    channel: discord.TextChannel = bot.dc.get_channel(channel_id)
    print(f"Channel {channel.name} selected!")

    for player_id in monitored_players:
        player: Player = Player(player_id)

        if not player.is_in_db():
            await player.insert()

        if not await player.has_new_scores():
            print(f"{player.player_name} has no new scores!")
            continue

        new_scores = await player.get_unannounced_scores()
        for new_score in new_scores:
            await channel.send(embed=get_embed(new_score, player.player_name))


if __name__ == "__main__":
    dbh.init_connection()
    dbh.get().send_statm(db_setup_sql)
    BotInstance()
