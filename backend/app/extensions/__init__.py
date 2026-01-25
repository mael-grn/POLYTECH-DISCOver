from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Création base de données SQLAlchemy
db = SQLAlchemy()
# Création marshmallow
ma = Marshmallow()