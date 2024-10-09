from flask import Blueprint, render_template, redirect, url_for, flash, session, request, send_from_directory
from models import *
from datetime import datetime, timedelta
from functools import wraps

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/schedule/classrooms', methods=['GET', 'POST'])
@login_required
def schedule_classroom():
    if request.method == 'POST':
        sala_id = request.form['sala_id']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        horario_inicio = request.form['horario_inicio']
        horario_fim = request.form['horario_fim']
        
        sala = Sala.query.get(sala_id)
        if not sala:
            flash('Sala não encontrada.', 'error')
            return redirect(url_for('main.schedule_classroom'))
        
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
        
        while data_inicio <= data_fim:
            timestamp_inicio = datetime.combine(data_inicio, datetime.strptime(horario_inicio, "%H:%M").time())
            timestamp_fim = datetime.combine(data_inicio, datetime.strptime(horario_fim, "%H:%M").time())
            
            agendamento = Agendamento(
                TimeStamp_inicio=timestamp_inicio,
                TimeStamp_fim=timestamp_fim,
                ID_locatario=session['user_id'],
                Tipo_locatario='Professor',
                ID_turma=None
            )
            db.session.add(agendamento)
            data_inicio += timedelta(days=1)
        
        db.session.commit()
        flash('Sala agendada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    salas = Sala.query.all()
    return render_template('schedule_classroom.html', salas=salas)

@main.route('/register-build', methods=['GET', 'POST'])
@login_required
def register_build():
    if request.method == 'POST':
        nome = request.form['nome']
        andares = request.form['andares']
        cor = request.form['cor']
        
        novo_predio = Predio(Nome=nome, Andares=andares, Cor=cor)
        db.session.add(novo_predio)
        db.session.commit()
        
        for i in range(1, int(andares) + 1):
            novo_andar = Andar(Numero=i, ID_predio=novo_predio.ID_predio)
            db.session.add(novo_andar)
        
        db.session.commit()
        flash('Prédio registrado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('register_build.html')

@main.route('/register', methods=['GET', 'POST'])
@login_required
def register_classroom():
    if request.method == 'POST':
        tipo = request.form['tipo']
        id_andar = request.form['id_andar']
        capacidade = request.form['capacidade']
        
        nova_sala = Sala(Tipo=tipo, ID_andar=id_andar, Capacidade=capacidade)
        db.session.add(nova_sala)
        db.session.commit()
        
        flash('Sala registrada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    andares = Andar.query.all()
    return render_template('register.html', andares=andares)

@main.route('/register-resource', methods=['GET', 'POST'])
@login_required
def register_resource():
    if request.method == 'POST':
        nome = request.form['nome']
        id_sala = request.form['id_sala']
        identificacao = request.form['identificacao']
        status = request.form['status']
        
        novo_recurso = Recurso(Nome=nome, ID_sala=id_sala, Identificacao=identificacao, Status=status)
        db.session.add(novo_recurso)
        db.session.commit()
        
        flash('Recurso registrado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    salas = Sala.query.all()
    return render_template('register_resource.html', salas=salas)

@main.route('/register-class', methods=['GET', 'POST'])
@login_required
def register_class():
    if request.method == 'POST':
        quantidade = request.form['quantidade']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        id_turno = request.form['id_turno']
        curso = request.form['curso']
        cor = request.form['cor']
        dias = request.form.getlist('dias')
        
        nova_turma = Turma(
            Quantidade=quantidade,
            Data_inicio=datetime.strptime(data_inicio, "%Y-%m-%d"),
            Data_Fim=datetime.strptime(data_fim, "%Y-%m-%d"),
            ID_turno=id_turno,
            Curso=curso,
            Cor=cor
        )
        db.session.add(nova_turma)
        db.session.commit()
        
        for dia_id in dias:
            turma_dia = TurmaDia(ID_turma=nova_turma.ID_turma, ID_dia=dia_id)
            db.session.add(turma_dia)
        
        db.session.commit()
        flash('Turma registrada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    turnos = Turno.query.all()
    dias = Dia.query.all()
    return render_template('register_class.html', turnos=turnos, dias=dias)

@main.route('/register-professor', methods=['GET', 'POST'])
@login_required
def register_professor():
    if request.method == 'POST':
        nome = request.form['nome']
        area = request.form['area']
        carga_horaria = request.form['carga_horaria']
        tipo_contrato = request.form['tipo_contrato']
        disponibilidades = request.form.getlist('disponibilidades')
        
        novo_professor = Professor(Nome=nome, Area=area, CargaHoraria=carga_horaria, TipoContrato=tipo_contrato)
        db.session.add(novo_professor)
        db.session.commit()
        
        for disp_id in disponibilidades:
            disponibilidade_professor = DisponibilidadeProfessor(ID_professor=novo_professor.ID_professor, ID_disponibilidade=disp_id)
            db.session.add(disponibilidade_professor)
        
        db.session.commit()
        flash('Professor registrado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    disponibilidades = Disponibilidade.query.all()
    return render_template('register_professor.html', disponibilidades=disponibilidades)

@main.route('/static/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('templates/static/img', filename)
