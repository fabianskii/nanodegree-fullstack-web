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
                     winner INTEGER REFERENCES player (player_id),
                     loser INTEGER REFERENCES player (player_id)
                    );

WITH wins as (SELECT p.player_id, COUNT(winner) as wins
                       FROM player as p LEFT JOIN match ON p.player_id = match.winner
                       GROUP BY p.player_id), loses as ( SELECT p.player_id, COUNT(loser) as loses
                       FROM player as p LEFT JOIN match ON p.player_id = match.loser GROUP BY p.player_id)
                       SELECT w.player_id, p.name, w.wins, l.loses+w.wins as matches FROM wins as w
                       LEFT JOIN (loses as l
                       LEFT JOIN player as p ON l.player_id = p.player_id) ON w.player_id = l.player_id
                       GROUP BY w.player_id,w.wins,l.loses,p.name ORDER BY w.wins desc