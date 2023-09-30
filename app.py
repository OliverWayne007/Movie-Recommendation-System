import pickle
import requests
import streamlit as st
import pandas as pd
import csv

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def Recommend(selected_movie_name):
    index = df[df['title'] == selected_movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.title('Movie Recommendation System')

# Load the list from the CSV file
with open('movies_list.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    movies_list = next(reader)

# Display the list in Streamlit
# st.write("List from Jupyter Notebook:", movies_list)

# Reading the "movies_dataframe.csv" file into a dataframe df
df = pd.read_csv("movies_dataframe.csv")
# st.dataframe(df)

# Loading the pickle file containing the similarity matrix containing the cosine-similarity scores
similarity = pickle.load(open('similarity.pkl' , 'rb'))


selected_movie_name = st.selectbox('Select a movie' , movies_list);

# Creating a Recommend button
recommend_button_clicked = st.button("Show Recommendation")

if recommend_button_clicked:
    recommended_movies_titles , recommended_movies_posters = Recommend(selected_movie_name)
    st.subheader("Top-5 recommended movies")

    # for i in recommended_movies_titles:
    #     st.write(i)

    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    with col1:
        st.text(recommended_movies_titles[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies_titles[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies_titles[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies_titles[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies_titles[4])
        st.image(recommended_movies_posters[4])