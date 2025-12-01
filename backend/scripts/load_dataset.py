import mysql.connector
from mysql.connector import Error

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Lycee2020.',
    'database': 'Songs',
    'allow_local_infile': True  # essentiel pour LOAD DATA LOCAL INFILE
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Connexion à MySQL réussie !")

    # Création de la table
    create_table = """
    CREATE TABLE IF NOT EXISTS Songs (
        id INT NOT NULL AUTO_INCREMENT,
        song_name VARCHAR(255),
        song_popularity INT,
        song_duration_ms INT,
        acousticness FLOAT,
        danceability FLOAT,
        energy FLOAT,
        instrumentalness FLOAT,
        `key` INT,
        liveness FLOAT,
        loudness FLOAT,
        audio_mode INT,
        speechiness FLOAT,
        tempo FLOAT,
        time_signature INT,
        audio_valence FLOAT,
        PRIMARY KEY (id)
    );
    """
    cursor.execute(create_table)

    # Charger le CSV
    load_csv = """
    LOAD DATA LOCAL INFILE '../../data/raw/song_data.csv'
    INTO TABLE Songs
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;
    """
    cursor.execute(load_csv)

    conn.commit()
    print("Table créée et CSV importé avec succès !")

except Error as e:
    print("Erreur MySQL :", e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connexion MySQL fermée.")