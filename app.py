from flask import Flask
from flask import render_template, Blueprint
from flask_login import login_required, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy


# The . is a shortcut that tells it search in current package before rest of the PYTHONPATH
# from .auth import login_required

__author__ = 'Zhongxuan Wang'
__doc__ = 'iGlossary'

app_blueprint = Blueprint('app', __name__)
app = Flask(__name__)


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


@app.route('/', methods=['GET'])
def index():
    print("aaa")
    return render_template('index.html')


# @login_required
def read_file(filename):
    try:
        with open(filename) as f:
            return f.readline()
    except IOError:
        print("IO ERROR Raised. Reading file failed,")
        f = open(filename, "w")
        f.write('email@example.com')
        f.close()
        return 'content'


# @login_required
def write_file(filename, file_content):
    try:
        with open(filename, 'w') as f:
            f.write(file_content)
    except IOError:
        print("IO ERROR Raised. Writing file failed,")
    return ''


@app_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


def create_app():

    app.config['SECRET_KEY'] = 'wwzzxxsecretekeytodatabase'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users/users.db'

    db.init_app(app)

    # # blueprint for auth routes in our app
    # from auth import auth as auth_blueprint
    # appl.register_blueprint(auth_blueprint)
    #
    # appl.register_blueprint(app_blueprint)
    # return appl

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.run(debug=True)


if __name__ == '__main__':
    create_app()
