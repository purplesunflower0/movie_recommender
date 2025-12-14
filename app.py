
#
# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
#
# # ---------- POSTER FETCH (FIXED & SAFE) ----------
# @st.cache_data(show_spinner=False)
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=60547b911eac77f541a3427c6b196f85&language=en-US"
#
#     try:
#         response = requests.get(url, timeout=5)
#         data = response.json()
#
#         poster_path = data.get('poster_path')
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500" + poster_path
#
#     except requests.exceptions.RequestException:
#         pass
#
#     # fallback image (never crashes)
#     return "https://via.placeholder.com/300x450?text=No+Poster"
#
#
# # ---------- RECOMMENDER ----------
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#
#     similar_movies = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]  # 5 movies
#
#     recommended_movies = []
#     recommended_movies_posters = []
#
#     for i in similar_movies:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies, recommended_movies_posters
#
#
# # ---------- LOAD DATA ----------
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
#
# # ---------- UI ----------
# st.title("Movie Recommendation System")
#
# movie_selected = st.selectbox(
#     "Search a Movie",
#     movies['title'].values
# )
#
# if st.button("Recommend"):
#     names, posters = recommend(movie_selected)
#
#     cols = st.columns(len(names))
#
#     for col, name, poster in zip(cols, names, posters):
#         with col:
#             st.text(name)
#             st.image(poster)

# import streamlit as st
# import pickle
# import pandas as pd
#
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#
#     similar_movies = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]
#
#     return [movies.iloc[i[0]].title for i in similar_movies]
#
#
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl','rb'))
#
#
# st.title("Movie Recommendation System")
#
# movie_selected = st.selectbox(
#     "Search a Movie",
#     movies['title'].values
# )
#
# if st.button("Recommend"):
#     recommendations = recommend(movie_selected)
#     for movie in recommendations:
#         st.write(movie)

import pickle

import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)


# ---------- RECOMMENDER (UNCHANGED) ----------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    similar_movies = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies.iloc[i[0]].title for i in similar_movies]


# ---------- LOAD DATA ----------
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl','rb'))
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)



# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
    }

    h1 {
        color: #E50914;
        text-align: center;
        margin-bottom: 30px;
    }

    .movie-card {
        background-color: #262730;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 17px;
        transition: transform 0.2s ease;
    }

    .movie-card:hover {
        transform: scale(1.02);
        background-color: #32343a;
    }

    .stButton > button {
        background-color: #E50914;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        font-size: 16px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------- UI ----------
st.title("🎬 Movie Recommendation System")

movie_selected = st.selectbox(
    "Search a movie you like",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations = recommend(movie_selected)

    st.subheader(f"Movies similar to **{movie_selected}**")

    for movie in recommendations:
        st.markdown(
            f"""
            <div class="movie-card">
                🎥 {movie}
            </div>
            """,
            unsafe_allow_html=True
        )











