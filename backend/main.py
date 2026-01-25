#from . import create_app
from app import create_app

# Création de l'application
app = create_app()

# Lancement de l'application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
