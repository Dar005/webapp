from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            the_title = 'This is the INDEX page.')

@app.route('/listing')
def display_listing():
    names = ['Paul', 'George', 'Ringo', 'John']
    return render_template('listing.html',
                           the_title = 'This is the LISTING page.',
                           the_names = names, )


@app.route('/hello/<name>')
def hello(name):
    if name == None:
        name = 'unknown'
    return render_template('hello.html',
                           the_name = name,
                           the_title = 'This is the HELLO page.',)


@app.route('/bye')
def bye():
    return render_template('bye.html',
                           the_title = 'This is the BYE page.')


if __name__ == '__main__':
    app.run(debug=True)



