from flask import Flask, render_template, request, session, redirect
import word_utils
import data_utils
import time
from wordgame import check_words

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           the_title = 'WordGame web.')


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
                           the_word = sourceword)


@app.route('/processwords', methods=['GET', 'POST'])
def word_process():
    # Gets and return the user_input
    if request.method == 'GET':
        return render_template('running.html',
                               the_title = 'error....')
    elif request.method == 'POST':
        session['end_time'] = time.perf_counter()
        user_input = request.form['user_input']
        session['user_input'] = user_input
        winner, status, words = check_words(session.get('sourceword'), user_input)
        session['winner'] = winner
        print(winner, status)
        if winner:
            session['time_taken'] = session['end_time'] - session['start_time']
            return render_template('winner.html',
                                   time_taken = session['time_taken'],)

        return render_template('loser.html',
                             the_tilte = 'user info',
                             the_word = session.get('sourceword'),
                             user_input = user_input,
                             status = status,
                             words = words)

@app.route('/addwinner', methods=['GET','POST'])
def add_winner():
    if request.method == 'POST':
        if session.get('winner'):
            data_utils.add_to_scores(request.form.get('user_name'), session.get('time_taken'))
            session['winner'] = False
            session['time_taken'] = False
            leaderboard = data_utils.get_sorted_leaderboard()[:10]
            return render_template('leaderboard.html',
                                   leaderboard = leaderboard)
        return redirect('/')


if __name__ == '__main__':
    app.secret_key = "adfs;45;']sgakltuuos;ga]][g"
    app.run(debug=True)