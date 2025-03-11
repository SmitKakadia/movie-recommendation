import pickle
import streamlit as st
import requests
import gdown  # Added for Google Drive download
import os

# Google Drive file ID for similarity.pkl
SIMILARITY_FILE_ID = "1wqcBbd5273njEgpne57WQDGfsMSyLhZu"

# Download similarity.pkl from Google Drive if not already present
if not os.path.exists('similarity.pkl'):
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", 'similarity.pkl', quiet=False)

# Load the preprocessed data
movies_df = pickle.load(open('movie_list.pkl', 'rb'))  # Directly from your GitHub repo
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Loaded from Google Drive

# Fetch poster function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    
    if data.get('poster_path'):  # Handle missing posters
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder image

# Recommendation logic
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_names.append(movies_df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('Movie Recommender System')

movie_list = movies_df['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    cols = st.columns(5)  # Updated from `st.beta_columns(5)`
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
