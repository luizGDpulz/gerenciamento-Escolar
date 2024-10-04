from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from sqlalchemy import text
from models import db, Usuario, Predio, Andar, Sala, Recurso, RecursoAlugavel, RecursoAlugavelDisponibilidade, Turma, TurmaDia, Dia, Professor, DisponibilidadeProfessor, Agendamento, Turno, Disponibilidade
from werkzeug.security import check_password_hash
import logging

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Criar blueprints para diferentes áreas da aplicação
main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)

class RouteManager:
    def __init__(self, main_routes, auth_routes):
        self.main_routes = main_routes
        self.auth_routes = auth_routes
        self.register_routes()

    def register_routes(self):
        # Rotas principais (main_routes)
        @self.main_routes.route('/')
        def main_menu():
            return "Sistema de gerenciamento de salas iniciado"

        @self.main_routes.route('/about')
        def sobre():
            return "Este é o sistema para gerenciar salas e recursos da escola"

        @self.main_routes.route('/contato')
        def contato():
            return "Contato: admin@escola.com"

        @self.main_routes.route('/test_db')
        def test_db():
            try:
                # Adicione aqui uma consulta simples ao banco de dados
                result = db.session.execute(text("SELECT 1")).fetchone()
                debug_message = f"Conexão com o banco de dados bem-sucedida. Resultado: {result[0]}"
                logger.debug(debug_message)
                return render_template('teste_db.html', debug_message=debug_message)
            except Exception as e:
                # Registre o erro para depuração
                error_message = f"Erro ao conectar ao banco de dados: {str(e)}"
                logger.error(error_message)
                return render_template('teste_db.html', error_message=error_message)

        @self.main_routes.route('/execute_query/<query_name>', methods=['GET'])
        def execute_query(query_name):
            try:
                result = []
                if query_name == 'listar_usuarios':
                    result = [{'ID': u.ID_usuario, 'Nome': u.Nome, 'Cargo': u.Cargo, 'Email': u.Email} for u in Usuario.listar_usuarios()]
                elif query_name == 'listar_predios':
                    result = [{'ID': p.ID_predio, 'Nome': p.Nome, 'Andares': p.Andares, 'Cor': p.Cor} for p in Predio.listar_predios()]
                elif query_name == 'listar_andares':
                    result = [{'ID': a.ID_andar, 'Numero': a.Numero, 'ID_predio': a.ID_predio} for a in Andar.listar_andares()]
                elif query_name == 'listar_salas':
                    result = [{'ID': s.ID_sala, 'Tipo': s.Tipo, 'ID_andar': s.ID_andar, 'Capacidade': s.Capacidade} for s in Sala.listar_salas()]
                elif query_name == 'listar_recursos':
                    result = [{'ID': r.ID_recurso, 'Nome': r.Nome, 'ID_sala': r.ID_sala, 'Identificacao': r.Identificacao, 'Status': r.Status} for r in Recurso.listar_recursos()]
                elif query_name == 'listar_recursos_alugaveis':
                    result = [{'ID': ra.ID_recurso_alugavel, 'Quantidade': ra.Quantidade, 'Identificacao': ra.Identificacao, 'Status': ra.Status} for ra in RecursoAlugavel.listar_recursos_alugaveis()]
                elif query_name == 'listar_turmas':
                    result = [{'ID': t.ID_turma, 'Quantidade': t.Quantidade, 'Data_inicio': t.Data_inicio.isoformat(), 'Data_Fim': t.Data_Fim.isoformat(), 'ID_turno': t.ID_turno, 'Curso': t.Curso, 'Cor': t.Cor} for t in Turma.listar_turmas()]
                elif query_name == 'listar_dias':
                    result = [{'ID': d.ID_dia, 'Nome': d.Nome} for d in Dia.listar_dias()]
                elif query_name == 'listar_professores':
                    result = [{'ID': p.ID_professor, 'Nome': p.Nome, 'Area': p.Area, 'CargaHoraria': p.CargaHoraria, 'TipoContrato': p.TipoContrato} for p in Professor.listar_professores()]
                elif query_name == 'listar_agendamentos':
                    result = [{'ID': a.ID_agendamento, 'TimeStamp_inicio': a.TimeStamp_inicio.isoformat(), 'ID_locatario': a.ID_locatario, 'Tipo_locatario': a.Tipo_locatario, 'ID_turma': a.ID_turma, 'TimeStamp_fim': a.TimeStamp_fim.isoformat()} for a in Agendamento.listar_agendamentos()]
                elif query_name == 'listar_turnos':
                    result = [{'ID': t.ID_turno, 'Nome_turno': t.Nome_turno, 'HorarioInicio': t.HorarioInicio.isoformat(), 'HorarioFim': t.HorarioFim.isoformat(), 'Cor': t.Cor} for t in Turno.listar_turnos()]
                elif query_name == 'listar_disponibilidades':
                    result = [{'ID': d.ID, 'ID_dia': d.ID_dia, 'ID_turno': d.ID_turno} for d in Disponibilidade.listar_disponibilidades()]
                else:
                    return jsonify({'error': 'Consulta não reconhecida'}), 400
                
                return jsonify(result)
            except Exception as e:
                logger.error(f"Erro ao executar consulta {query_name}: {str(e)}")
                return jsonify({'error': str(e)}), 500

        # Rotas de autenticação e cadastro (auth_routes)
        @self.auth_routes.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                email = request.form['email']
                senha = request.form['password']
                logger.debug(f"Tentativa de login para o email: {email}")
                usuario = Usuario.query.filter_by(Email=email).first()
                if usuario:
                    logger.debug(f"Usuário encontrado: {usuario.Nome}")
                    if usuario.Senha == senha:
                        session['user_id'] = usuario.ID_usuario
                        logger.info(f"Login bem-sucedido para o usuário: {usuario.Nome}")
                        flash('Login realizado com sucesso!', 'success')
                        return jsonify({'success': True, 'redirect': url_for('main.dashboard')})
                    else:
                        logger.warning(f"Senha incorreta para o usuário: {usuario.Nome}, {senha} - {usuario.Senha}")
                        return jsonify({'success': False, 'message': 'Senha incorreta. Por favor, tente novamente.'})
                else:
                    logger.warning(f"Tentativa de login com email não cadastrado: {email}")
                    return jsonify({'success': False, 'message': 'Email não encontrado. Por favor, verifique o email ou registre-se.'})
            return render_template('login.html')

        @self.auth_routes.route('/logout')
        def logout():
            session.pop('user_id', None)
            flash('Você foi desconectado.', 'info')
            return redirect(url_for('auth.login'))

        @self.auth_routes.route('/register_student')
        def register_student():
            return "Cadastro de Aluno"

        # Rota do dashboard
        @self.main_routes.route('/dashboard')
        def dashboard():
            if 'user_id' not in session:
                logger.warning("Tentativa de acesso ao dashboard sem login")
                flash('Por favor, faça login para acessar o dashboard.', 'error')
                return redirect(url_for('auth.login'))
            logger.info(f"Acesso ao dashboard pelo usuário ID: {session['user_id']}")
            return render_template('dashboard.html')

        @self.auth_routes.route('/schedule')
        def schedule():
            return "Agendamento de Aulas"
        
        
        # # Rota para registrar uma nova turma
        # @self.main_routes.route('/register_class', methods=['GET', 'POST'])
        # def register_class():
        #     if request.method == 'POST':
        #         # Lógica para registrar uma nova turma
        #         nova_sala = Sala(nome=request.form['name'])
        #         db.session.add(nova_sala)
        #         db.session.commit()
        #         flash('Turma registrada com sucesso!', 'success')
        #         return redirect(url_for('main.dashboard'))
        #     return render_template('register_class.html')

        # # Rota para agendar salas de aula
        # @self.main_routes.route('/schedule_classrooms', methods=['GET', 'POST'])
        # def schedule_classrooms():
        #     if request.method == 'POST':
        #         # Lógica para agendar salas de aula
        #         sala = Sala.query.get(request.form['classroom_id'])
        #         # Adicione aqui a lógica de agendamento
        #         flash('Sala de aula agendada com sucesso!', 'success')
        #         return redirect(url_for('main.dashboard'))
            
        #     salas = Sala.query.all()
        #     return render_template('schedule_classrooms.html', classrooms=salas)

        # Novas rotas
        @self.main_routes.route('/schedule/classrooms', methods=['POST'])
        def schedule_classroom():
            return render_template('codigo.html')

        @self.main_routes.route('/register-build', methods=['POST'])
        def register_build():
            return render_template('codigo.html')
        
        @self.main_routes.route('/register-classroom', methods=['POST'])
        def register_classroom():
            return render_template('codigo.html')

# Instanciando o gerenciador de rotas
route_manager = RouteManager(main_routes, auth_routes)