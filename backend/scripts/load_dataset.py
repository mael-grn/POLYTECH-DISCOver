import mysql.connector
from mysql.connector import Error
import csv
import os

# Chemin de la base de données CSV
csv_path = '/home/etudiant/POLYTECH-DISCOver/data/raw/song_data.csv'

# Config connexion
config = {
    'host': 'localhost',
    'user': 'pythonuser',
    'password': 'MotDePasse123',
    'database': 'songs_db',
    'use_pure': True
}

try:
    conn = mysql.connector.connect(**config) # connexionn mySQL
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
    # Exécution de la requête
    cursor.execute(create_table)

    # Importation du CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Insertion de toutes les données du CSV dans la table
        for row in reader:
            cursor.execute("""
                INSERT INTO Songs (
                    song_name, song_popularity, song_duration_ms, acousticness, danceability,
                    energy, instrumentalness, `key`, liveness, loudness, audio_mode,
                    speechiness, tempo, time_signature, audio_valence
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['song_name'], row['song_popularity'], row['song_duration_ms'],
                row['acousticness'], row['danceability'], row['energy'], row['instrumentalness'],
                row['key'], row['liveness'], row['loudness'], row['audio_mode'],
                row['speechiness'], row['tempo'], row['time_signature'], row['audio_valence']
            ))

    conn.commit()
    print("Table créée et CSV importé avec succès !")

# Gestion d'erreur
except Error as e:
    print("Erreur MySQL :", e)

finally:
    # Si le curseur est encore présent, le fermer
    if 'cursor' in locals() and cursor:
        cursor.close()
    # Si la connection est encore présente, la fermer
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connexion MySQL fermée.")
