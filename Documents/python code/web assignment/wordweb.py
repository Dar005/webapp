from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           the_title = 'WordGame web.')

@app.route('/input')
def input():
    return render_template('input.html',
                           the_title = 'Input page.')

@app.route('/winner')
def winner():
    return render_template('winner.html',
                           the_tilte = 'Winner.')


if __name__ == '__main__':
    app.run(debug=True)