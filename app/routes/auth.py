from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import *
from werkzeug.security import check_password_hash, generate_password_hash
import logging

auth = Blueprint('auth', __name__)

logger = logging.getLogger(__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        next_url = request.form.get('next') or url_for('main.dashboard')
        logger.debug(f"Tentativa de login para o email: {email}")
        usuario = Usuario.query.filter_by(Email=email).first()
        if usuario and usuario.Senha == senha:
            session['user_id'] = usuario.ID_usuario
            logger.info(f"Login bem-sucedido para o usuário: {usuario.Nome}")
            return jsonify({'success': True, 'redirect': next_url})
        else:
            logger.warning(f"Falha no login para o email: {email}")
            return jsonify({'success': False, 'message': 'Credenciais inválidas. Por favor, tente novamente.'})
    next_url = request.args.get('next', url_for('main.dashboard'))
    return render_template('login.html', next=next_url)

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.dashboard'))

@auth.route('/register-student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if Usuario.query.filter_by(Email=email).first():
            flash('Email já cadastrado.', 'error')
            return redirect(url_for('auth.register_student'))
        
        novo_aluno = Usuario(Nome=nome, Cargo='Aluno', Email=email, Senha=generate_password_hash(senha))
        db.session.add(novo_aluno)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register_student.html')

@auth.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        sala_id = request.form['sala_id']
        data = request.form['data']
        horario_inicio = request.form['horario_inicio']
        horario_fim = request.form['horario_fim']
        timestamp_inicio = datetime.strptime(f"{data} {horario_inicio}", "%Y-%m-%d %H:%M")
        timestamp_fim = datetime.strptime(f"{data} {horario_fim}", "%Y-%m-%d %H:%M")
        
        novo_agendamento = Agendamento(
            TimeStamp_inicio=timestamp_inicio,
            TimeStamp_fim=timestamp_fim,
            ID_locatario=session['user_id'],
            Tipo_locatario='Aluno',
            ID_turma=None
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Aula agendada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    salas = Sala.query.all()
    return render_template('schedule.html', salas=salas)
