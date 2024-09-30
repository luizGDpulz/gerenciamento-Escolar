"""
Luiz:

Login
Register student
Schedule

Kelvin:

Dashboard
Register class
Schedule classrooms

Matiele:

MainFrame
Register classrooms

Rafael:

Register build
Schedule classrooms
"""

from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app import *
from app.models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://app_user:QWxVbk9zVERz@alunostds.dev.br:3308/app_user'

db = SQLAlchemy(app)

@app.route('/')
def main_menu():
    return "Sistema de gerenciamento de salas iniciado"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register_class', methods=['GET', 'POST'])
def register_class():
    if request.method == 'POST':
        # Lógica para registrar uma nova turma
        nova_sala = Sala(nome=request.form['name'])
        db.session.add(nova_sala)
        db.session.commit()
        flash('Turma registrada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register_class.html')

@app.route('/schedule_classrooms', methods=['GET', 'POST'])
def schedule_classrooms():
    if request.method == 'POST':
        # Lógica para agendar salas de aula
        sala = Sala.query.get(request.form['classroom_id'])
        # Adicione aqui a lógica de agendamento
        flash('Sala de aula agendada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    salas = Sala.query.all()
    return render_template('schedule_classrooms.html', classrooms=salas)