import requests

def getMovieDetails(tmdb_id):
    r = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}', params={'api_key': 'c3d8153074130e5ea68224a4e50f9883'})
    data = r.json()

    success = data.get('success', True)
    name = data.get('title', "")
    if len(name) > 30:
        name = name[:27] + "..."

    plot = data.get('overview', "")
    genre = data.get('genres', None)
    if genre is None or len(genre) == 0:
        genre = "None"
    else:
        genre = genre[0]['name']

    try:
        poster_url = f'https://image.tmdb.org/t/p/w185{data["poster_path"]}'
    except:
        poster_url = ""
        success = False
    return success, name, plot, genre, poster_url, str(tmdb_id)