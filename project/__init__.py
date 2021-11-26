from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

CONFIG_FILE = "config.py"

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app(config_file=CONFIG_FILE):

    # Setup app
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    # Setup db
    db.init_app(app)

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Import db models
    from .models import User
    from .models import TDList
    from .models import Task

    ### 2 Lines below only required once, when creating DB. ####
    # with app.app_context():
    #     db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .views import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .views import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


app = create_app()
