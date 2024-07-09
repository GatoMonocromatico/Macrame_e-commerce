from flask import Flask
import pyrebase
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('CHAVE_SECRETA_FLASK')

csrf = CSRFProtect(app)

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "serviceAccount": "serviceAccount.json"
}
# config para o firebase
firebase = pyrebase.initialize_app(firebase_config)
bd = firebase.database()
storage = firebase.storage()

auth_firebase = firebase.auth()

login_manager = LoginManager()

senha_gmail = os.getenv("CHAVE_DE_APP_GMAIL")