# Game Recommendation System  

#### Video Demo: [(https://www.youtube.com/watch?v=cJ_o4oep8Q4)]  

#### Description:  
The **Game Recommendation System** is a web-based application designed to help users discover new games based on their preferences. Built using **Streamlit**, **Python**, and **pandas**, this project leverages content-based filtering techniques to recommend games similar to the ones users already enjoy. The system analyzes game descriptions, genres, and player ratings to generate personalized recommendations.  

This project was developed as the final submission for **CS50x**, showcasing the skills and concepts learned throughout the course, including programming, data analysis, and software development.  

---  

## Features:  
1. **Game Search**:  
   - Users can input the name of a game they like, and the system will find the closest matches from the dataset.  
   - A dropdown menu allows users to select the correct game if multiple matches are found.  

2. **Personalized Recommendations**:  
   - The system provides a list of recommended games based on the selected game.  
   - Recommendations are generated using a **content-based filtering algorithm** that combines:  
     - **Game descriptions** (analyzed using TF-IDF and cosine similarity).  
     - **Genres** (encoded and compared using cosine similarity).  
     - **Player ratings** (normalized and weighted).  

3. **Interactive Web Interface**:  
   - Built with **Streamlit**, the app provides a clean and user-friendly interface.  
   - Users can interact with the app in real-time to explore recommendations.  

4. **Dataset Integration**:  
   - The app uses a preprocessed dataset of games, including fields such as:  
     - Game name  
     - Short description  
     - Genres  
     - Overall player ratings  
   - The dataset is cleaned and normalized to ensure accurate recommendations.  

5. **Scalability**:  
   - The app is designed to handle large datasets efficiently, making it suitable for future expansion with more games or additional features.  

---  

## Technical Details:  
### **Technologies Used**:  
- **Python**: The core programming language for data processing and recommendation logic.  
- **Streamlit**: For building the interactive web application.  
- **pandas**: For data manipulation and preprocessing.  
- **scikit-learn**: For implementing TF-IDF vectorization and cosine similarity.  
- **Altair**: (Optional) For visualizing data trends or distributions.  

### **Recommendation Algorithm**:  
The recommendation system uses a **content-based filtering approach**:  
1. **TF-IDF Vectorization**:  
   - Game descriptions are vectorized using the TF-IDF (Term Frequency-Inverse Document Frequency) technique to capture the importance of words in each description.  
   - Cosine similarity is calculated between games based on their TF-IDF vectors.  

2. **Genre Encoding**:  
   - Game genres are encoded using a multi-label binarizer, and cosine similarity is calculated between genre vectors.  

3. **Player Ratings**:  
   - Player ratings are normalized using Min-Max scaling and incorporated into the similarity calculation.  

4. **Combined Similarity**:  
   - A weighted combination of description similarity, genre similarity, and player ratings is used to generate the final similarity score:  
     ```  
     combined_similarity = 0.4 * description_similarity + 0.4 * genre_similarity + 0.2 * normalized_ratings  
     ```  

---  

## How to Run the Project:  
### **Locally**:  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-username/game-recommendation-system.git  
   cd game-recommendation-system