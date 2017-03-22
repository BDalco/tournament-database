-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



-- drop the database create the database from scratch
DROP DATABASE tournament;
CREATE DATABASE tournament;

-- connect to database
\c tournament

-- create the table for the players
CREATE TABLE players (
  player_id SERIAL PRIMARY KEY, 
  player TEXT
);

-- create the table for matches
CREATE TABLE matches (
  winner INTEGER references players(player_id), 
  loser INTEGER references players(player_id),
  PRIMARY KEY (winner, loser)
);

-- create a view that calculates the matches for each player
-- http://postgresguide.com/sql/views.html
CREATE OR REPLACE VIEW matches_view AS
SELECT players.player_id, COUNT(matches.*) AS games
FROM players LEFT JOIN matches ON players.player_id = matches.winner OR players.player_id = matches.loser
GROUP BY players.player_id;