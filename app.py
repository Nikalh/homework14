from flask import Flask, jsonify

from utils import get_movie_by_title, get_movie_by_years, get_movie_by_rating, get_movie_by_genre

app = Flask(__name__)


@app.route("/movies/title/<movie_title>")
def page_movies(movie_title):
    movie = get_movie_by_title(movie_title)
    return jsonify(movie)


@app.route("/movies/year/to/year/<int:year1>/<int:year2>")
def page_movies_years(year1, year2):
    movie = get_movie_by_years(year1, year2)
    return movie


@app.route("/movies/rating/<rating>")
def page_movies_rating(rating):
    movie = get_movie_by_rating(rating)
    return movie

@app.route("/movies/genre/<genre>")
def page_movies_genre(genre):
    movie = get_movie_by_genre(genre)
    return jsonify(movie)
