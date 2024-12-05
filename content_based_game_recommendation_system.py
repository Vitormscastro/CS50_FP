
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from difflib import get_close_matches

# Load the cleaned dataset
df = pd.read_csv('games_description_cleaned.csv')

# Ensure 'genres' is a list (if not already processed)
df['genres'] = df['genres'].str.replace(r"[\[\]']", "", regex=True).str.split(", ")

# Step 1: Vectorize the 'short_description' column
vectorizer = TfidfVectorizer(stop_words='english')  # Remove common stop words
tfidf_matrix = vectorizer.fit_transform(df['short_description'])

# Step 2: Compute cosine similarity for descriptions
description_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 3: Compute genre similarity (if genres are one-hot encoded)
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(df['genres'])
genre_similarity = cosine_similarity(genres_encoded, genres_encoded)

# Step 4: Normalize 'overall_player_rating'
scaler = MinMaxScaler()
df['overall_player_rating_normalized'] = scaler.fit_transform(df[['overall_player_rating']])

# Step 5: Combine similarity scores
# Example weights: 0.4 for description, 0.4 for genres, 0.2 for ratings
combined_similarity = (
    0.4 * description_similarity +
    0.4 * genre_similarity +
    0.2 * df['overall_player_rating_normalized'].values[:, None]
)

# Function to find the closest matching game names
def find_closest_games(game_name, df):
    """
    Finds the closest matching game names in the dataset.

    Parameters:
        game_name (str): The game name entered by the user.
        df (pd.DataFrame): The dataset containing game information.

    Returns:
        list: A list of closest matching game names.
    """
    game_names = df['name'].tolist()
    closest_matches = get_close_matches(game_name, game_names, n=5, cutoff=0.4)
    return closest_matches

# Function to recommend games
def recommend_games(game_name, df, similarity_matrix, top_n=5):
    """
    Recommends games similar to the given game name.

    Parameters:
        game_name (str): The name of the game to base recommendations on.
        df (pd.DataFrame): The dataset containing game information.
        similarity_matrix (numpy.ndarray): The similarity matrix.
        top_n (int): The number of recommendations to return.

    Returns:
        tuple: The closest matching game name and a list of recommended game names.
    """
    # Find the closest matching game name
    closest_game = find_closest_games(game_name, df)
    if not closest_game:
        return None, f"Game '{game_name}' not found in the dataset."

    # Use the first closest match
    selected_game = closest_game[0]
    game_index = df[df['name'] == selected_game].index[0]

    # Get similarity scores for the game
    similarity_scores = list(enumerate(similarity_matrix[game_index]))

    # Sort games by similarity score (descending order)
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the top N similar games (excluding the input game itself)
    top_games = sorted_scores[1:top_n+1]

    # Return the names of the recommended games
    recommended_games = [df['name'].iloc[i[0]] for i in top_games]
    return selected_game, recommended_games


def find_closest_games(game_name, df):
    # Use difflib to find the closest match from the given game names
    names = df['name'].tolist()
    closest_matches = get_close_matches(game_name, names, n=5, cutoff=0.6)
    return closest_matches

def get_recommendations(game_name, df, combined_similarity, top_n=5):
    closest_matches = find_closest_games(game_name, df)
    if not closest_matches:
        raise ValueError(f"Game '{game_name}' not found in the dataset.")
    selected_game = closest_matches[0]
    game_index = df.index[df['name'] == selected_game].tolist()[0]
    similarities = list(enumerate(combined_similarity[game_index]))
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_similarities[1:top_n+1]]
    recommendations = df.iloc[top_indices]['name'].tolist()
    return selected_game, recommendations
def find_closest_games(game_name, df):
    """
    Finds the closest matching game names in the dataset.

    Parameters:
        game_name (str): The game name entered by the user.
        df (pd.DataFrame): The dataset containing game information.

    Returns:
        list: A list of closest matching game names.
    """
    game_names = df['name'].tolist()
    closest_matches = get_close_matches(game_name, game_names, n=5, cutoff=0.4)
    return closest_matches

def get_recommendations(game_name, df, combined_similarity, top_n=5):
    """
    Recommends games similar to the given game name.

    Parameters:
        game_name (str): The name of the game to recommend similar games for.
        df (pd.DataFrame): The dataset containing game information.
        combined_similarity (numpy.ndarray): The matrix of combined similarity scores.
        top_n (int): The number of top similar games to return.

    Returns:
        tuple: The closest matching game name and a list of recommended game names.
    """
    closest_matches = find_closest_games(game_name, df)
    if not closest_matches:
        return None, f"Game '{game_name}' not found in the dataset."
    
    selected_game = closest_matches[0]
    game_index = df.index[df['name'] == selected_game].tolist()[0]
    similarities = list(enumerate(combined_similarity[game_index]))
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_similarities[1:top_n+1]]
    recommendations = df.iloc[top_indices]['name'].tolist()
    return selected_game, recommendations

if __name__ == "__main__":  
    import sys  

    # Input game name from the user  
    game_name = input("Enter the name of a game: ").strip()  

    try:  
        # Find the closest matches for the input game name  
        closest_matches = find_closest_games(game_name, df)  

        if not closest_matches:  
            print(f"No games found similar to '{game_name}'. Please try again.")  
            sys.exit()  

        # Display the closest matches to the user  
        print("Closest matches found:")  
        for i, match in enumerate(closest_matches, 1):  
            print(f"{i}. {match}")  

        # Ask the user to confirm the correct game  
        selected_index = int(input("Select the correct game by entering the number (1-5): ").strip()) - 1  

        if selected_index < 0 or selected_index >= len(closest_matches):  
            print("Invalid selection. Exiting.")  
            sys.exit()  

        # Get the selected game name  
        selected_game = closest_matches[selected_index]  

        # Generate recommendations for the selected game  
        selected_game, recommendations = get_recommendations(selected_game, df, combined_similarity)  

        # Display the recommendations  
        print(f"\nRecommendations for '{selected_game}':")  
        for i, rec in enumerate(recommendations, 1):  
            print(f"{i}. {rec}")  

    except ValueError as e:  
        print(e)  
    except Exception as e:  
        print(f"An error occurred: {e}")  