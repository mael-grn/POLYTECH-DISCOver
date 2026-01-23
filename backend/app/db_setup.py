from app import create_app
from app.extensions import db


from app.models.user import User
from app.models.song import Song
from app.models.analyze import Analyze
from app.models.uploaded_by import UploadedBy
from app.models.history import History

app = create_app()

with app.app_context():
    db.create_all()
    print("BD bien creer")
