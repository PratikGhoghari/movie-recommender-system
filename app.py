import streamlit as st
import pickle
import pandas as pd
import requests

def recommend_movies(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    recommended_movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in recommended_movies_list:
        print(i)
        movie_id = i[0]
        print(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def fetch_poster(movie_id):
    #url = "https://api.themoviedb.org/3/movie/{0}?api_key=e8c69a1872920bf163dcecdd98c19d46&language=en-US".format(movie_id)
    url = "https://api.themoviedb.org/11/movie/movie_id?language=en-US"
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
    recommended_movie_names,recommended_movie_posters = recommend_movies(selected_movie_name)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
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
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
