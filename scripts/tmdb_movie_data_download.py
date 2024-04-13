import requests
import json
import numpy as np
import time
from tqdm import tqdm


def download_movie_data():
    list_of_movies = open("movie_ids_05_15_2023.json", encoding="utf8")
    movie_count = 0
    bar = tqdm(list_of_movies.readlines())
    for row in bar:
        if len(row) == 0:
            break

        # if movie_count % 30 == 0:
        #     time.sleep(1)
        
        movie_data = json.loads(row)
        if movie_data['popularity'] >= 1.0:
            r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_data["id"]}', params={'api_key': 'c3d8153074130e5ea68224a4e50f9883'})
            data = r.json()

            success = data.get('success', True)
            if success:
                outfp = open(f"movie_data_dir/{movie_data['id']}.json", "w", encoding="utf8")
                json.dump(data, outfp)
                movie_count += 1

        bar.set_description_str(f"Saved {movie_count} movies")
    print("Done! Saved {movie_count} movies")


if __name__ == "__main__":
    download_movie_data()