from .main import main
from .auth import auth
from .admin import admin
from .test import test

def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(test)

