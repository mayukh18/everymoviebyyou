# Movie Reco App

### Requirements:

1. Given a set of rated movies, the app should be able to recommend a new set of movies. (**Functional Req**)
2. The recommendation latency should be minimum for a t2.micro (1 GB RAM, No GPU) (**Non-Functional Req**)

## Design

Two tiered pipeline: Candidate generation and reranking.
Make content generation modular -- multiple methods (heuristic or not) generating a set number of candidates. All the candidates ultimately get fed to the reranking block where the candidates get ranked and we return the top N items.

### Candidate Generation

Heuristic/ Content based methods.

1. Top K_genre movies of each genre.
2. Extra K_genre_extra movies for genres preferred by user (average rating over a threshold).
3. K_contemporary movies for movies around the years preferred by user (get maybe 2 clusters of years and pick popular movies in those year clusters)
4. K_simiar movies per each well rated movie from item-item embeddings -- faiss
5. K_popular in general popular movies.

Filter duplicates and pass on to reranking.

