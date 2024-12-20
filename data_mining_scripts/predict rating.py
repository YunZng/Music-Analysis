# Import necessary libraries
import numpy as np
import pandas as pd
import warnings
from catboost import Pool, CatBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from feature_engine.encoding import RareLabelEncoder

warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 1000)

# Load and preprocess data
def preprocess_data(file_path, main_label):
    df = pd.read_csv(file_path).drop_duplicates()

    # Filter and process relevant columns
    df = df[df[main_label] > 0]
    df['duration_minutes'] = df['Track Duration (ms)'].apply(lambda x: str(round(x / 6e4)))
    df['release_year'] = df['Album Release Date'].fillna('None').apply(lambda x: x[:4])

    for col in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']:
        df[col] = df[col].apply(lambda x: round(x, 1))
    df['Loudness'] = df['Loudness'].fillna(0).apply(lambda x: 5 * round(1 / 5 * x))
    df['Tempo'] = df['Tempo'].fillna(df['Tempo'].mean()).apply(lambda x: 20 * round(1 / 20 * x))

    # Rare label encoding
    for col in ['Artist Name(s)', 'release_year', 'duration_minutes', 'Label']:
        df[col] = df[col].fillna('None')
        encoder = RareLabelEncoder(n_categories=1, max_n_categories=70, replace_with='Other', tol=12 / df.shape[0])
        df[col] = encoder.fit_transform(df[[col]])

    # Drop unused columns
    cols_to_drop = ['Track URI', 'Track Name', 'Artist URI(s)', 'Album URI', 'Album Name', 'ISRC',
                    'Track Number', 'Disc Number', 'Album Artist URI(s)', 'Album Artist Name(s)', 'Album Image URL',
                    'Copyrights', 'Album Genres', 'Artist Genres', 'Track Preview URL', 'Track Duration (ms)',
                    'Album Release Date', 'Label', 'Added By', 'Added At']
    df = df.drop(cols_to_drop, axis=1, errors='ignore')

    return df

# Train the model
def train_model(df, main_label):
    y = df[main_label].values
    X = df.drop([main_label], axis=1)

    cat_cols = df.select_dtypes(include=['object']).columns
    cat_cols_idx = [list(X.columns).index(c) for c in cat_cols]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    train_pool = Pool(X_train, y_train, cat_features=cat_cols_idx)
    test_pool = Pool(X_test, y_test, cat_features=cat_cols_idx)

    # Optimized CatBoost parameters
    model = CatBoostRegressor(
        iterations=500,
        depth=8,
        learning_rate=0.05,
        l2_leaf_reg=3,
        random_strength=1,
        bagging_temperature=1,
        loss_function='RMSE',
        verbose=0
    )
    model.fit(train_pool)

    y_train_pred = model.predict(train_pool)
    y_test_pred = model.predict(test_pool)

    rmse_train = mean_squared_error(y_train, y_train_pred, squared=False)
    rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)
    print(f"RMSE (Train): {rmse_train:.2f}, RMSE (Test): {rmse_test:.2f}")

    return model, X.columns.tolist(), cat_cols

# Predict a new song
def predict_new_song(model, new_song, training_columns, cat_cols):
    for col in training_columns:
        if col not in new_song.columns:
            new_song[col] = 0

    new_song = new_song[training_columns]

    cat_cols_idx = [list(new_song.columns).index(c) for c in cat_cols]

    new_song_pool = Pool(new_song, cat_features=cat_cols_idx)
    prediction = model.predict(new_song_pool)
    return prediction

# Main script
if __name__ == "__main__":
    file_path = 'top_10000_1950-now.csv'  # Replace with your dataset path
    main_label = 'Popularity'

    df = preprocess_data(file_path, main_label)
    model, training_columns, cat_cols = train_model(df, main_label)

    new_song = pd.DataFrame([{
        'Acousticness': 0.5,
        'Danceability': 0.8,
        'Energy': 0.7,
        'Instrumentalness': 0.0,
        'Liveness': 0.2,
        'Speechiness': 0.1,
        'Valence': 0.6,
        'Loudness': -5.0,
        'Tempo': 120.0,
        'Artist Name(s)': 'Other',
        'release_year': '2010',
        'duration_minutes': '4',
    }])

    predicted_rating = predict_new_song(model, new_song, training_columns, cat_cols)
    print(f"Predicted Rating: {predicted_rating[0]:.2f}")





