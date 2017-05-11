#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

"""Remove all the match records from the database."""
def deleteMatches():
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM matches")
	conn.commit()
	conn.close()

"""Remove all the player records from the database."""
def deletePlayers():
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM players")
	conn.commit()
	conn.close()


"""Returns the number of players currently registered."""
def countPlayers():
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT Count(*) FROM players")
	count = c.fetchone()[0]
	conn.close()
	return count

"""Adds a player to the tournament database."""
def registerPlayer(name):
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
	conn.commit()
	conn.close()

"""Returns a list of the players and their win records, sorted by wins."""
def playerStandings():

	conn = connect()
	c = conn.cursor()
	c.execute("""CREATE VIEW v0 AS SELECT
								players.pid,
								count(matches.mid)
								AS wins FROM players
							LEFT OUTER JOIN matches
							ON
								players.pid = matches.winner
							GROUP BY players.pid""")
	c.execute("""CREATE VIEW v1 AS SELECT
								players.pid,
								count(matches.mid)
								AS matchTot FROM players
							LEFT OUTER JOIN matches
							ON
								players.pid = matches.winner
								OR players.pid = matches.loser
							GROUP BY players.pid""")
	c.execute("""SELECT players.pid, players.name, v0.wins, v1.matchTot  from players
						FULL OUTER JOIN v0 ON players.pid = v0.pid
						FULL OUTER JOIN v1 ON players.pid = v1.pid
						GROUP BY players.pid, v0.wins, v1.matchTot
						ORDER BY v0.wins desc
						"""
		)
	temp = c.fetchall()
	conn.close()
	return temp


"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
def reportMatch(winner, loser):
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", ((winner,), (loser,)))
	conn.commit()
	conn.close()



	"""Returns a list of pairs of players for the next round of a match.
	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
	"""

def swissPairings():
	standings = playerStandings()
	pairings = []
	while True:
		if len(standings) <= 0:
			break
		temp = []
		temp.append(standings.pop(0))
		temp.append(standings.pop(0))
		pairings.append((temp[0][0], temp[0][1], temp[1][0], temp[1][1]))

	return pairings





	# """Original solution, made the reviewer smile but
	# didn't quit pass Udacity standards"""
	# c.execute("DROP VIEW IF EXISTS v0")
	# c.execute("CREATE VIEW v0 as SELECT pid, name from players ORDER BY wins desc")
	# while True:
	# 	c.execute("""DELETE from v0
	# 						WHERE pid IN (
	# 						SELECT pid
	# 						FROM v0
	# 						LIMIT 2
	# 						) RETURNING *""")
	# 	if c.rowcount == 0:
	# 		break
	# 	temp = c.fetchall()
	# 	pairings.append((temp[0][0], temp[0][1], temp[1][0], temp[1][1]))
	# conn.close()
	# return pairings

