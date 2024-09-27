from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/nome_do_banco'

db = SQLAlchemy(app)

@app.route('/test_db')
def test_db():
    try:
        db.session.execute('SELECT 1')
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