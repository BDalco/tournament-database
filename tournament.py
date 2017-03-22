#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import itertools


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Problems connecting to the database.")


def deleteMatches():
    """Remove all the match records from the database and sets matches and wins to 0."""
    """https://www.postgresql.org/docs/9.3/static/sql-truncate.html"""
    db, cursor = connect()
    query = "TRUNCATE matches"
    cursor.execute(query,)

    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)

    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT COUNT(*) FROM players;"
    cursor.execute(query)
    player_count = cursor.fetchone() [0]

    db.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players VALUES (DEFAULT, %s)"
    param = (name,)
    cursor.execute(query, param)

    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    # query = "SELECT player_id, player, wins, matches FROM players ORDER BY wins;"
    # Display & Count across multiple columns technique via http://stackoverflow.com/questions/30091148/postgresql-display-and-count-distinct-occurrences-of-values-across-multiple-col

    query = ("SELECT player_id, player, COUNT(matches.winner) AS wins, "
             "(SELECT games FROM matches_view WHERE matches_view.player_id = players.player_id) "
             "FROM players LEFT JOIN matches "
             "ON players.player_id = matches.winner "
             "GROUP BY players.player_id, players.player "
             "ORDER BY wins DESC")

    cursor.execute(query)
    standings = cursor.fetchall()

    db.close()

    return standings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    # update the matches table
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    param = (winner, loser)
    cursor.execute(query, param)
    
    db.commit()
    db.close()

 
 
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
    # Array for swiss pairing results
    results = []
    # Player Standings
    player_standings = playerStandings()
    
    # Using iZip via http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
    matchup_iter = itertools.izip(*[iter(player_standings)]*2)

    matchups = list(matchup_iter)

    # build the matchups
    for matchup in matchups:
        id1 = matchup[0][0]
        name1 = matchup[0][1]
        id2 = matchup[1][0]
        name2 = matchup[1][1]
        matchup = (id1, name1, id2, name2)
        results.append(matchup)

    return results