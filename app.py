import streamlit as st
import pickle
import pandas as pd
import requests
import time

api_key = st.secrets["api_key"]

def recommend_movies(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US".format(movie_id, api_key)
    headers = {"accept": "application/json"}
    print(url)
    data = requests.get(url, headers=headers)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

st.title('Movie Recommender System')

movies = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity_dict.pkl','rb'))
movies_df = pd.DataFrame(movies)
movies_list = movies_df['title'].values

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list
)

if st.button("Recommend", type="primary"):
    time.sleep(2)
    recommended_movie_names,recommended_movie_posters = recommend_movies(selected_movie_name)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    col = st.columns(1)
    with col:
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])
