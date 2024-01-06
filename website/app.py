from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
IPAC_USERS="database.db"
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='123456789'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{IPAC_USERS}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
    
def create_database(app, db):
    if not path.exists(IPAC_USERS):
        with app.app_context():
            db.create_all()
        print('Created Database!')

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from views import views
from auth import auth
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
with app.app_context():
    create_database(app, db)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=False)