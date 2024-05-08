import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time
load_dotenv()


api_key = os.getenv("tmdb_api")

information_needed = ['adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 
 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'production_companies', 
 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count', 'keywords', 'credits']

def get_movie(id:int):
    request = requests.get(f"https://api.themoviedb.org/3/movie/{id}", params={"api_key":api_key, "append_to_response":"keywords,credits"})
    return request.json()


def get_pd_df(movies:list[int]):
    data = []
    for i, id in enumerate(movies):
        if i % 1000 == 0:
            print(i)
        movie_info = get_movie(id)
        if movie_info:
            data.append({key: movie_info.get(key, None) for key in information_needed})
    df = pd.DataFrame(data)
    return df

start_time = time.time()
movies = pd.read_csv("tmdb_scraper/movie_ids.csv")["id"]
data_frame = get_pd_df(movies)
data_frame.to_csv("movie_db.csv")
print(f"End time {time.time() - start_time}")
