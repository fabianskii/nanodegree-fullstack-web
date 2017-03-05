#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()

    connection = DB.cursor()
    connection.execute("DELETE FROM match")

    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""

    DB = connect()
    connection = DB.cursor()

    connection.execute("DELETE FROM player")

    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""

    DB = connect()
    connection = DB.cursor()

    connection.execute("SELECT count(name) as playerCount FROM player")
    response = {'player_count': connection.fetchone()[0]}

    DB.commit()
    DB.close()

    return response['player_count']

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()

    c.execute("INSERT INTO player (name) VALUES (%s)", (name,))

    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

   Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    connection = DB.cursor()

    if (countPlayers() == 0):
        return []
    #Maybe a view would make a better job here...
    connection.execute("WITH wins as (SELECT p.player_id, COUNT(winner) as wins "
                       "FROM player as p LEFT JOIN match ON p.player_id = match.winner "
                       "GROUP BY p.player_id), loses as ( SELECT p.player_id, COUNT(loser) as loses "
                       "FROM player as p LEFT JOIN match ON p.player_id = match.loser GROUP BY p.player_id) "
                       "SELECT w.player_id, p.name, w.wins, l.loses+w.wins as matches FROM wins as w "
                       "LEFT JOIN (loses as l "
                       "LEFT JOIN player as p ON l.player_id = p.player_id) ON w.player_id = l.player_id "
                       "GROUP BY w.player_id,p.name,w.wins,l.loses ORDER BY w.wins desc")

    results = connection.fetchall()
    return results;

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    connection = DB.cursor()

    connection.execute("INSERT INTO match (winner, loser) "
                        "VALUES (%s, %s)", (winner, loser,))

    DB.commit()
    DB.close

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    pairings = []

    while (standings):
        for pairs in xrange(2):
            player1 = standings.pop(0)
            player2 = standings.pop(0)
            match = (player1[0], player1[1], player2[0], player2[1])
            pairings.append(match)

    return pairings



