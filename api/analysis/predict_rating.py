import pandas as pd
import warnings
from catboost import Pool, CatBoostRegressor
from sklearn.model_selection import train_test_split
from feature_engine.encoding import RareLabelEncoder

warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 1000)

# Load and preprocess data
def preprocess_data(data, columns, main_label):
    df = pd.DataFrame(data, columns=columns).drop_duplicates()

    # Filter and process relevant columns
    df = df[df[main_label] > 0]
    df['Duration Minutes'] = df['Track Duration ms'].apply(lambda x: str(round(x / 6e4)))

    for col in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']:
        df[col] = df[col].apply(lambda x: round(x, 1))
    df['Loudness'] = df['Loudness'].fillna(0).apply(lambda x: 5 * round(1 / (5 * float(x) + 1e-5)))
    df['Tempo'] = df['Tempo'].fillna(df['Tempo'].mean()).apply(lambda x: 20 * round(1 / (20 * float(x) + 1e-5)))

    for col in ['Artist Names', 'Duration Minutes', 'Label']:
        df[col] = df[col].fillna('None')
        encoder = RareLabelEncoder(n_categories=1, max_n_categories=70, replace_with='Other', tol=12 / df.shape[0])
        df[col] = encoder.fit_transform(df[[col]])

    # Drop unused columns
    cols_to_drop = ['Track URI', 'Track Name', 'Artist URIs', 'Album URI', 'Album Name', 'ISRC',
                    'Track Number', 'Disc Number', 'Album Artist URIs', 'Album Artist Names', 'Album Image URL',
                    'Copyrights', 'Album Genres', 'Artist Genres', 'Track Preview URL', 'Track Duration ms',
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

    X_train[cat_cols] = X_train[cat_cols].astype(str)
    X_test[cat_cols] = X_test[cat_cols].astype(str)
    train_pool = Pool(X_train, y_train, cat_features=cat_cols_idx)

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
    return model, X.columns.tolist(), cat_cols

# Predict a new song
def predict_new_song(model, new_song, training_columns, cat_cols):
    for col in training_columns:
        if col not in new_song.columns:
            new_song[col] = 0

    new_song = new_song[training_columns]

    cat_cols_idx = [list(new_song.columns).index(c) for c in cat_cols]

    new_song[cat_cols] = new_song[cat_cols].astype(str)
    new_song_pool = Pool(new_song, cat_features=cat_cols_idx)
    prediction = model.predict(new_song_pool)
    return prediction

# Main script
def predict_rating(row, columns, data):
    main_label = 'Popularity'

    df = preprocess_data(row, columns, main_label)
    model, training_columns, cat_cols = train_model(df, main_label)

    new_song = pd.DataFrame([data])

    predicted_rating = predict_new_song(model, new_song, training_columns, cat_cols)
    return f"{predicted_rating[0]:.2f}"

