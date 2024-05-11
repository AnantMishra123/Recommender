import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time
load_dotenv()


api_key = os.getenv("tmdb_api_2")

information_needed = ['adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 
 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'production_companies', 
 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count', 'keywords', 'credits']

def get_movie(id:int):
    try:
        request = requests.get(f"https://api.themoviedb.org/3/movie/{id}", params={"api_key":api_key, "append_to_response":"keywords,credits"})
    except Exception:
        print(f"Error!!")
        return None
    if request.status_code != 200:
        return None
    return request.json()


def get_pd_df(movies:list[int]):
    data = []
    prev_time = time.time()
    for i, id in enumerate(movies):
        if i % 10 == 0:
            new_time = time.time()
            print(i, new_time - prev_time)
            prev_time = new_time
        movie_info = get_movie(id)
        if movie_info:
            data.append({key: movie_info.get(key, None) for key in information_needed})
    df = pd.DataFrame(data)
    return df

start_time = time.time()
movies = pd.read_csv("data/movie_ids.csv")["id"][:100000]
data_frame = get_pd_df(movies)
data_frame.to_csv("data/movie_db.csv")
print(f"End time {time.time() - start_time}")
