from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db  = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    db = SQLAlchemy(app)
    ma = Marshmallow(app)