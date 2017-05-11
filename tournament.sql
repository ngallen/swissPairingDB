-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS p CASCADE;
DROP TABLE IF EXISTS m;

CREATE TABLE players(
	pid serial,
	name TEXT NOT NULL,
	PRIMARY KEY (pID)
);

CREATE TABLE matches(
	mid serial NOT NULL,
	winner INTEGER REFERENCES players (pid),
	loser INTEGER REFERENCES players (pid),
	PRIMARY KEY (mID)
);

