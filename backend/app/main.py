from app import create_app
from app.extensions import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():  # context app pour SQLAlchemy
        db.create_all()       # crée toutes les tables
        print("Tables créées ou existantes ✅")
    
    app.run(debug=True)
