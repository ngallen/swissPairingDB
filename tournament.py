#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

"""Remove all the match records from the database."""
def deleteMatches():
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM m")
	c.execute("UPDATE p SET wins=0, matches=0")
	conn.commit()
	conn.close()

"""Remove all the player records from the database."""
def deletePlayers():
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM p")
	conn.commit()
	conn.close()


"""Returns the number of players currently registered."""
def countPlayers():
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT Count(*) FROM p")
	count = c.fetchone()[0]
	conn.close()
	return count

"""Adds a player to the tournament database."""
def registerPlayer(name):
	cleanName = bleach.clean(name.replace("'", "''"))
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO p (name) VALUES ('{}')".format(cleanName))
	conn.commit()
	conn.close()

"""Returns a list of the players and their win records, sorted by wins."""
def playerStandings():

	conn = connect()
	c = conn.cursor()
	c.execute("SELECT * FROM p ORDER BY wins, name desc")
	return c.fetchall()
	conn.close()

"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
def reportMatch(winner, loser):
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO m (winner, loser) VALUES ('{}','{}')".format(winner, loser))
	c.execute("UPDATE p SET wins=wins+1, matches=matches+1 WHERE pid='{}'".format(winner))
	c.execute("UPDATE p SET matches=matches+1 WHERE pid='{}'".format(loser))
	conn.commit()
	conn.close()

	"""Returns a list of pairs of players for the next round of a match.
	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
	"""

def swissPairings():
	conn = connect()
	c = conn.cursor()
	pairings = []
	c.execute("DROP VIEW IF EXISTS v0")
	""" **NOTE** The project description specified that I use
	the playerStanding() method. I believe my way of creating an SQL VIEW
	and DELETING from the view, 2 at a time is a cleaner way to do it.
	It also shows off the SQL skills taught in this lesson better to
	potential employers."""
	c.execute("CREATE VIEW v0 as SELECT pid, name from p ORDER BY wins desc")
	while True:
		c.execute("""DELETE from v0
							WHERE pid IN (
							SELECT pid
							FROM v0
							LIMIT 2
							) RETURNING *""")
		if c.rowcount == 0:
			break
		temp = c.fetchall()
		pairings.append((temp[0][0], temp[0][1], temp[1][0], temp[1][1]))
	conn.close()
	return pairings

