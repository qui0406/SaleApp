from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager


app= Flask(__name__)
app.secret_key= '#$%^&GYVGS^D%^&^&YSDGVYF%S&^^&SGD'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost/saleappdatabase?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['PAGE_SIZE']=4

cloudinary.config(
    cloud_name= 'do43r8nr0',
    api_key='947875495844325',
    api_secret= 'evQEPk5TbxIMpCWbbXl8sLMbo6A'
)

db= SQLAlchemy(app=app)
login= LoginManager(app=app)

