import os
import json
import numpy as np
import pandas as pd
from typing import List

from flask import Flask, render_template, request, redirect, send_file, jsonify, make_response
from recommender.recommender import recommendMovies
from tmdb import getMovieDetails

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    resp = make_response(render_template("index.html"))

    # items = request.cookies.get('rated-movies')
    # print("cookie", items)
    # if items is None:
    resp = reset_ratings(resp)
    return resp

def reset_ratings(response):
    response.set_cookie('rated-movies', json.dumps({}))
    return response

@app.route('/add-item', methods=['POST'])
def add_item():
    new_item = request.form.get('movie_id')
    new_rating = request.form.get('movie_rating')
    items = request.cookies.get('rated-movies')
    if items == "":
        items = {}
    else:
        items = json.loads(items)
    items[new_item] = new_rating

    rec_flag = int(request.form.get('recommend'))
    if rec_flag == True:
        carousel_items = json.loads(request.form.get('carousel_movies'))
        movies_data = recommendMoviesWrapper(items, carousel_items, 8)
        response = {'movies': movies_data}
    else:
        response = {}

    response = make_response(jsonify(response))
    response.set_cookie('rated-movies', json.dumps(items))
    return response

def recommendMoviesWrapper(rated_movies, carousel_movies, n_items):
    liked_movies = [int(k) for k,v in rated_movies.items() if int(v) > 2]
    skipped_movies = [int(k) for k,v in rated_movies.items() if int(v) < 2]
    skipped_movies.extend(carousel_movies)

    recommended_movies = recommendMovies(liked_movies, skipped_movies, n_items)

    movies_data = []
    for movie_id in recommended_movies:
        movie_data = getMovieDetails(movie_id)
        if movie_data[0]:
            movies_data.append(movie_data[1:])

    return movies_data

def recommendMoviesWrapperv2(liked_movies, carousel_movies, n_items):
    liked_movies = [int(k) for k in liked_movies]
    recommended_movies = recommendMovies(liked_movies, carousel_movies, n_items)
    
    print("recommended_movies", recommended_movies, len(recommended_movies))

    movies_data = []
    for movie_id in recommended_movies:
        movie_data = getMovieDetails(movie_id)
        print(movie_data[0], movie_data[1])
        if movie_data[0]:
            movies_data.append(movie_data[1:])

    return movies_data


@app.route('/getMovies', methods=['GET'])
def getMovies():
    rated_movies = request.cookies.get('rated-movies')
    rated_movies = json.loads(rated_movies)
    movies_data = recommendMoviesWrapper(rated_movies, [], 18)
    
    print(len(movies_data))
    return jsonify({'movies': movies_data})

@app.route('/getMoviesv2', methods=['GET'])
def getMoviesv2():
    rated_movies = json.loads(request.args["param1"])
    print("get movies", rated_movies)
    
    movies_data = recommendMoviesWrapperv2(rated_movies, [], 10)
    print(len(movies_data))
    return jsonify({'movies': movies_data})



if __name__ == '__main__':
    app.run(debug=True, port=80)