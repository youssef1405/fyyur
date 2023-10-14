from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))


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
    artist = Artist(name=request.form['name'], city=request.form['city'],
                    state=request.form['state'], phone=request.form['phone'], genres=request.form['genres'],
                    image_link=request.form['image_link'], facebook_link=request.form['facebook_link'], website_link=request.form['website_link'])
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

# VENUE ROUTES AND CONTROLLERS


@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_form():
    if request.method == 'GET':
        venue_form = VenueForm()
        return render_template('forms/new_venue.html', form=venue_form)
    else:
        venue = Venue(name=request.form['name'], city=request.form['city'], address=request.form['address'],
                      state=request.form['state'], phone=request.form['phone'], genres=request.form['genres'],
                      image_link=request.form['image_link'], facebook_link=request.form['facebook_link'], website_link=request.form['website_link'])
        db.session.add(venue)
        db.session.commit()
        return render_template('pages/home.html')


@app.route('/venues', methods=['GET'])
def show_all_venues():
    areas = {}
    res = Venue.query.all()
    for venue in res:
        if venue.city in areas:
            areas[venue.city].append(venue)
        else:
            areas[venue.city] = [venue]

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if request.method == 'GET':
        venue_form = VenueForm()
        venue_form.name.data = venue.name
        venue_form.city.data = venue.city
        venue_form.state.data = venue.state
        venue_form.address.data = venue.address
        venue_form.phone.data = venue.phone
        venue_form.genres.data = venue.genres
        venue_form.facebook_link.data = venue.facebook_link
        venue_form.website_link.data = venue.website_link
        return render_template('forms/edit_venue.html', form=venue_form, venue=venue)
    else:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.geners = request.form['genres']
        venue.facebook_link = request.form['facebook_link']
        venue.website_link = request.form['website_link']
        db.session.commit()
        return redirect(url_for('show_venue', venue_id=venue_id))


if __name__ == '__main__':
    app.run(debug=True)
