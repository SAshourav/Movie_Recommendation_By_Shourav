import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=315554d537704de2702d592a480e536c&language=en-US'.format(movie_id))
    data = response.json()

    # Debugging print statement
    print("API Response Data:", data)

    # Check if 'poster_path' key is present in the dictionary
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # Debugging print statement
        print("Missing 'poster_path' key in API response.")
        # Provide a default poster URL or handle the case where 'poster_path' is missing
        return "https://example.com/default_poster.jpg"
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = i[0]
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Wanna get movie Suggestion ?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.header(names[i])
            st.image(posters[i])


