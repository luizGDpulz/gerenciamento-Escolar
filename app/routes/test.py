from flask import Blueprint, render_template, jsonify, request
from models import *
from sqlalchemy import text
import logging
from werkzeug.security import generate_password_hash
from routes.admin import admin_required  

test = Blueprint('test', __name__)

logger = logging.getLogger(__name__)


@test.route('/test_db')
@admin_required
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

@test.route('/execute_query/<query_name>', methods=['GET'])
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

@test.route('/insert_data', methods=['POST'])
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

