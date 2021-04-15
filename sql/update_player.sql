UPDATE player
SET player_name = '{0}',
    player_total_playcount = {1},
    player_last_announced_song_id = '{2}'
WHERE player_id = '{3}';