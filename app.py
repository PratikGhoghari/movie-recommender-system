import streamlit as st
import pickle
import pandas as pd
import requests
import time
import lzma
import shutil
import os

api_key = st.secrets["api_key"]


def decompress_lzma(input_lzma, output_file):
    # Check if the decompressed file already exists
    if os.path.exists(output_file):
        print(f"The decompressed file {output_file} already exists. Skipping decompression.")
    else:
        # Decompress the .lzma file
        with lzma.open(input_lzma, 'rb') as f_in, open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"File {input_lzma} has been successfully decompressed to {output_file}.")

def read_pickle(file_path):
    # Read the decompressed pickle file
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    print("Pickle file read successfully.")
    return data


def recommend_movies(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    decompress_lzma(input_lzma="compressed_similarity_scores.pkl.gz", output_file="decompressed_similarity_scores.pkl")
    similarity = read_pickle(file_path="decompressed_similarity_scores.pkl")
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
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

    # Row 2
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
    with col6:
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])
    with col7:
        st.text(recommended_movie_names[6])
        st.image(recommended_movie_posters[6])
    with col8:
        st.text(recommended_movie_names[7])
        st.image(recommended_movie_posters[7])