# 1. Retrieve all tracks released after 2020
SELECT `Track Name`, `Album Name`, `Album Release Date`
FROM mytable
WHERE `Album Release Date` >= '2020-01-01';

# 2. Find the most popular tracks (top 10 by Popularity)
SELECT `Track Name`, `Artist Names`, Popularity
FROM mytable
ORDER BY Popularity DESC
LIMIT 10;

# 3. Get all tracks by a specific artist (e.g., 'Tiësto')
SELECT `Track Name`, `Album Name`, `Track Duration ms`
FROM mytable
WHERE `Artist Names` = 'Tiësto';

# 4. Count the number of tracks in each genre
SELECT `Artist Genres`, COUNT(*) AS track_count
FROM mytable
WHERE `Artist Genres` IS NOT NULL
GROUP BY `Artist Genres`
ORDER BY track_count DESC;

# 5. Find the total track duration for each album
SELECT `Album Name`, SUM(`Track Duration ms`) AS total_duration
FROM mytable
GROUP BY `Album Name`
ORDER BY total_duration DESC;

# 6. Find tracks with Danceability greater than 0.8 and Energy greater than 0.7
SELECT `Track Name`, Danceability, Energy
FROM mytable
WHERE Danceability > 0.8 AND Energy > 0.7;

# 7. List the tracks that are marked as explicit
SELECT `Track Name`, `Artist Names`, Explicit
FROM mytable
WHERE Explicit = 'true';

# 8. Retrieve all tracks along with their tempo, sorted by tempo (highest to lowest)
SELECT `Track Name`, Tempo
FROM mytable
ORDER BY Tempo DESC;

# 9. Find the albums with more than 5 tracks
SELECT `Album Name`, COUNT(*) AS track_count
FROM mytable
GROUP BY `Album Name`
HAVING COUNT(*) > 5;

# 10. List all tracks with missing preview URLs
SELECT `Track Name`, `Album Name`
FROM mytable
WHERE `Track Preview URL` IS NULL;

# 11. Find the track with the longest duration
SELECT `Track Name`, `Album Name`, `Track Duration ms`
FROM mytable
ORDER BY `Track Duration ms` DESC
LIMIT 1;

# 12. Retrieve all unique artist names in the database
SELECT DISTINCT `Artist Names`
FROM mytable;

# 13. Find tracks with a loudness value lower than -10
SELECT `Track Name`, Loudness
FROM mytable
WHERE Loudness < -10;

# 14. Find the average Danceability and Energy per genre
SELECT `Artist Genres`, AVG(Danceability) AS avg_danceability, AVG(Energy) AS avg_energy
FROM mytable
WHERE `Artist Genres` IS NOT NULL
GROUP BY `Artist Genres`;

# 15. Find the top 5 most common words in track names
SELECT word, COUNT(*) AS word_count
FROM (
    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(`Track Name`, ' ', numbers.n), ' ', -1) AS word
    FROM mytable
    JOIN (
        SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7
        UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    ) numbers ON CHAR_LENGTH(`Track Name`) - CHAR_LENGTH(REPLACE(`Track Name`, ' ', '')) >= numbers.n - 1
) AS words
WHERE word <> ''
GROUP BY word
ORDER BY word_count DESC
LIMIT 5;

# 16. Find the top 3 longest tracks per album
SELECT `Album Name`, `Track Name`, `Track Duration ms`
FROM (
    SELECT `Album Name`, `Track Name`, `Track Duration ms`,
           RANK() OVER (PARTITION BY `Album Name` ORDER BY `Track Duration ms` DESC) AS rank
    FROM mytable
) AS ranked_tracks
WHERE rank <= 3
LIMIT 3;

# 17. Find artists who have more than 2 albums in the database
SELECT `Artist Names`, COUNT(DISTINCT `Album Name`) AS album_count
FROM mytable
GROUP BY `Artist Names`
HAVING album_count > 2
ORDER BY album_count DESC;

# 18. Calculate the average loudness and tempo for each year
SELECT LEFT(`Album Release Date`, 4) AS release_year,
       AVG(Loudness) AS avg_loudness,
       AVG(Tempo) AS avg_tempo
FROM mytable
WHERE `Album Release Date` IS NOT NULL
GROUP BY release_year
ORDER BY release_year;

# 19. Identify duplicate tracks by name and artist
SELECT `Track Name`, `Artist Names`, COUNT(*) AS duplicate_count
FROM mytable
GROUP BY `Track Name`, `Artist Names`
HAVING duplicate_count > 1;

# 20. List albums with at least one track having Energy greater than 0.9
SELECT DISTINCT `Album Name`, `Artist Names`
FROM mytable
WHERE Energy > 0.9
ORDER BY `Album Name`;

# 21. Find the top 3 albums with the highest average track popularity, 
#     considering only albums with at least 5 tracks released after 2020
SELECT `Album Name`, AVG_Popularity
FROM (
    SELECT `Album Name`, AVG(Popularity) AS AVG_Popularity
    FROM mytable
    WHERE `Album Release Date` >= '2020-01-01'
    GROUP BY `Album Name`
    HAVING COUNT(*) >= 5
) AS album_avg_popularity
ORDER BY AVG_Popularity DESC
LIMIT 3;

