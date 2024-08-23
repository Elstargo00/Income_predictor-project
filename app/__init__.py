from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import stripe
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./site.db'

#### Stripe Setting ####
stripe_keys = {
  'secret_key': os.environ.get("STRIPE_PUBLISHABLE_KEY"),
  'publishable_key': os.environ.get("STRIPE_SECRET_KEY")
}

stripe.api_key = stripe_keys['secret_key']
#########################
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from . import routes