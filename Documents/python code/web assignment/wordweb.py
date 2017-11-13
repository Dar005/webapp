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
    # gets a random source word and displays it
    word_utils.pre_process_words()
    sourceword = word_utils.get_source_word()
    session['sourceword'] = sourceword
    return render_template('running.html',
                           the_title = 'WordGame',
                           the_word = sourceword)


@app.route('/processinput', methods=['GET', 'POST'])
def input_process():
    # Gets and return the user_input
    if request.method == 'GET':
        return render_template('running.html',
                               the_title = 'error....')
    elif request.method == 'POST':
        user_input = request.form['user_input']
        session['user_input'] = user_input
    return render_template('winner.html',
                           the_tilte = 'success.',
                           the_word = user_input)


if __name__ == '__main__':
    app.secret_key = "adfs;45;']sgakltuuos;ga]][g"
    app.run(debug=True)