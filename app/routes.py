from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, send_file, send_from_directory
from sqlalchemy import text
from models import *
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from datetime import datetime, timedelta
import os
from functools import wraps

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Criar blueprints para diferentes áreas da aplicação
main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)
test_routes = Blueprint('test', __name__)
config_routes = Blueprint('config', __name__)

# Definir o decorador login_required fora da classe RouteManager
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

class RouteManager:
    def __init__(self, main_routes, auth_routes, test_routes, config_routes):
        self.main_routes = main_routes
        self.auth_routes = auth_routes
        self.test_routes = test_routes
        self.config_routes = config_routes
        self.register_routes()

    def register_routes(self):
        # Rotas principais (main_routes)
        @self.main_routes.route('/')
        def index():
            return redirect(url_for('main.dashboard'))

        @self.main_routes.route('/dashboard')
        def dashboard():
            return render_template('dashboard.html')

        @self.main_routes.route('/schedule/classrooms', methods=['GET', 'POST'])
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

        @self.main_routes.route('/register-build', methods=['GET', 'POST'])
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
        
        @self.main_routes.route('/register', methods=['GET', 'POST'])
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

        @self.main_routes.route('/register-resource', methods=['GET', 'POST'])
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

        @self.main_routes.route('/register-class', methods=['GET', 'POST'])
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

        @self.main_routes.route('/register-professor', methods=['GET', 'POST'])
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
        
        @self.main_routes.route('/static/img/<path:filename>')
        def serve_image(filename):
            return send_from_directory('templates/static/img', filename)

        # Rotas de autenticação (auth_routes)
        @self.auth_routes.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                email = request.form['email']
                senha = request.form['password']
                next_url = request.form.get('next') or url_for('main.dashboard')
                logger.debug(f"Tentativa de login para o email: {email}")
                usuario = Usuario.query.filter_by(Email=email).first()
                # if usuario and check_password_hash(usuario.Senha, senha):
                if usuario.Senha == senha:
                    session['user_id'] = usuario.ID_usuario
                    logger.info(f"Login bem-sucedido para o usuário: {usuario.Nome}")
                    flash('Login realizado com sucesso!', 'success')
                    return jsonify({'success': True, 'redirect': next_url})
                else:
                    logger.warning(f"Falha no login para o email: {email}")
                    return jsonify({'success': False, 'message': 'Credenciais inválidas. Por favor, tente novamente.'})
            next_url = request.args.get('next')
            return render_template('login.html', next=next_url)

        @self.auth_routes.route('/logout')
        def logout():
            session.pop('user_id', None)
            flash('Você foi desconectado.', 'info')
            return redirect(url_for('main.dashboard'))

        @self.auth_routes.route('/register-student', methods=['GET', 'POST'])
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

        @self.auth_routes.route('/schedule', methods=['GET', 'POST'])
        @login_required
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
                    ID_turma=None  # Assumindo que alunos não estão associados a turmas específicas
                )
                db.session.add(novo_agendamento)
                db.session.commit()
                
                flash('Aula agendada com sucesso!', 'success')
                return redirect(url_for('main.dashboard'))
            
            salas = Sala.query.all()
            return render_template('schedule.html', salas=salas)

        # Rotas de teste (test_routes)
        @self.test_routes.route('/test_db')
        @login_required
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

        @self.test_routes.route('/execute_query/<query_name>', methods=['GET'])
        @login_required
        def execute_query(query_name):
            try:
                result = []
                if query_name == 'listar_usuarios':
                    result = [{'ID': u.ID_usuario, 'Nome': u.Nome, 'Cargo': u.Cargo, 'Email': u.Email} for u in Usuario.query.all()]
                elif query_name == 'listar_predios':
                    result = [{'ID': p.ID_predio, 'Nome': p.Nome, 'Andares': p.Andares, 'Cor': p.Cor} for p in Predio.query.all()]
                elif query_name == 'listar_andares':
                    result = [{'ID': a.ID_andar, 'Numero': a.Numero, 'ID_predio': a.ID_predio} for a in Andar.query.all()]
                elif query_name == 'listar_salas':
                    result = [{'ID': s.ID_sala, 'Tipo': s.Tipo, 'ID_andar': s.ID_andar, 'Capacidade': s.Capacidade} for s in Sala.query.all()]
                elif query_name == 'listar_recursos':
                    result = [{'ID': r.ID_recurso, 'Nome': r.Nome, 'ID_sala': r.ID_sala, 'Identificacao': r.Identificacao, 'Status': r.Status} for r in Recurso.query.all()]
                elif query_name == 'listar_recursos_alugaveis':
                    result = [{'ID': ra.ID_recurso_alugavel, 'Quantidade': ra.Quantidade, 'Identificacao': ra.Identificacao, 'Status': ra.Status} for ra in RecursoAlugavel.query.all()]
                elif query_name == 'listar_turmas':
                    result = [{'ID': t.ID_turma, 'Quantidade': t.Quantidade, 'Data_inicio': t.Data_inicio.isoformat(), 'Data_Fim': t.Data_Fim.isoformat(), 'ID_turno': t.ID_turno, 'Curso': t.Curso, 'Cor': t.Cor} for t in Turma.query.all()]
                elif query_name == 'listar_dias':
                    result = [{'ID': d.ID_dia, 'Nome': d.Nome} for d in Dia.query.all()]
                elif query_name == 'listar_professores':
                    result = [{'ID': p.ID_professor, 'Nome': p.Nome, 'Area': p.Area, 'CargaHoraria': p.CargaHoraria, 'TipoContrato': p.TipoContrato} for p in Professor.query.all()]
                elif query_name == 'listar_agendamentos':
                    result = [{'ID': a.ID_agendamento, 'TimeStamp_inicio': a.TimeStamp_inicio.isoformat(), 'ID_locatario': a.ID_locatario, 'Tipo_locatario': a.Tipo_locatario, 'ID_turma': a.ID_turma, 'TimeStamp_fim': a.TimeStamp_fim.isoformat()} for a in Agendamento.query.all()]
                elif query_name == 'listar_turnos':
                    result = [{'ID': t.ID_turno, 'Nome_turno': t.Nome_turno, 'HorarioInicio': t.HorarioInicio.isoformat(), 'HorarioFim': t.HorarioFim.isoformat(), 'Cor': t.Cor} for t in Turno.query.all()]
                elif query_name == 'listar_disponibilidades':
                    result = [{'ID': d.ID, 'ID_dia': d.ID_dia, 'ID_turno': d.ID_turno} for d in Disponibilidade.query.all()]
                else:
                    return jsonify({'error': 'Consulta não reconhecida'}), 400
                
                return jsonify(result)
            except Exception as e:
                logger.error(f"Erro ao executar consulta {query_name}: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.test_routes.route('/insert_data', methods=['POST'])
        @login_required
        def insert_data():
            try:
                data = request.get_json()
    
                nome = data.get('nome')
                cargo = data.get('cargo')
                email = data.get('email')
                senha = data.get('senha')

                if not nome or not cargo or not email or not senha:
                    return jsonify({'error': 'Faltam dados obrigatórios'}), 400

                senha_hash = generate_password_hash(senha)
                novo_usuario = Usuario(Nome=nome, Cargo=cargo, Email=email, Senha=senha_hash)
                db.session.add(novo_usuario)
                db.session.commit()
                
                return jsonify({
                    'message': 'Usuário criado com sucesso!',
                    'usuario': {
                        'ID': novo_usuario.ID_usuario,
                        'Nome': novo_usuario.Nome,
                        'Cargo': novo_usuario.Cargo,
                        'Email': novo_usuario.Email
                    }
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
        
        # Rotas de configuração (config_routes)
        @self.config_routes.route('/admin')
        @login_required
        def admin_panel():
            usuario = Usuario.query.get(session['user_id'])
            if usuario.Cargo != 'Administrador':
                flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
                return redirect(url_for('main.dashboard'))
            
            # Aqui você pode adicionar a lógica para o painel de administrador
            return render_template('admin_panel.html', usuario=usuario)

# Instanciando o gerenciador de rotas
route_manager = RouteManager(main_routes, auth_routes, test_routes, config_routes)