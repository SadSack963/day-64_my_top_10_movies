from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Length
import requests
import os


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
    ranking = db.Column('ranking', db.Integer(), nullable=False)
    review = db.Column('review', db.String(1000), nullable=False)
    img_url = db.Column('img_url', db.String(1000), nullable=False)

    def __repl__(self):
        return f'<Movie: {self.title}'


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


# ROUTES
# ======

@app.route("/")
def home():
    # Get a list of all movies in the database
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


# ToDo: Pass the movie in, get the data out
@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_rating_form = RateMovieForm()
    if edit_rating_form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('edit.html', form=edit_rating_form)


@app.route("/delete")
def delete():
    pass
    return render_template({{url_for('home')}})


if __name__ == '__main__':
    app.run(debug=True)
