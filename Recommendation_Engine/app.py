# py -m streamlit run
import pickle
import pandas as pd
import streamlit as st
import requests
from PIL import Image

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=86bf0702c85c82e8bb060d171cdc6552".format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance=similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie = []
    recommended_posters = []
    for i in movie_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_posters.append(fetch_poster(movie_id))
        recommended_movie.append(movies.iloc[i[0]].title)

    return recommended_movie,recommended_posters

st.header('Movie Recommendation System')
movies_list = pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))

select_option = st.selectbox(
    "How would you like ? ",
    movies['title'].values
)

if st.button('Recommend'):

    recommended_movie,recommended_posters = recommend(select_option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie[0])
        st.image(recommended_posters[0])
    with col2:
        st.text(recommended_movie[1])
        st.image(recommended_posters[1])

    with col3:
        st.text(recommended_movie[2])
        st.image(recommended_posters[2])
    with col4:
        st.text(recommended_movie[3])
        st.image(recommended_posters[3])
    with col5:
        st.text(recommended_movie[4])
        st.image(recommended_posters[4])
        