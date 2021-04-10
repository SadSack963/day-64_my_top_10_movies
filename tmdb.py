# Attribution:
# This product uses the TMDb API but is not endorsed or certified by TMDb.

import requests
import os
from dotenv import load_dotenv

load_dotenv("E:/Python/EnvironmentVariables/.env")
TMDB_API_KEY = os.getenv('API_Key_v3Auth_TMDB')
TMDB_BEARER_TOKEN = os.getenv('API_Key_v4Auth_TMDB')


"""
Finding Data
============
There are 3 ways to search for and find movies, TV shows and people on TMDb. They're outlined below.

/search - Text based search is the most common way. You provide a query string and we provide the closest match. 
    Searching by text takes into account all original, translated, alternative names and titles.

/discover - Sometimes it useful to search for movies and TV shows based on filters or definable values like ratings, 
    certifications or release dates. The discover method make this easy. For some example queries, and to get an idea 
    about the things you can do with discover, take a look here.

/find - The last but still very useful way to find data is with existing external IDs. For example, if you know 
    the IMDB ID of a movie, TV show or person, you can plug that value into this method and we'll return anything 
    that matches. This can be very useful when you have an existing tool and are adding our service to the mix.
"""


def search_movie(title):
    url = 'https://api.themoviedb.org/3/search/movie'

    query = {
        'api_key': TMDB_API_KEY,
        'query': title,  # URI encoded
    }

    # https://developers.themoviedb.org/4/getting-started
    header = {
        'Authorization': f'Bearer {TMDB_BEARER_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }

    response = requests.get(url,params=query, headers=header)
    response.raise_for_status()

    # print(response.json())
    return response.json()


def get_movie_info(movie_id):
    url = 'https://api.themoviedb.org/3/movie/'

    query = {
        'api_key': TMDB_API_KEY,
    }

    header = {
        'Authorization': f'Bearer {TMDB_BEARER_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }
    response = requests.get(url + movie_id, params=query, headers=header)
    response.raise_for_status()

    return response.json()
