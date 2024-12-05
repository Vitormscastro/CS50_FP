import streamlit as st  
import pandas as pd  
from content_based_game_recommendation_system import find_closest_games, get_recommendations, combined_similarity 

# Load the dataset  
@st.cache  
def load_data():  
    return pd.read_csv('games_description_cleaned.csv')

df = load_data()  

# Title and description  
st.title("Steam Game Recommendation System")  
st.write("Enter the name of a game to get recommendations based on its description, genres, and ratings.")  

# User input  
game_name = st.text_input("Enter a game name:")  

if game_name:  
    # Find closest matches  
    closest_matches = find_closest_games(game_name, df)  
    if not closest_matches:  
        st.error(f"No games found similar to '{game_name}'. Please try again.")  
    else:  
        # Display closest matches  
        st.write("Closest matches found:")  
        selected_game = st.selectbox("Select the correct game:", closest_matches)  

        if selected_game:  
            # Generate recommendations  
            selected_game, recommendations = get_recommendations(selected_game, df, combined_similarity)  
            st.write(f"Recommendations for '{selected_game}':")  
            for i, rec in enumerate(recommendations, 1):  
                st.write(f"{i}. {rec}")