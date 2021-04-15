CREATE TABLE IF NOT EXISTS player(
    player_id TEXT PRIMARY KEY,
    player_name TEXT NOT NULL,
    player_total_playcount BIGINT NOT NULL,
    player_last_announced_song_id TEXT NOT NULL
);