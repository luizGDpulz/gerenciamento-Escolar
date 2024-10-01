from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

##app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://app_user:QWxVbk9zVERz@alunostds.dev.br:3308/app_user'

##db = SQLAlchemy(app)

salas = []

@app.route('/register', methods=['POST'])
def register_classroom():
   return render_template('codigo.html')