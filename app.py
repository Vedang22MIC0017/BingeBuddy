import streamlit as st
import pickle
import pandas as pd
import requests
from pathlib import Path

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / 'style.css'
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# TMDB API to fetch posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    return full_path

# Recommender function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    recommended_movies = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app UI
load_css()

# Add audio player in sidebar
with st.sidebar:
    st.markdown('### Listen to Music While Browsing for Your Next Watch')
    st.markdown('#### Want to be Suprised ?Play the Soundtrack')
    audio_file = open('assets/mission-imposible.mp3', 'rb')
    st.audio(audio_file, format='audio/mp3')

st.markdown('<h1 class="stTitle">🎬 The Binge Buddy</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="app-description">
    Your personal movie companion that helps you discover amazing films based on your taste!
</div>
""", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Which movie have you watched recently?",
    movies['title'].values
)

if st.button('Take me to my next watch'):
    with st.spinner('Finding amazing movies for you...'):
        names, posters = recommend(selected_movie_name)
        
        # Create rows of 3 movies each
        for i in range(0, len(names), 3):
            cols = st.columns(3)
            # Get the movies for this row (up to 3)
            row_movies = list(zip(names[i:i+3], posters[i:i+3]))
            # Fill each column with a movie
            for col, (name, poster) in zip(cols, row_movies):
                with col:
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{poster}" alt="{name}">
                        <div class="movie-title">{name}</div>
                    </div>
                    """, unsafe_allow_html=True)