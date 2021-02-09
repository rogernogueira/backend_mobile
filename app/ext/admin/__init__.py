from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.ext.database import db, ma
from app.ext.models import TasksSchema, User, user_share_schema, users_share_schema, Tasks, tasks_share_schema, task_share_schema
from werkzeug.security import generate_password_hash


admin = Admin()

class UserView(ModelView):
    def index(self):
        return self.render('user.html')
    def on_model_change(self, form, User, is_created=False):
         User.password =generate_password_hash(form.password.data)

def init_app(app):
    admin.name = "Back-End"
    admin.template_mode = 'bootstrap3'
    admin.init_app(app)
    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(Tasks, db.session))
