#__author__ == "Priyanka Shanmugasundaram (pshanmu)"
# note: most of this code is modified from lecture
import os
from flask import Flask, render_template, session, redirect, url_for, request# tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this
import seaborn as sns
from flask_wtf import Form
from wtforms import StringField, DecimalField, SubmitField, FloatField
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelForm
import requests
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = '05201996'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy



#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

# Set up association Table if you wanted many to many relationship:
collections = db.Table('collections',db.Column('genre_id',db.Integer, db.ForeignKey('genres.id')),db.Column('director_id',db.Integer, db.ForeignKey('directors.id')))

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    directors = db.relationship('Director',secondary=collections,backref=db.backref('genres',lazy='dynamic'),lazy='dynamic')
    #directors = db.relationship('Director', backref = 'Genre')
    movies = db.relationship('Movie',backref='Genre')


class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    movies = db.relationship('Movie',backref='Director')

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64)) # unique=True, Only unique title songs can exist in this data model
    genre = db.Column(db.Integer, db.ForeignKey("genres.id")) #ok to be null for now
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id")) # ok to be null for now
    #genre = db.Column(db.String(64)) # ok to be null
    imdb_rating = db.Column(db.Float)


    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.director_id, self.genre)

##### Form for Final Project####

class UpdateForm(Form):
    title = StringField('title', validators = [InputRequired()])
    director = StringField('director', validators = [InputRequired()])
    genre = StringField('genre', validators = [InputRequired()])
    imdb_rating = FloatField('imdb_rating', validators = [InputRequired()])
    submit = SubmitField('Submit')

##### Helper functions #####

### For database additions
### Relying on global session variable above existing

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director


##### Set up Controllers (route functions) #####

## Main route
@app.route('/') #MODIFED ROUTE 1 FOR FINAL PROJECT
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/movie/new/<title>/<genre>/<director>/<rating>') ## CHANGE FOR FINAL PROJECT (NEW ROUTE 1)
def new_movie(title, director, genre, rating):
    if Movie.query.filter_by(title=title).first(): # if there is a song by that title
        return "That movie already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        movie = Movie(title=title, director_id=director.id,genre=genre, imdb_rating = rating)
        session.add(movie)
        session.commit()
        return "New movie: {} by {}. Check out the URL for ALL movies to see the whole list.".format(movie.title, director.name)

@app.route('/all_movies')
def all_movies():
    all_movies = [] # Will be be tuple list of title, genre
    movies = Movie.query.all()
    for m in movies:
        director = Director.query.filter_by(id=m.director_id).first() # get just one artist instance
        all_movies.append((m.title,director.name, m.genre)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!

@app.route('/all_directors')
def all_directors():
    directors = Director.query.all()
    names = []
    for d in directors:
        num_movies = len(Movie.query.filter_by(director_id=d.id).all())
        newtup = (d.name,num_movies)
        names.append(newtup) # names will be a list of tuples
    return render_template('all_directors.html',director_names=names)

@app.route('/movie/new', methods=['POST', 'GET']) ## NEW ROUTE 2 FOR FINAL PROJECT
def new_movie_form(): #source: https://stackoverflow.com/questions/27367233/how-can-print-input-from-flask-wtform-to-html-with-sqlalchemy
    form = UpdateForm(request.form)
    movie = Movie()
    #form.populate_obj(movie)
        #director = get_or_create_director(director)
        #movie = Movie(title=title, director_id=director.id,genre=genre, imdb_rating = imdb_rating)
        #session.add(movie)
        #session.commit()
    director = get_or_create_director(form.director.data)
    movie.title = form.title.data
    movie.director_id = director.id
    movie.genre = form.genre.data
    movie.imdb_rating = form.imdb_rating.data
    session.add(movie)
    session.commit()
    return render_template('form.html', form=form)

@app.route('/top_movies') ## NEW ROUTE 3 FOR FINAL PROJECT
def see_top_movies():
    top_movies = []
    movies = Movie.query.all()
    for m in movies:
        director = Director.query.filter_by(id=m.director_id).first()
        imdb = float(m.imdb_rating)
        if imdb >= 8.0:
            top_movies.append((m.title, director.name, m.imdb_rating, m.genre))
    return render_template('all_movies.html', all_movies = top_movies)

@app.route('/ratings/visualized')
def see_ratings():
    movie_ratings = []
    movies = Movie.query.all()
    for m in movies:
        movie_ratings.append(m.imdb_rating)
    img = io.BytesIO()
    plt.hist(movie_ratings)
    plt.xlabel('Ratings')
    plt.title('Distribution of Ratings Among Movies in this Database')
    plt.savefig(img, format = 'png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)




if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
