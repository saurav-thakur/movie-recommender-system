import os
import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()

st.title("Movie Recommender System")

df = pickle.load(open("./pickle_files/moviesdict.pkl","rb"))
similarity = pickle.load(open("./pickle_files/similarity_matrix.pkl","rb"))
df = pd.DataFrame(df)

API_Key = os.environ["tmdb_api_key"]
# st.write(API_Key)

def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_Key}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data["poster_path"]
    full_poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_poster_path

def recommend_movie(df,movie_name,top_n_movies=5):
    index = df[df['title'] == movie_name].index[0]
    posters = []
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:top_n_movies]:
        st.write(df.iloc[i[0]].title)
        st.image(fetch_posters(df.iloc[i[0]].movie_id))

top_n_movies = st.slider("How many number of movies do you want to be recommended?",min_value=5,max_value=20,step=1)

chosen_option = st.selectbox("Enter the movie name",(
    df["title"].values
))

if st.button("Recommend"):
    recommend_movie(df,chosen_option,top_n_movies=top_n_movies)