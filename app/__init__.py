from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import stripe



app = Flask(__name__)

app.config['SECRET_KEY'] = '69c82efcb274db8b33f21d04a3d21d99'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#### Stripe Setting ####
os.environ["STRIPE_PUBLISHABLE_KEY"] = "pk_test_dTOyodiHgWWkT6wFPGSoLpiy00EdeKqAJP"
os.environ["STRIPE_SECRET_KEY"] = "sk_test_Hj5EeRmrgeoVLEcCFrzic1sw00EEpN3Szk"

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']
#########################
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from . import routes