import os
from flask import Flask, sessions
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import redis
from flask_session import Session

#load env
load_dotenv(".env")

app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


app.config.from_mapping(
        MYSQL_HOST=os.getenv("MYSQL_HOST"),
        MYSQL_DB=os.getenv("MYSQL_DB"),  
        MYSQL_USER=os.getenv("MYSQL_USER"),
        MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD"),
        MYSQL_CURSORCLASS = "DictCursor",

        SECRET_KEY = os.getenv("SECRET_KEY"),
        SESSION_COOKIE_SAMESITE="None",
        SESSION_COOKIE_SECURE = True,
        SESSION_TYPE = "redis",
        SESSION_PERMANENT = False,
        SESSION_USE_SIGNER = True,
        SESSION_REDIS = redis.from_url(os.getenv("REDIS_URL"))
    )

app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

#Connect to Database
mysql = MySQL(app)

#Session 
server_session = Session(app)

#CORS
CORS(app, supports_credentials=True ,resources={r"/api/*": {"origins": os.getenv("FRONTEND_URL")}})

