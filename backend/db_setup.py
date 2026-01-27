
import csv
import os
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.song import Song
from app.models.analyze import Analyze
from app.models.uploaded_by import UploadedBy
from app.models.history import History


app = create_app()

# Chemin du CSV
CSV_PATH = './dataset.csv'

with app.app_context():
    # Initialisation de la base de données
    db.create_all()
    print("Base de données initialisée.")

    # Si la table n'est pas vide, l'import est annulé
    if Song.query.first() is not None:
        print("La table 'song' contient déjà des données. Importation annulée.")
    else:
        print(f"Début de l'importation depuis {CSV_PATH}...")
        try:
            # Ouverture et lecture du fichier CSV
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Création d'un tableau contenant les chansons à ajouter
                songs_to_add = []
                
                # Ajout de chaque chanson du fichier CSV dans le tableau
                for row in reader:
                    new_song = Song(
                        song_name=row['song_name'],
                        song_popularity=int(row['song_popularity']),
                        song_duration_ms=int(row['song_duration_ms']),
                        acousticness=float(row['acousticness']),
                        danceability=float(row['danceability']),
                        energy=float(row['energy']),
                        instrumentalness=float(row['instrumentalness']),
                        key=int(row['key']),
                        liveness=float(row['liveness']),
                        loudness=float(row['loudness']),
                        audio_mode=int(row['audio_mode']) if row.get('audio_mode') not in (None, "", "NA") else None,
                        speechiness=float(row['speechiness']) if row.get('speechiness') not in (
                        None, "", "NA") else None,
                        tempo=float(row['tempo']) if row.get('tempo') not in (None, "", "NA") else None,
                        time_signature=int(row['time_signature']) if row.get('time_signature') not in (
                        None, "", "NA") else None,
                        audio_valence=float(row['audio_valence']) if row.get('audio_valence') not in (
                        None, "", "NA") else None,
                        is_in_data_set=True
                    )
                    songs_to_add.append(new_song)
                
                # Ajout du contenu du tableau dans la base de données
                db.session.bulk_save_objects(songs_to_add)
                db.session.commit()
                print(f"Succès ! {len(songs_to_add)} chansons importées.")

        # Gestion des erreurs
        except FileNotFoundError:
            print(f"Erreur : Le fichier CSV est introuvable à l'adresse {CSV_PATH}")
        except Exception as e:
            db.session.rollback()
            print(f"Une erreur est survenue lors de l'insertion : {e}")