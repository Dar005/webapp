# Student Name:     Darran Gahan
# Student Number:   C00098391
# wordgame.py - the WordGame webapp - by Paul Barry.
# email: paul.barry@itcarlow.ie

import enchant
import word_utils


# Before we do anything else, pre-process the words, then
# update our enchant dictionary.  We do this only ONCE.
# Yes, that's right: these are GLOBAL.
word_utils.pre_process_words()
wordgame_dictionary = enchant.DictWithPWL('en_GB', word_utils.ALL_WORDS)


def check_spellings(words):
    """Check a list of words for spelling errors.

       Is the word in the dictionary.
       Accepts a list of words and returns a list of tuples,
       with each tuple containing (word, bool) based on
       whether or not the word is spelled correctly."""
    spellings = []
    for w in words:
        spellings.append((w, wordgame_dictionary.check(w)))
    return spellings


def check_words(sourceword, seven_words):
    seven_words = seven_words.strip().split(' ')
    errors = []
    winner = True
    if seven_words[0] == '':
        winner = False
        error = ("No words entered. You've gotta gimme something to work with"
                 " here!!.", [])
        errors.append(error)
        return (winner, errors)
    if len(seven_words) != 7:
        winner = False
        error = ('You did not provide seven words, maybe more, maybe '
                 'less.', [])
        errors.append(error)
        return (winner, errors)
    disallowed_letters = []
    for word in seven_words:
        disallowed = [letter for (letter, ok) in
                      word_utils.check_letters(sourceword, word)
                      if not ok]
        disallowed_letters.extend(disallowed)  # Here
    if disallowed_letters:
        winner = False
        error = ('Not allowed letters: ', set(disallowed_letters))
        errors.append(error)
    misspelt_words = [word for (word, ok) in
                      check_spellings(seven_words)
                      if not ok]
    if misspelt_words:
        winner = False
        error = ('Misspelt words:', sorted(misspelt_words))
        errors.append(error)
    short_words = [word for (word, ok) in
                   word_utils.check_size(seven_words)
                   if not ok]
    if short_words:
        winner = False
        error = ('These words are too small: ', sorted(short_words))
        errors.append(error)
    if word_utils.duplicates(seven_words):
        winner = False
        error = ('You have duplicates:', sorted(seven_words))
        errors.append(error)
    if word_utils.check_not_sourceword(seven_words, sourceword):
        winner = False
        error = ('You cannot use the source word: ', [sourceword])
        errors.append(error)
    if winner:
        return (winner, [])
    return (winner, errors)
