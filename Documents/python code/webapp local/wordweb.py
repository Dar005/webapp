# Student Name:     Darran Gahan
# Student Number:   C00098391

from flask import Flask, render_template, request, session, redirect
from flask import copy_current_request_context
import word_utils
import data_utils
import time
import wordgame
from threading import Thread

app = Flask(__name__)
app.secret_key = "adfs;45;']sgakltuuos;ga]][g"


@app.route('/')
def index():
    return render_template('index.html',
                           the_title='WordGame.')


@app.route('/running')
def running():
    # gets a random source word and displays it
    word_utils.pre_process_words()
    sourceword = word_utils.get_source_word()
    print(sourceword)
    session['sourceword'] = sourceword
    session['start_time'] = time.perf_counter()

    return render_template('running.html',
                           the_title='WordGame',
                           sourceword=sourceword)


@app.route('/processwords', methods=['GET', 'POST'])
def word_process():

    @copy_current_request_context
    def log_attempt(sourceword, user_input, request):
        with open('attempts.log', 'a') as logf:
            print(f"{sourceword}: {user_input}: {str(request)}", file=logf)
            print(str(request.user_agent), file=logf)
            print(str(request.host), file=logf)
            print(str(request.remote_addr), file=logf)
    # Gets and returns the user_input
    if request.method == 'POST':
        session['end_time'] = time.perf_counter()
        user_input = request.form['user_input']
        session['user_input'] = user_input
        winner, words = wordgame.check_words(session.get('sourceword'), user_input)
        session['winner'] = winner
        # data_utils.log_attempt(session['sourceword'], session['seven_words'], request)
        # attempts to log user input, source word, user ip, time of attempt and browser used
        try:
            t = Thread(target=log_attempt, args=(session['sourceword'], session['user_input'], request))
            t.start()
        except Exception as err:
            print('***** Logging failed with reported error:', str(err))
        if winner:
            # if user wins
            session['time_taken'] = session['end_time'] - session['start_time']
            final_time = round(session['time_taken'], 2)
            session['final_time'] = final_time
            return render_template('winner.html',
                                   time_taken=session['time_taken'],
                                   final_time=final_time,
                                   the_title='Winner')
        return render_template('loser.html',
                               # if user loses
                               the_tilte='WordGame',
                               sourceword=session.get('sourceword'),
                               user_input=user_input,
                               words=words, )


@app.route('/addwinner', methods=['GET', 'POST'])
def add_winner():
    if request.method == 'POST':
        if session.get('winner'):
            data_utils.add_to_scores(request.form.get('user_name'),
                                     session.get('final_time'),
                                     session.get('sourceword'),
                                     session.get('user_input'),
                                     )
            session['winner'] = False
            session['time_taken'] = False
            leaderboard = data_utils.get_sorted_leaderboard()[:10]
            return render_template('leaderboard.html',
                                   the_title='WordGame',
                                   leaderboard=leaderboard,)
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = "adfs;45;']sgakltuuos;ga]][g"