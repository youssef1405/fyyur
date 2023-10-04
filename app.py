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
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist)


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    artist_form = ArtistForm()
    return render_template('forms/new_artist.html', form=artist_form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # print(request.form['name'])
    artist = Artist(name=request.form['name'], city=request.form['city'],
                    state=request.form['state'], phone=request.form['phone'], genres=request.form['genres'],
                    image_link=request.form['image_link'], facebook_link=request.form['facebook_link'])
    db.session.add(artist)
    db.session.commit()
    return render_template('pages/home.html')


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    return render_template('forms/edit_artist.html', form=form, artist=artist)


if __name__ == '__main__':
    app.run(debug=True)
