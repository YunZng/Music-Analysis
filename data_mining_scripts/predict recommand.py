import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and preprocess the dataset
def load_and_preprocess(file_path):
    try:
        # Load dataset
        songs = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError("Dataset not found. Please check the file path.")

    # Remove duplicates
    songs.drop_duplicates(subset=['Track Name', 'Artist Name(s)'], inplace=True)

    # Select relevant features
    required_columns = ['Track Name', 'Artist Genres', 'Artist Name(s)', 'Danceability', 'Energy', 'Acousticness', 
                        'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature']
    missing_columns = [col for col in required_columns if col not in songs.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")
    
    songs = songs[required_columns]

    # Drop rows with missing values
    songs.dropna(inplace=True)

    # Helper function to normalize text
    def normalize_text(column):
        return column.apply(lambda x: [word.strip().lower().replace(" ", "") for word in x.split(', ')])

    # Normalize text fields
    songs['Artist Name(s)'] = normalize_text(songs['Artist Name(s)'])
    songs['Artist Genres'] = normalize_text(songs['Artist Genres'])

    # Combine genres and artist names into a single text field
    songs['tags'] = songs['Artist Genres'] + songs['Artist Name(s)']
    songs['tags'] = songs['tags'].apply(lambda x: " ".join(x))

    # Apply TF-IDF vectorization
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectors = tfidf_vectorizer.fit_transform(songs['tags'])

    # Merge TF-IDF features with the original dataset
    tfidf_df = pd.DataFrame(tfidf_vectors.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    songs.reset_index(drop=True, inplace=True)
    songs = pd.concat([songs, tfidf_df], axis=1)
    songs.drop(columns=['tags'], inplace=True)

    return songs

# Recommendation system
def recommend(song_name, songs):
    if song_name not in songs['Track Name'].values:
        print(f"'{song_name}' is not in the dataset. Please check the song name.")
        return

    # Get the index of the song
    song_index = songs[songs['Track Name'] == song_name].index[0]

    # Compute cosine similarity for numerical features
    numerical_features = songs.select_dtypes(include=[np.number])
    similarity_scores = cosine_similarity(numerical_features)

    # Retrieve top 5 similar songs (excluding itself)
    similar_songs_indices = similarity_scores[song_index].argsort()[::-1][1:6]

    # Display recommendations
    print(f"Top 5 songs similar to '{song_name}':")
    recommendations = songs.iloc[similar_songs_indices]['Track Name'].tolist()
    for idx, song in enumerate(recommendations, 1):
        print(f"{idx}. {song}")

# Main execution
if __name__ == "__main__":
    FILE_PATH = "top_10000_1950-now.csv"
    songs_data = load_and_preprocess(FILE_PATH)
    recommend('Mercy', songs_data)




