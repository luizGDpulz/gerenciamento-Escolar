from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://app_user:QWxVbk9zVERz@alunostds.dev.br:3308/app_user'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)