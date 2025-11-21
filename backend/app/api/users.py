# backend/app/api/users.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from ..core.db import db
from ..models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Champs manquants"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email déjà utilisé"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 400

    hashed = generate_password_hash(password)

    user = User(
        email=email,
        username=username,
        password_hash=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Compte créé avec succès", "user_id": user.id}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Champs manquants"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Identifiants invalides"}), 401

    # Pas encore d'auth JWT → on renvoie l'user_id (à améliorer plus tard)
    return jsonify({
        "message": "Connexion réussie",
        "user_id": user.id,
        "username": user.username
    })
