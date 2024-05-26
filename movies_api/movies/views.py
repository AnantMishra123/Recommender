from django.shortcuts import render

import pandas as pd
from ast import literal_eval
from django.http import JsonResponse
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from .groq_api import get_keywords

load_dotenv()

def preprocess(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'\W+|\d+', ' ', text)
    # Remove stopwords and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

def tfidf_search(query, tfidf_matrix, vectorizer):
    query_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix)
    ranked_indices = np.argsort(-similarity_scores).flatten()
    return ranked_indices

def get_movies_from_indices(count, movies, keyword):
    keyword = " ".join(keyword)
    indices = tfidf_search(keyword, tfidf_matrix, vectorizer)
    return movies.iloc[indices[:count]].to_dict(orient='records')

#Booting work
movies = pd.read_csv(os.environ.get("movies_path"))
movies = movies[movies["clean_overview"].isna() == False]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies['clean_overview'])



# Function to handle requests for searching movies based on keywords
# This function expects a GET request with a 'keyword' parameter and optionally a 'count' parameter
# The 'keyword' parameter should contain a list of keywords in string format
# The 'count' parameter specifies the number of top relevant movies to return
# If 'count' is not provided, it defaults to 10
# The function returns a JSON response containing the list of matched movies or an error message
def get_movies(request):
    # Check if the request is a GET request
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required.'}, status=400)

    # Extract keyword from request
    keyword = request.GET.get('keyword')
    if not keyword:
        return JsonResponse({'error': 'Keyword parameter is missing.'}, status=400)

   
    # Extract count from request or use default value of 10
    count = request.GET.get('count', 10)
    try:
        count = int(count)
    except ValueError:
        return JsonResponse({'error': 'Count parameter must be an integer.'}, status=400)

    # Search for movies using the provided keyword
    try:
        keywords = literal_eval(keyword)
        matched_movies = get_movies_from_indices(count, movies, keywords)
        return JsonResponse({'movies': matched_movies}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Function to handle requests for searching movies based on a text prompt
# This function expects a GET request with a 'prompt' parameter
# The 'prompt' parameter should contain a descriptive text from which keywords will be generated
# Optionally, a 'count' parameter can be provided to specify the number of top relevant movies to return
# If 'count' is not provided, it defaults to 10
# The function returns a JSON response containing the list of matched movies, the generated keywords, or an error message
def get_movies_from_prompt(request):
    if request.method != "GET":
        return JsonResponse({'error': 'GET request required.'}, status=400)
    prompt = request.GET.get('prompt')
    if not prompt:
        return JsonResponse({'error': 'Prompt parameter is missing.'}, status=400)
    
    try:
        keywords_json = literal_eval(get_keywords(prompt))

        if not keywords_json.get('keywords'):
            return JsonResponse({'error': 'No keywords generated from the prompt.'}, status=400)

        # Extract count from request or use default value of 10
        count = request.GET.get('count', 10)
        try:
            count = int(count)
        except ValueError:
            return JsonResponse({'error': 'Count parameter must be an integer.'}, status=400)

        keywords =  keywords_json.get('keywords')
        matched_movies = get_movies_from_indices(count, movies, keywords)
        return JsonResponse({'movies': matched_movies, "keywords": keywords_json.get('keywords')}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
