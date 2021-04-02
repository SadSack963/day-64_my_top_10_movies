from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
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


# ROUTES
# ======

# @app.route("/")
# def home():
#     return render_template("index.html")
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
