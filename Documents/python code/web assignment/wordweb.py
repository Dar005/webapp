from flask import Flask, render_template, request, session
import word_utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           the_title = 'WordGame web.')

@app.route('/input')
def input():
    return render_template('input.html',
                           the_title = 'Input page.')


@app.route('/running')
def running():
    word_utils.pre_process_words()
    sourceword = word_utils.get_source_word()
    session['sourceword'] = sourceword
    return render_template('running.html',
                           the_title = 'WordGame',
                           the_word = sourceword)

@app.route('/winner')
def winner():
    return render_template('winner.html',
                           the_tilte = 'Winner.')


if __name__ == '__main__':
    app.secret_key = "adfs;45;']sgakltuuos;ga]][g"
    app.run(debug=True)