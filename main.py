from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length
import os
import tmdb

# Create the database file in /database/new-books-collection.db
FILE_URL = 'sqlite:///database/movies-collection.db'

app = Flask(__name__)
# Config for Bootstrap
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
# Config for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URL  # load the configuration for database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Significant overhead if True. Future default: False
db = SQLAlchemy(app)  # create the SQLAlchemy object by passing it the application


class Movie(db.Model):
    __tablename__ = 'Movies'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(250), unique=True, nullable=False)
    year = db.Column('year', db.String(5), nullable=False)
    description = db.Column('description', db.String(250), nullable=False)
    rating = db.Column('rating', db.Float(), nullable=False)
    ranking = db.Column('ranking', db.Integer(), nullable=True)
    review = db.Column('review', db.String(1000), nullable=True)
    img_url = db.Column('img_url', db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Movie: {self.title}>'


# Create the database file and tables
if not os.path.isfile(FILE_URL):
    db.create_all()

# # Create a test movie
# new_movie = Movie(
#     title='Phone Booth',
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
#                 "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads "
#                 "to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg",
# )
# db.session.add(new_movie)
# db.session.commit()
# # Print Out Movie Title
# movie = Movie.query.get(1)
# print(repr(movie))  # or print(movie.__repr__())
# # >>> <Movie: Phone Booth>
# exit()


class RateMovieForm(FlaskForm):
    new_rating = DecimalField(
        label='Your Rating',
        validators=[DataRequired()],
    )
    new_review = StringField(
        label='Your Review',
        validators=[InputRequired(), Length(max=1000)],
    )
    submit_button = SubmitField(
        label='Done',
        render_kw={'btn-primary': 'True'},
    )


class AddMovieForm(FlaskForm):
    new_movie = StringField(
        label='Movie Title',
        validators=[InputRequired(), Length(max=1000)],
    )
    submit_button = SubmitField(
        label='Add',
        render_kw={'btn-primary': 'True'},
    )


# ROUTES
# ======

@app.route("/")
def home():
    # Get a list of all movies in the database
    all_movies = db.session.query(Movie).order_by('rating').all()
    number_of_movies = len(all_movies)
    for i, movie in enumerate(all_movies):
        movie.ranking = number_of_movies - i
    db.session.commit()  # Write to database file
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    # TODO: I need to review - I failed this challenge... though I did get close :(
    form = RateMovieForm()
    # Get movie_id from the argument in the index.html <a> tag
    movie_id = request.args.get('id')
    # Find the movie in the database
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        # This also works:
        # movie.rating = float(request.form['new_rating'])
        # movie.review = request.form['new_review']
        movie.rating = float(form.new_rating.data)
        movie.review = form.new_review.data
        db.session.commit()  # Write to database file
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)


@app.route("/delete")
def delete():
    # Get movie_id from the argument in the index.html <a> tag
    movie_id = request.args.get('id')
    # Find the movie in the database
    movie = Movie.query.get(movie_id)
    # Delete it
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.new_movie.data
        # Get movie info from API
        json = tmdb.search_movie(movie_title)
        return render_template('select.html', data=json)
    return render_template('add.html', form=form)


@app.route('/find')
def find_movie():
    # TODO: Get movie details and add to database
    movie_id = request.args.get('id')
    movie = tmdb.get_movie_info(movie_id)

    """
    "In order to generate a fully working image URL, you'll need 3 pieces of data. 
    Those pieces are a base_url, a file_size and a file_path."

    You can get the images sizes from GET /configuration, e.g. paste this into your browser address bar:
    https://api.themoviedb.org/3/configuration?api_key=<your_api_key>

    """
    base_url = 'https://image.tmdb.org/t/p/'
    file_size = 'original'
    file_path = movie['poster_path']
    img_url = base_url + file_size + file_path

    new_movie = Movie(
        title=movie['title'],
        year=movie['release_date'][0:3],
        description=movie['overview'],
        rating=movie['vote_average'],
        review=movie['tagline'],
        img_url=img_url,
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5005)
