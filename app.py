from flask import Flask
from models import db
from flask_login import LoginManager
from models.user import User  # Import after db init

login_manager = LoginManager()




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'books'  # For session/cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/book_recommendation_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but recommended

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Route name from Blueprint
    login_manager.login_message_category = 'info'

    # Register Blueprints
    from routes.auth_routes import auth
    from routes.user_routes import user
    from routes.book_routes import book
    from routes.main_routes import main
    from routes.admin_routes import admin
    

    

    app.register_blueprint(admin, url_prefix='/admin')
    # app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(book)

    return app
