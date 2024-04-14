import numpy as np
import pandas as pd
import random
from collections import Counter
from recommender.candidate_gen import CandidateGeneration

movies_df = pd.read_csv("data/movies_data_v2.csv")
cg = CandidateGeneration("data/movies_data_v2.csv")

def get_popular_movies():
    genres_set = Counter(movies_df['genres']).most_common(20)
    top_genres = [g[0] for g in genres_set[:10]]

    popular_movies = []
    well_known_movies = movies_df[movies_df['total_ratings'] > 1000]
    for genre in top_genres:
        popular_movies.append(well_known_movies.loc[well_known_movies['genres'] == genre, :].sort_values(["average_rating", "total_ratings"], ascending=False).head(10))
    # print(popular_movies)
    popular_movies = pd.concat(popular_movies, axis=0)
    return popular_movies

def getRandomMovies(n, df):
    sampled_df = df.sample(n)
    sampled_tmdb_ids = sampled_df['tmdbId']
    return sampled_tmdb_ids

def recommendMovies(liked_movies, skipped_movies, n):
    # print("Liked Movies", type(liked_movies))
    # print("Skipped Movies", type(skipped_movies))
    excluded_movies = set(skipped_movies + liked_movies)
    popular_movies = [movie for movie in cg.get_popular_candidates(50) if movie not in excluded_movies]
    
    if len(liked_movies) > 2:
        candidate_movies = generateCandidates(liked_movies, skipped_movies)
        candidate_movies = [movie for movie in candidate_movies if movie not in excluded_movies]
        # n_candidates = min(len(candidate_movies), (9*n)//10)
        output_movies = candidate_movies # [:n_candidates] #+ popular_movies[:n-n_candidates]
    else:
        output_movies = popular_movies
    
    random.shuffle(output_movies)
    return output_movies[:n]

def generateCandidates(liked_movies, skipped_movies):
    k_similar = 4
    candidates = []
    
    for movie_id in liked_movies:
        candidates.extend(cg.get_similar_candidates(movie_id, k_similar))
    # print("Candidate Movies --", candidates)
    
    candidates = sorted(candidates, key=lambda x: x[1])
    similar_movies = [movie_id for movie_id, dist in candidates]
    return similar_movies
