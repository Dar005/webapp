#Student Name:      Darran Gahan
#Student Number:    C00098391
# data_utils.py - part of the WordGame - by Paul Barry.
# email: paul.barry@itcarlow.ie

import DBcm

config = {
    'user': 'scoreuser',
    'password': 'scorepasswd',
    'host': 'localhost', # Change this on pythonAnywhere.for
    'database': 'scoresDB',
}

def add_to_scores(name, score, word) -> None:
    """Add the name its associated score to the db,
       as the word (which was the sourceword)."""
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """
        insert into leaderboard
        (name, sourceword, timetaken)
        values
        (%s, %s, %s)
        """
        cursor.execute(_SQL, (name, word, score))


def get_sorted_leaderboard() -> list:
    """Return a sorted list of tuples - this is the leaderboard."""
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """
        select timetaken, name, sourceword from leaderboard
        order by timetaken asc
        """
        cursor.execute(_SQL)
        return cursor.fetchall()