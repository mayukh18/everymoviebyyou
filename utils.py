import numpy as np
import pandas as pd
import random
from collections import Counter

def create_movies_v2():
    movies_df = pd.read_csv("ml-25m/movies_data.csv")
    ratings = pd.read_csv("ml-25m/ratings.csv")
    movies_df['average_rating'] = movies_df['movieId'].apply(
        lambda x: ratings.loc[ratings['movieId'] == x, 'rating'].mean())
    movies_df['total_ratings'] = movies_df['movieId'].apply(
        lambda x: ratings.loc[ratings['movieId'] == x, 'rating'].count())

    movies_df.to_csv("ml-25m/movies_data_v2.csv", index=False)


if __name__ == "__main__":
    create_movies_v2()