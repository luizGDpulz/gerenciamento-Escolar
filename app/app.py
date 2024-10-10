from flask import Flask, render_template
from models import db, Usuario
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import time
import os 
import logging

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Adicione estas linhas para configurar a chave secreta
    app.secret_key = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_muito_secreta'

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://app_user:QWxVbk9zVERz@alunostds.dev.br:3308/app_user'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 280,
        'pool_timeout': 20,
        'pool_pre_ping': True
    }
    
    # Inicializar a instância do banco de dados
    db.init_app(app)

    # Registrar os blueprints
    from routes import register_blueprints
    register_blueprints(app)

    # Adicionar rota de teste de conexão ao banco de dados
    @app.route('/test_db')
    def test_db():
        try:
            result = db.session.execute(text("SELECT 1")).fetchone()
            debug_message = f"Conexão com o banco de dados bem-sucedida. Resultado: {result[0]}"
            logger.debug(debug_message)
            return render_template('teste_db.html', debug_message=debug_message)
        except Exception as e:
            error_message = f"Erro ao conectar ao banco de dados: {str(e)}"
            logger.error(error_message)
            return render_template('test_db.html', error_message=error_message)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    