import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL

#load env
load_dotenv(".env")

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

#Connect to Database
app.config.from_mapping(
        MYSQL_HOST=os.getenv("MYSQL_HOST"),
        MYSQL_DB=os.getenv("MYSQL_DB"),  
        MYSQL_USER=os.getenv("MYSQL_USER"),
        MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD"),
    )
    
mysql = MySQL(app)

CORS(app)




