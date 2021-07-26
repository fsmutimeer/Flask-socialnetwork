# Project/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager




basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

####################
#####Database Config
app.config['SECRET_KEY']='mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/code",

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

Migrate(app, db)
####################

###############
##Login Config#
login_manager=LoginManager()
login_manager.init_app(app)

login_manager.login_view='users.login'

###############

######################
##BluePrints##########

from project.core.views import core
from project.users.views import users
from project.blog_posts.views import blog_posts_blueprint
from project.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(blog_posts_blueprint)
