from flask import Flask
from models import db
from routes import main_routes, auth_routes

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://app_user:QWxVbk9zVERz@alunostds.dev.br:3308/app_user'
    
    # Inicializar a instância do banco de dados
    db.init_app(app)

    # Registrar os Blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
