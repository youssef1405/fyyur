from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from forms import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))


db.create_all()


@app.route('/')
def index():
    return render_template('pages/home.html')


@app.route('/artists')
def artists():
    data = [
        {"id": 4, "name": "Guns N Petals"},
        {"id": 5, "name": "Matt Quevedo"},
        {"id": 6, "name": "The Wild Sax Band"},
    ]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_name):
    return f'{artist_name}'


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    #artist_form = ArtistForm()
    return render_template('forms/new_artist.html', form=artist_form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    print(request.form['name'])
    return render_template('pages/home.html')


if __name__ == '__main__':
    app.run(debug=True)
