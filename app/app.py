from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://app_user:QWxVbk9zVERz@alunostds.dev.br:3308/app_user'

db = SQLAlchemy(app)

@app.route('/test_db')
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return 'Conexão com o banco de dados estabelecida com sucesso!'
    except Exception as e:
        return str(e)

@app.route('/')
def main_menu():
    return "Sistema de gerenciamento de salas iniciado"

@app.route('/sobre')
def sobre():
    return "Este é o sistema para gerenciar salas e recursos da escola"

@app.route('/contato')
def contato():
    return "Contato: admin@escola.com"

if __name__ == '__main__':
    app.run(debug=True)