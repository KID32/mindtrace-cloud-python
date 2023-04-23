from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def connect(app: Flask, database_name: str) -> SQLAlchemy:
    # 连接数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:2004131phy123@localhost/{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return SQLAlchemy(app)
