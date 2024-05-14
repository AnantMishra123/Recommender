import aiohttp
import os
import pandas as pd
import time
from dotenv import load_dotenv
import asyncio
import polars as pl

load_dotenv()

api_key = os.getenv("tmdb_api_2")

information_needed = ['adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id',
                     'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path',
                     'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime',
                     'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count',
                     'keywords', 'credits']

async def fetch_movie(session, id):
    try :
        async with session.get(f"https://api.themoviedb.org/3/movie/{id}", params={"api_key": api_key, "append_to_response": "keywords,credits"}, timeout=30) as response:
            try:
                return await response.json()
            except Exception as e:
                print(f"Error fetching movie {id}: {e}")
                return None
    except Exception as e:
        print(f"Error fetching movie {id}: {e}")
        return None 
async def get_movies(movies):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_movie(session, id) for id in movies]
        return await asyncio.gather(*tasks)

def get_pd_df(movies):
    loop = asyncio.get_event_loop()
    movies_data = loop.run_until_complete(get_movies(movies))
    data = []
    for i, movie_info in enumerate(movies_data):
        if movie_info:
            data.append({key: movie_info.get(key, "") for key in information_needed})
    df = pd.DataFrame(data)
    return df

def append_to_file(src, dst):
    with open(src, "r") as s:
        s.readline()
        content = s.read()
        with open (dst, "a") as d:
            d.write(content)
    

start_time = time.time()
movies = list(pd.read_csv("data/movie_ids.csv")["id"])
movies.sort()
res = get_pd_df([movies[100000]])
res.head(0).to_csv("data/async_movie_db_100K_200K.csv")

reset = False
for i in range(100000, 200000, 100):
    data_frame = get_pd_df(movies[i : i + 100])
    if reset:
        res = data_frame
        reset = False
    else:
        res = pd.concat([res, data_frame], ignore_index=True)
    if i % 1000 == 0:
        print(i)
        res.to_csv("temp/temp_movies.csv")
        append_to_file("temp/temp_movies.csv", "data/async_movie_db_100K_200K.csv")
        reset = True

print(f"End time {time.time() - start_time}")