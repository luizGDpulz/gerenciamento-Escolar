from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from models import db # ,Sala  # Importa a instância do banco de dados e o modelo Sala

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
                print(debug_message)  # Para depuração no console
                return render_template('teste_db.html', debug_message=debug_message)
            except Exception as e:
                # Registre o erro para depuração
                error_message = f"Erro ao conectar ao banco de dados: {str(e)}"
                print(error_message)  # Para depuração no console
                return render_template('teste_db.html', error_message=error_message)

        # Rotas de autenticação e cadastro (auth_routes)
        @self.auth_routes.route('/login')
        def login():
            return render_template('login.html')

        @self.auth_routes.route('/register_student')
        def register_student():
            return "Cadastro de Aluno"

        # Rota do dashboard
        @self.main_routes.route('/dashboard')
        def dashboard():
            return render_template('dashboard.html')

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

        @self.auth_routes.route('/schedule')
        def schedule():
            return "Agendamento de Aulas"

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
