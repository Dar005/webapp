#Student Name:      Darran Gahan
#Student Number:    C00098391
# data_utils.py - part of the WordGame - by Paul Barry.
# email: paul.barry@itcarlow.ie

import pymongo


def add_to_scores(name, score, word, user_input):
    """Add the name and its associated score to the db,
       as the word (which was the sourceword)."""
    score = {
        'name': name,
        'score': score,
        'sourceword': word,
        'words': user_input,
    }
    client = pymongo.MongoClient()
    db = client['leadersDB']
    c = db['leaderboard']
    c.insert_one(score)


def get_sorted_leaderboard():
    """Return a sorted list of tuples - this is the leaderboard."""
    client = pymongo.MongoClient()
    db = client['leadersDB']
    c = db['leaderboard']
    results = []
    for s in c.find().sort('score', pymongo.ASCENDING):
        results.append( ( s['score'], s['name'], s['words'] ) )
    return results
