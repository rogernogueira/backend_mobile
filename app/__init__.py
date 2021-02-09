from flask import Flask

from app.ext import admin,database, routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:master10@localhost/db_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'L3CqXEN7Ym57KYI'
    database.init_app(app)
    admin.init_app(app)
    routes.init_app(app)
       
    return app
