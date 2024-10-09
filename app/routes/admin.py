from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from models import *
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('auth.login', next=request.url))
        usuario = Usuario.query.get(session['user_id'])
        if usuario.Cargo != 'Administrador':
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@admin_required
def admin_panel():
    usuario = Usuario.query.get(session['user_id'])
    return render_template('admin_panel.html', usuario=usuario)
