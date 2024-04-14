# Candidate Generation
# Heuristic/ Content based methods.

# 1. Top K_genre movies of each genre. Extra movies for genres preferred by user (average rating over a threshold).
# 2. K_contemporary movies for movies around the years preferred by user (get maybe 2 clusters of years and pick popular movies in those year clusters)
# 3. K_simiar movies per each well rated movie from item-item embeddings -- faiss
# 4. K_popular in general popular movies.

# Filter duplicates and pass on to reranking.

import numpy as np
import pandas as pd
import random
from collections import Counter
import faiss
import json


class CandidateGeneration:
    def __init__(self, movies_data_path):
        self.movies_data_path = movies_data_path
        self.load_movies_dataset()
        self.create_candidates_corpus()
        self.load_movies_embeddings()

    def load_movies_dataset(self):
        self.movies_df = pd.read_csv(self.movies_data_path)
        self.movie_id_to_tmdb_id = {row['movieId']: row['tmdbId'] for _,row in self.movies_df.iterrows()}
        self.tmdb_id_to_movie_id = {row['tmdbId']: row['movieId'] for _,row in self.movies_df.iterrows()}

        self.movies_df = self.movies_df[self.movies_df['total_ratings'] > 100]
        self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: x.strip().split("|"))

    def load_movies_embeddings(self):
        self.movie_embeddings = np.load("data/movie_embeddings.npy")
        self.index = faiss.IndexFlatL2(16)
        self.index.add(self.movie_embeddings)
        self.movie_id_to_embed_idx = json.load(open("data/movie_id_map.json", "r"))
        self.movie_id_to_embed_idx = {int(k): int(v) for k,v in self.movie_id_to_embed_idx.items()}

        self.tmdb_id_to_embed_idx = {self.movie_id_to_tmdb_id[k]:v for k,v in self.movie_id_to_embed_idx.items()}
        self.embed_idx_to_tmdb_id = {v:self.movie_id_to_tmdb_id[k] for k,v in self.movie_id_to_embed_idx.items()}


    def get_genre_candidates(self, genre, k=5):
        candidates = self.genre_candidates.get_group(genre).head(k)
        return list(candidates['tmdbId'])
    
    def get_contemporary_candidates(self, year, offset=1, k=3):
        candidates = []
        for t in range(year-offset, year+offset+1):
            t_candidates = self.year_candidates.get_group(t).reset_index()
            candidates.append(t_candidates)

        candidates = pd.concat(candidates, axis=0)
        return list(candidates['tmdbId'])

    def get_popular_candidates(self, k=10):
        popular_candidates = list(self.popular_movies.sample(k)['tmdbId'].values)
        return [movie for movie in popular_candidates if movie in self.tmdb_id_to_embed_idx]

    def get_similar_candidates(self, movie_id, k=3):
        query_embed = np.expand_dims(self.movie_embeddings[self.tmdb_id_to_embed_idx[movie_id]], 0)
        D, I = self.index.search(query_embed, k)
        candidates = zip(I[0], D[0])
        return candidates

    def create_candidates_corpus(self):
        _separate_genres_df = self.movies_df.explode('genres')
        genres_set = Counter(_separate_genres_df['genres']).most_common(50)
        top_genres = [g[0] for g in genres_set if g[1] > 1000]

        self.genre_candidates = _separate_genres_df[_separate_genres_df['genres'].isin(top_genres)]\
                                            .sort_values(["average_rating"], ascending=False)\
                                            .groupby(['genres']).head(100).groupby(['genres'])
        
        self.popular_movies = self.movies_df.sort_values(["average_rating"], ascending=False).head(150)
        self.year_candidates = self.movies_df.sort_values(['average_rating'], ascending=False).groupby(['year']).head(5).groupby(['year'])
        

if __name__ == "__main__":
    cg = CandidateGeneration("data/movies_data_v2.csv")
    print(cg.get_similar_candidates(567))