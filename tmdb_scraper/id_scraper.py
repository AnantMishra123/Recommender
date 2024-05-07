import requests
import os
from dotenv import load_dotenv
import pandas as pd
import json 

load_dotenv()


api_key = os.getenv("tmdb_api")

information_needed = ['adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 
 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'production_companies', 
 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count', 'keywords', 'credits']

def get_movie(id:int):
    request = requests.get(f"https://api.themoviedb.org/3/movie/{id}", params={"api_key":api_key, "append_to_response":"keywords,credits"})
    
    if request.status_code == 200:
        print(request.json()["title"])
    with open("temp.json", "w") as file:
        json.dump(request.json(), file)
    

get_movie(600)


