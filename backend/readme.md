# Faire marcher l'application

## Prérequis

Assurez vous d'avoir créé un fichier `.env` à la racine du projet, avec le contenu suivant :

```
MYSQL_ROOT_PASSWORD=123456789
MYSQL_DATABASE=discover_db
MYSQL_USER=discover_db_user
MYSQL_PASSWORD=123456789
MYSQL_PORT=3307
```
Vous pouvez modifier les valeurs de ces variables à votre convenance, mais celles-ci ne doivent pas être modifiées après avoir initialisé la base de données.

## Installation

1. initialiser la base de données : `docker compose up -d`.
2. installer les dependances python : `pip install -r requirements.txt`.
3. Initialiser la base de données : `python db_setup.py`.
4. Remplissez votre table analyse en lancant le ml sur le dataset avec la commande suivante : `python ml_backfill_analyze.py`.
5. Executer l'app : `python main.py`.