# 22. Find the artist who has contributed to the highest number of albums with more than 3 tracks per album
SELECT `Artist Names`, COUNT(DISTINCT `Album Name`) AS album_count
FROM mytable
WHERE `Album Name` IN (
    SELECT `Album Name`
    FROM mytable
    GROUP BY `Album Name`
    HAVING COUNT(*) > 3
)
GROUP BY `Artist Names`
ORDER BY album_count DESC
LIMIT 1;

# 23. Identify the album with the longest total track duration among albums released by artists with average loudness above 10
SELECT `Album Name`, MAX(total_duration) AS max_duration
FROM (
    SELECT `Album Name`, SUM(`Track Duration ms`) AS total_duration
    FROM mytable
    WHERE `Artist Names` IN (
        SELECT `Artist Names`
        FROM mytable
        GROUP BY `Artist Names`
        HAVING ABS(AVG(Loudness)) >= 10
    )
    GROUP BY `Album Name`
) AS album_durations;

# 24. Find the top 3 genres with the highest average danceability, considering only tracks with Energy above the overall average
SELECT `Artist Genres`, AVG(Danceability) AS avg_danceability
FROM mytable
WHERE Energy > (
    SELECT AVG(Energy)
    FROM mytable
)
GROUP BY `Artist Genres`
ORDER BY avg_danceability DESC
LIMIT 3;

# 25. Find the top 3 albums with the highest total track duration, 
#     considering only albums released by artists whose average loudness 
#     is above the overall average loudness of all artists
SELECT `Album Name`, total_duration
FROM (
    SELECT `Album Name`, SUM(`Track Duration ms`) AS total_duration
    FROM mytable
    WHERE `Artist Names` IN (
        SELECT `Artist Names`
        FROM (
            SELECT `Artist Names`, AVG(Loudness) AS avg_loudness
            FROM mytable
            GROUP BY `Artist Names`
            HAVING avg_loudness > (
                SELECT AVG(Loudness)
                FROM mytable
            )
        ) AS loud_artists
    )
    GROUP BY `Album Name`
) AS album_durations
ORDER BY total_duration DESC
LIMIT 3;

# 26. Retrieve songs from M2023 that also appear in the top 50 of M2024, including their rank
SELECT m2023.track_name, m2023.`artist(s)_name`, m2024.`All Time Rank` AS Rank2024
FROM M2023 m2023
JOIN M2024 m2024 
ON m2023.track_name = m2024.`Track` AND m2023.`artist(s)_name` = m2024.`Artist`
WHERE CAST(REPLACE(m2024.`All Time Rank`, ',', '') AS UNSIGNED) <= 50;

# 27. List artists in M2023 who have songs in M2024, along with the total streams in both years and latest track score
SELECT m2023.`artist(s)_name`, m2023.streams AS TotalStreams2023, m2024.`Spotify Streams` AS TotalStreams2024, m2024.`Track Score`
FROM M2023 m2023
JOIN M2024 m2024 ON m2023.`artist(s)_name` = m2024.`Artist`
GROUP BY m2023.`artist(s)_name`
ORDER BY m2024.`Track Score` DESC;

# 28. Find the most popular songs in mytable that also appear in Songs, including their rank from DailyMusicRank
SELECT s.`Title` AS SongsName, s.`Artist`,
       MIN(dr.daily_rank) AS BestRank, m.Popularity
FROM mytable m
JOIN Songs s ON m.`Track Name` = s.`Title`
JOIN DailyMusicRank dr ON s.`Title` = dr.name
GROUP BY s.`Title`
ORDER BY m.Popularity DESC, BestRank ASC
LIMIT 10;

# 29. Compare the total streams of songs in mytable and Songs that are also present in M2023
SELECT DISTINCT s.`Title` AS SongsName, s.`Artist`,
       m2023.Streams AS M2023Streams, m.Popularity
FROM mytable m
JOIN Songs s ON m.`Track Name` = s.`Title` AND m.`Artist Names` = s.`Artist`
JOIN M2023 m2023 ON s.`Title` = m2023.track_name AND s.`Artist` = m2023.`artist(s)_name`
ORDER BY m.Popularity DESC
LIMIT 10;

# 30. Find the top 5 most consistent tracks across mytable, Songs, and M2024 based on average rank and popularity
SELECT s.`Title` AS SongsTrackName, s.`Artist`,
       AVG(CAST(REPLACE(m2024.`All Time Rank`, ',', '') AS UNSIGNED)) AS RankConsistency, m.Popularity
FROM mytable m
JOIN Songs s ON m.`Track Name` = s.`Title` AND m.`Artist Names` = s.`Artist`
JOIN M2024 m2024 ON s.`Title` = m2024.`Track` AND s.`Artist` = m2024.`Artist`
GROUP BY s.`Title`, s.`Artist`
ORDER BY RankConsistency DESC, m.Popularity DESC
LIMIT 5;
