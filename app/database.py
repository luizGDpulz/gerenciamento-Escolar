from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DatabaseConnection:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        db.init_app(app)  # Associa o SQLAlchemy ao app Flask

    def get_db(self):
        return db

    def initialize_db(self, app):
        with app.app_context():
            db.create_all()  # Cria as tabelas do banco de dados, se não existirem