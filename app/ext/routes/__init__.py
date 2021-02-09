from flask import jsonify, request
from flask_migrate import Migrate
from datetime import date
from app.ext.database import db, ma
from app.ext.models import TasksSchema, User, user_share_schema, users_share_schema, Tasks, tasks_share_schema, task_share_schema
from werkzeug.security import generate_password_hash
from app.ext.auth import jwt_required
import datetime
import jwt
import time

def init_app(app):
    TEMPO_EXPIRACAO = 100
    data_atual = date.today()

    Migrate(app, db)


    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            User=User,
        )
    @app.route('/auth/register', methods=["POST"])
    def register():
        name = request.json['name']   
        email = request.json['email'].lower()   
        password = request.json['password']
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        result = User.query.filter_by(email=email).first()
        return jsonify(user_share_schema.dump(result))


    @app.route('/auth/login', methods=["POST"])
    def login():
        email = request.json['email'].lower()   
        password = request.json['password']
     

        user = User.query.filter_by(email=email).first_or_404()
        if not user.verify_password(password) :
            return jsonify({
                "error":"Login ou senha incorreta!"
            }), 403
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=TEMPO_EXPIRACAO)
        payload = {
            "id": user.id, 
            "exp":expire, 
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])
        return jsonify({ "token": token})


    @app.route('/tasks/list', methods=["GET"])
    @jwt_required
    def list_tasks(current_user):
        result = tasks_share_schema.dump(Tasks.query.all())
        return jsonify(result)



    @app.route('/tasks/add', methods=["POST"])
    @jwt_required
    def add_tasks(current_user):
        descricao = request.json['descricao']
        estimateAt = request.json['estimateAt'] 
        task = Tasks(descricao=descricao ,estimateAt = estimateAt, doneAt="", user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        result = Tasks.query.filter_by(descricao=descricao, user_id=current_user.id).first()
        return jsonify(task_share_schema.dump(result))
    

    @app.route('/tasks/delete', methods=["POST"])
    @jwt_required
    def delete_tasks(current_user):
        task_id = request.json['id']   
        task_del = Tasks.query.filter_by(id=task_id).first()
        db.session.delete(task_del)
        db.session.commit()
        return jsonify(task_share_schema.dump(task_del))

    @app.route('/tasks/edit', methods=["POST"])
    @jwt_required
    def edit_tasks(current_user):
        task_id = request.json['id']   
        task_edit = Tasks.query.filter_by(id=task_id).first()
        task_edit.descricao = request.json['descricao']
        task_edit.estimateAt = request.json['estimateAt']
    
        db.session.commit()

        return jsonify(task_share_schema.dump(task_edit))


    @app.route('/auth/check_token', methods=["POST"])
    @jwt_required
    def check_tokem(current_user):
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=TEMPO_EXPIRACAO)
        payload = {
            "id": current_user.id, 
            "exp":expire, 
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'])     
        return jsonify({ "token": token , "id":current_user.id})