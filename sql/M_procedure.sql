# stored-procedure
# Insert a New Track
DELIMITER $$

CREATE PROCEDURE InsertTrack(
    IN p_track_uri VARCHAR(75),
    IN p_track_name VARCHAR(150),
    IN p_artist_uris VARCHAR(271),
    IN p_artist_names VARCHAR(113),
    IN p_album_uri VARCHAR(36),
    IN p_album_name VARCHAR(153),
    IN p_album_artist_uris VARCHAR(271),
    IN p_album_artist_names VARCHAR(80),
    IN p_album_release_date VARCHAR(10),
    IN p_album_image_url VARCHAR(2083),
    IN p_disc_number INTEGER,
    IN p_track_number INTEGER,
    IN p_track_duration_ms INTEGER,
    IN p_track_preview_url VARCHAR(2083),
    IN p_explicit BOOLEAN,
    IN p_popularity INTEGER,
    IN p_isrc VARCHAR(15),
    IN p_added_by VARCHAR(50),
    IN p_added_at DATETIME,
    IN p_artist_genres VARCHAR(300),
    IN p_danceability FLOAT,
    IN p_energy FLOAT,
    IN p_key INTEGER,
    IN p_loudness FLOAT,
    IN p_mode BOOLEAN,
    IN p_speechiness FLOAT,
    IN p_acousticness FLOAT,
    IN p_instrumentalness FLOAT,
    IN p_liveness FLOAT,
    IN p_valence FLOAT,
    IN p_tempo FLOAT,
    IN p_time_signature INTEGER,
    IN p_album_genres VARCHAR(50),
    IN p_label VARCHAR(69),
    IN p_copyrights VARCHAR(974)
)
BEGIN
    -- Check for existing Track URI to avoid duplicates
    IF EXISTS (
        SELECT 1 FROM mytable WHERE `Track URI` = p_track_uri
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Duplicate Track URI. Entry already exists.';
    ELSE
        -- Insert the new record if no duplicate is found
        INSERT INTO mytable (
            `Track URI`, `Track Name`, `Artist URIs`, `Artist Names`, `Album URI`,
            `Album Name`, `Album Artist URIs`, `Album Artist Names`, `Album Release Date`,
            `Album Image URL`, `Disc Number`, `Track Number`, `Track Duration ms`,
            `Track Preview URL`, Explicit, Popularity, ISRC, `Added By`, `Added At`,
            `Artist Genres`, Danceability, Energy, `Key`, Loudness, Mode,
            Speechiness, Acousticness, Instrumentalness, Liveness, Valence,
            Tempo, `Time Signature`, `Album Genres`, Label, Copyrights
        ) VALUES (
            p_track_uri, p_track_name, p_artist_uris, p_artist_names, p_album_uri,
            p_album_name, p_album_artist_uris, p_album_artist_names, p_album_release_date,
            p_album_image_url, p_disc_number, p_track_number, p_track_duration_ms,
            p_track_preview_url, p_explicit, p_popularity, p_isrc, p_added_by, p_added_at,
            p_artist_genres, p_danceability, p_energy, p_key, p_loudness, p_mode,
            p_speechiness, p_acousticness, p_instrumentalness, p_liveness, p_valence,
            p_tempo, p_time_signature, p_album_genres, p_label, p_copyrights
        );
    END IF;
END $$

DELIMITER ;

# What This Procedure Does:
# Input Parameters: Accepts all the required columns as input parameters.
# Duplicate Check: Before inserting a new track, it checks whether the Track URI already exists.
# If a duplicate is found, it raises an error using SIGNAL SQLSTATE.
# Insertion: If no duplicate exists, the procedure inserts the new record into the mytable.

# How to use with example
# To call the procedure and insert a new track:
/* CALL InsertTrack(
    'spotify:track:0zKbDrEXKpnExhGQRe9dxt', 
    'Lay Low', 
    'spotify:artist:2o5jDhtHVPhrJdv3cEQ99Z', 
    'Tiësto', 
    'spotify:album:0EYKSXXTsON8ZA95BuCoXn', 
    'Lay Low', 
    'spotify:artist:2o5jDhtHVPhrJdv3cEQ99Z', 
    'Tiësto', 
    '2023-01-06', 
    'https://i.scdn.co/image/ab67616d0000b273c8fdaf1b33263d88246ba90a',
    1, 
    1, 
    153442, 
    'https://p.scdn.co/mp3-preview/d4e0715dc213858f53a104ee498944a0d759b6cb', 
    FALSE, 
    87, 
    'NLZ542202348', 
    'spotify:user:bradnumber1', 
    '2023-07-18 22:06:36', 
    'big room,brostep,dutch edm', 
    0.534, 
    0.855, 
    1, 
    -4.923, 
    0, 
    0.183, 
    0.0607, 
    0.000263, 
    0.346, 
    0.42, 
    122.06, 
    4, 
    'EDM, House', 
    'Musical Freedom', 
    'C © 2023 Musical Freedom Label Ltd., P ℗ 2023 Musical Freedom Label Ltd.'
);
*/

# Reminder:
# Error Handling: If the Track URI already exists, the procedure will throw an error.
# Input Validation: Add further checks (e.g., data ranges, NULL values) as needed.
# Transaction Safety: You can wrap this procedure with a transaction if needed for bulk inserts.
