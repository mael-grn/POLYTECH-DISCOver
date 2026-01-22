# scripts/train_analyze_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy import create_engine
from app.models.song import Song
from app.models.analyze import Analyze
from app.extensions import db
from sqlalchemy.orm import sessionmaker

# --- Configuration DB ---
DATABASE_URL = "mysql+mysqlconnector://pythonuser:MotDePasse123@localhost/songs_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# --- Charger les données de Songs ---
songs = session.query(Song).filter(Song.song_popularity != None).all()

if not songs:
    print("Aucune chanson avec popularité disponible")
    exit(0)

# Convertir en DataFrame
data = pd.DataFrame([{
    "song_id": s.song_id,
    "acousticness": s.acousticness or 0.0,
    "danceability": s.danceability or 0.0,
    "energy": s.energy or 0.0,
    "instrumentalness": s.instrumentalness or 0.0,
    "liveness": s.liveness or 0.0,
    "loudness": s.loudness or 0.0,
    "valence": getattr(s, "valence", 0.5),
    "tempo": getattr(s, "tempo", 120.0),
    "song_popularity": s.song_popularity
} for s in songs])

# Features et target
X = data[["acousticness", "danceability", "energy", "instrumentalness",
          "liveness", "loudness", "valence", "tempo"]]
y = (data["song_popularity"] >= 50).astype(int)  # populaire si >= 50

# Split train/test
if len(X) == 1:
    X_train, X_test, y_train, y_test = X, X, y, y
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

# --- Entraînement modèle ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Modèle entraîné ! Score sur test:", model.score(X_test, y_test))

# --- Prédire probabilité de popularité ---
probas = model.predict_proba(X)
if probas.shape[1] == 1:
    # Tout est de la même classe, mettre 0 ou 1 selon la classe
    if model.classes_[0] == 1:
        data["popularity_prob"] = 1.0
    else:
        data["popularity_prob"] = 0.0
else:
    data["popularity_prob"] = probas[:, 1]

# --- Mettre à jour la table Analyze ---
for idx, row in data.iterrows():
    analyze = session.query(Analyze).filter(Analyze.id_song == row["song_id"]).first()
    if analyze is None:
        analyze = Analyze(id_song=row["song_id"])
        session.add(analyze)
    analyze.popularity_probability = float(row["popularity_prob"])

try:
    session.commit()
    print("Table Analyze mise à jour avec les probabilités !")
except Exception as e:
    session.rollback()
    print("Erreur lors de la mise à jour de Analyze:", e)
finally:
    session.close()
