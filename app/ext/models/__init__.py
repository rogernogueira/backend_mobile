from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)


    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self) :
        return f"< User : {self.email}>"

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', )
        
user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    descricao = db.Column(db.String(128), nullable=False)
    doneAt = db.Column(db.String(84), nullable=True)
    estimateAt = db.Column(db.String(84), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=user_id)


    def __init__(self, descricao, doneAt, estimateAt, user_id):
        self.descricao = descricao
        self.doneAt = doneAt
        self.estimateAt = estimateAt
        self.user_id = user_id

   
    def __repr__(self) :
        return f"< demanda : {self.descricao}>"

class TasksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'descricao','estimateAt', 'doneAt', 'user_id')
        
task_share_schema = TasksSchema()
tasks_share_schema = TasksSchema(many=True)


