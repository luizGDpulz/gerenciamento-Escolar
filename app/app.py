from flask import Flask

app = Flask(__name__)

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