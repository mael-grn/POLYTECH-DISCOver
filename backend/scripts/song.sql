CREATE TABLE Songs (
    id int NOT NULL AUTO_INCREMENT,
    song_name varchar(255),
    song_popularity int,
    song_duration_ms int,
    acousticness float,
    danceability float,
    energy float,
    instrumentalness float,
    key int,
    liveness float,
    loudness float,
    audio_mode int,
    speechiness float,
    tempo float,
    time_signature int,
    audio_valence float
);

LOAD DATA INFILE '/mnt/c/Users/nahel/Downloads/song_data.csv'
INTO TABLE Songs
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;