import aiohttp
import os
import pandas as pd
import time
from dotenv import load_dotenv
import asyncio

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
            data.append({key: movie_info.get(key, None) for key in information_needed})
    df = pd.DataFrame(data)
    return df

start_time = time.time()
movies = pd.read_csv("data/movie_ids.csv")["id"].tolist()

res = get_pd_df(movies[:100])

for i in range(100, len(movies), 100):
    print(i)
    data_frame = get_pd_df(movies[i : i + 100])
    res = pd.concat([res, data_frame], ignore_index=True)
    if i % 10000 == 0:
        res.to_csv("data/async_movie_db.csv")

res.to_csv("data/async_movie_db.csv")
print(f"End time {time.time() - start_time}")
