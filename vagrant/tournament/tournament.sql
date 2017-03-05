-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE player ( player_id SERIAL PRIMARY KEY,
                      name TEXT
                     );

CREATE TABLE match ( match_id SERIAL PRIMARY KEY,
                     player_1_id INTEGER REFERENCES player (player_id),
                     player_2_id INTEGER REFERENCES player (player_id),
                     player_winner INTEGER REFERENCES player (player_id)
                     );

CREATE VIEW ranking as
SELECT p.player_id, p.name, count(m.match_id) as wins
FROM player as p, match as m WHERE p.player_id = m.player_winner
GROUP BY p.name, p.player_id ORDER BY wins;
