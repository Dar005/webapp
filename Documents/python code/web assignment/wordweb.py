from flask import Flask, render_template, request, session, redirect
import word_utils
import data_utils
import time
from wordgame import check_words

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           the_title = 'WordGame.')


@app.route('/running')
def running():
    # gets a random source word and displays it
    word_utils.pre_process_words()
    sourceword = word_utils.get_source_word()
    print(sourceword)
    session['sourceword'] = sourceword
    session['start_time'] = time.perf_counter()

    return render_template('running.html',
                           the_title = 'WordGame',
                           sourceword = sourceword)


@app.route('/processwords', methods=['GET', 'POST'])
def word_process():
    # Gets and returns the user_input
    if request.method == 'POST':
        session['end_time'] = time.perf_counter()
        user_input = request.form['user_input']
        session['user_input'] = user_input
        winner, words = check_words(session.get('sourceword'), user_input)
        session['winner'] = winner
        if winner:
            ## if user wins
            session['time_taken'] = session['end_time'] - session['start_time']
            final_time = round(session['time_taken'], 2)
            session['final_time'] = final_time
            return render_template('winner.html',
                                   time_taken = session['time_taken'],
                                   final_time = final_time,
                                   the_title = 'Winner')

        return render_template('loser.html',
                               ## if user loses
                             the_tilte = 'user info',
                             sourceword = session.get('sourceword'),
                             user_input = user_input,
                             words = words,
                             the_title = 'Wordgame')


@app.route('/addwinner', methods=['GET','POST'])
def add_winner():
    if request.method == 'POST':
        if session.get('winner'):
            data_utils.add_to_scores(request.form.get('user_name'), session.get('final_time'))
            session['winner'] = False
            session['time_taken'] = False
            leaderboard = data_utils.get_sorted_leaderboard()[:10]
            return render_template('leaderboard.html',
                                   leaderboard = leaderboard,
                                   the_title = 'Wordgame')
        return redirect('/')


if __name__ == '__main__':
    app.secret_key = "adfs;45;']sgakltuuos;ga]][g"
    app.run(debug=True)