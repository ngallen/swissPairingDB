-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tDB;
\c tournament;

DROP TABLE IF EXISTS p CASCADE;
DROP TABLE IF EXISTS m;

CREATE TABLE p(
	pid serial NOT NULL,
	name VARCHAR (40) NOT NULL,
	wins integer DEFAULT 0,
	matches integer DEFAULT 0,
	PRIMARY KEY (pID)
);

CREATE TABLE m(
	mid serial NOT NULL,
	winner VARCHAR (40) NOT NULL,
	loser VARCHAR (40) NOT NULL,
	PRIMARY KEY (mID)
);

