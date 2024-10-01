from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância do SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    ID_usuario = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Cargo = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Senha = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.Nome}>'

    @classmethod
    def criar_usuario(cls, nome, cargo, email, senha):
        novo_usuario = cls(Nome=nome, Cargo=cargo, Email=email, Senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    @classmethod
    def listar_usuarios(cls):
        return cls.query.all()

class Predio(db.Model):
    __tablename__ = 'predios'
    ID_predio = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Andares = db.Column(db.Integer, nullable=False)
    Cor = db.Column(db.String(20))
    andares = db.relationship('Andar', backref='predio', lazy=True)

    def __repr__(self):
        return f'<Predio {self.Nome}>'

    @classmethod
    def criar_predio(cls, nome, andares, cor):
        novo_predio = cls(Nome=nome, Andares=andares, Cor=cor)
        db.session.add(novo_predio)
        db.session.commit()
        return novo_predio

    @classmethod
    def listar_predios(cls):
        return cls.query.all()

class Andar(db.Model):
    __tablename__ = 'andares'
    ID_andar = db.Column(db.Integer, primary_key=True)
    Numero = db.Column(db.Integer, nullable=False)
    ID_predio = db.Column(db.Integer, db.ForeignKey('predios.ID_predio'), nullable=False)
    salas = db.relationship('Sala', backref='andar', lazy=True)

    def __repr__(self):
        return f'<Andar {self.Numero} do Prédio {self.ID_predio}>'

    @classmethod
    def adicionar_andar(cls, numero, id_predio):
        novo_andar = cls(Numero=numero, ID_predio=id_predio)
        db.session.add(novo_andar)
        db.session.commit()
        return novo_andar

    @classmethod
    def listar_andares(cls):
        return cls.query.all()

class Sala(db.Model):
    __tablename__ = 'salas'
    ID_sala = db.Column(db.Integer, primary_key=True)
    Tipo = db.Column(db.String(50), nullable=False)
    ID_andar = db.Column(db.Integer, db.ForeignKey('andares.ID_andar'), nullable=False)
    Capacidade = db.Column(db.Integer, nullable=False)
    recursos = db.relationship('Recurso', backref='sala', lazy=True)

    def __repr__(self):
        return f'<Sala {self.ID_sala} do Andar {self.ID_andar}>'

    @classmethod
    def criar_sala(cls, tipo, id_andar, capacidade):
        nova_sala = cls(Tipo=tipo, ID_andar=id_andar, Capacidade=capacidade)
        db.session.add(nova_sala)
        db.session.commit()
        return nova_sala

    @classmethod
    def listar_salas(cls):
        return cls.query.all()

class Recurso(db.Model):
    __tablename__ = 'recursos'
    ID_recurso = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    ID_sala = db.Column(db.Integer, db.ForeignKey('salas.ID_sala'), nullable=False)
    Identificacao = db.Column(db.String(50), unique=True, nullable=False)
    Status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Recurso {self.Nome} da Sala {self.ID_sala}>'

    @classmethod
    def adicionar_recurso(cls, nome, id_sala, identificacao, status):
        novo_recurso = cls(Nome=nome, ID_sala=id_sala, Identificacao=identificacao, Status=status)
        db.session.add(novo_recurso)
        db.session.commit()
        return novo_recurso

    @classmethod
    def listar_recursos(cls):
        return cls.query.all()

class RecursoAlugavel(db.Model):
    __tablename__ = 'recursos_alugaveis'
    ID_recurso_alugavel = db.Column(db.Integer, primary_key=True)
    Quantidade = db.Column(db.Integer, nullable=False)
    Identificacao = db.Column(db.String(50), unique=True, nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    disponibilidades = db.relationship('RecursoAlugavelDisponibilidade', backref='recurso_alugavel', lazy=True)

    def __repr__(self):
        return f'<RecursoAlugavel {self.Identificacao}>'

    @classmethod
    def criar_recurso_alugavel(cls, quantidade, identificacao, status):
        novo_recurso_alugavel = cls(Quantidade=quantidade, Identificacao=identificacao, Status=status)
        db.session.add(novo_recurso_alugavel)
        db.session.commit()
        return novo_recurso_alugavel

    @classmethod
    def listar_recursos_alugaveis(cls):
        return cls.query.all()

class RecursoAlugavelDisponibilidade(db.Model):
    __tablename__ = 'recursos_alugaveis_disponibilidade'
    ID_recurso_alugavel_disponibilidade = db.Column(db.Integer, primary_key=True)
    Data = db.Column(db.Date, nullable=False)
    ID_turno = db.Column(db.Integer, db.ForeignKey('turnos.ID_turno'), nullable=False)
    ID_recurso_alugavel = db.Column(db.Integer, db.ForeignKey('recursos_alugaveis.ID_recurso_alugavel'), nullable=False)
    ID_locatario = db.Column(db.Integer, nullable=False)
    Tipo_locatario = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<RecursoAlugavelDisponibilidade {self.ID_recurso_alugavel_disponibilidade}>'

    @classmethod
    def listar_disponibilidades(cls):
        return cls.query.all()

class Turma(db.Model):
    __tablename__ = 'turmas'
    ID_turma = db.Column(db.Integer, primary_key=True)
    Quantidade = db.Column(db.Integer, nullable=False)
    Data_inicio = db.Column(db.Date, nullable=False)
    Data_Fim = db.Column(db.Date, nullable=False)
    ID_turno = db.Column(db.Integer, db.ForeignKey('turnos.ID_turno'), nullable=False)
    Curso = db.Column(db.String(100), nullable=False)
    Cor = db.Column(db.String(20))
    dias = db.relationship('TurmaDia', backref='turma', lazy=True)

    def __repr__(self):
        return f'<Turma {self.ID_turma} do Curso {self.Curso}>'

    @classmethod
    def criar_turma(cls, quantidade, data_inicio, data_fim, id_turno, curso, cor):
        nova_turma = cls(Quantidade=quantidade, Data_inicio=data_inicio, Data_Fim=data_fim,
                         ID_turno=id_turno, Curso=curso, Cor=cor)
        db.session.add(nova_turma)
        db.session.commit()
        return nova_turma

    @classmethod
    def listar_turmas(cls):
        return cls.query.all()

class TurmaDia(db.Model):
    __tablename__ = 'turma_dias'
    ID_turma_dia = db.Column(db.Integer, primary_key=True)
    ID_turma = db.Column(db.Integer, db.ForeignKey('turmas.ID_turma'), nullable=False)
    ID_dia = db.Column(db.Integer, db.ForeignKey('dias.ID_dia'), nullable=False)

    def __repr__(self):
        return f'<TurmaDia {self.ID_turma_dia}>'

    @classmethod
    def listar_turma_dias(cls):
        return cls.query.all()

class Dia(db.Model):
    __tablename__ = 'dias'
    ID_dia = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Dia {self.Nome}>'

    @classmethod
    def listar_dias(cls):
        return cls.query.all()

class Professor(db.Model):
    __tablename__ = 'professores'
    ID_professor = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Area = db.Column(db.String(50), nullable=False)
    CargaHoraria = db.Column(db.Integer, nullable=False)
    TipoContrato = db.Column(db.String(50), nullable=False)
    ID_disponibilidade = db.Column(db.Integer, db.ForeignKey('disponibilidade_professores.ID_disponibilidade_professor'))
    disponibilidades = db.relationship('DisponibilidadeProfessor', backref='professor', lazy=True)

    def __repr__(self):
        return f'<Professor {self.Nome}>'

    @classmethod
    def adicionar_professor(cls, nome, area, carga_horaria, tipo_contrato):
        novo_professor = cls(Nome=nome, Area=area, CargaHoraria=carga_horaria, TipoContrato=tipo_contrato)
        db.session.add(novo_professor)
        db.session.commit()
        return novo_professor

    @classmethod
    def listar_professores(cls):
        return cls.query.all()

class DisponibilidadeProfessor(db.Model):
    __tablename__ = 'disponibilidade_professores'
    ID_disponibilidade_professor = db.Column(db.Integer, primary_key=True)
    IDprofessor = db.Column(db.Integer, db.ForeignKey('professores.ID_professor'), nullable=False)

    def __repr__(self):
        return f'<DisponibilidadeProfessor {self.ID_disponibilidade_professor}>'

    @classmethod
    def listar_disponibilidades_professores(cls):
        return cls.query.all()

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    ID_agendamento = db.Column(db.Integer, primary_key=True)
    TimeStamp_inicio = db.Column(db.DateTime, nullable=False)
    ID_locatario = db.Column(db.Integer, nullable=False)
    Tipo_locatario = db.Column(db.String(50), nullable=False)
    ID_turma = db.Column(db.Integer, db.ForeignKey('turmas.ID_turma'))
    TimeStamp_fim = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Agendamento {self.ID_agendamento}>'

    @classmethod
    def criar_agendamento(cls, timestamp_inicio, id_locatario, tipo_locatario, id_turma, timestamp_fim):
        novo_agendamento = cls(TimeStamp_inicio=timestamp_inicio, ID_locatario=id_locatario,
                               Tipo_locatario=tipo_locatario, ID_turma=id_turma, TimeStamp_fim=timestamp_fim)
        db.session.add(novo_agendamento)
        db.session.commit()
        return novo_agendamento

    @classmethod
    def listar_agendamentos(cls):
        return cls.query.all()

class Turno(db.Model):
    __tablename__ = 'turnos'
    ID_turno = db.Column(db.Integer, primary_key=True)
    Nome_turno = db.Column(db.String(50), nullable=False)
    HorarioInicio = db.Column(db.Time, nullable=False)
    HorarioFim = db.Column(db.Time, nullable=False)
    Cor = db.Column(db.String(20))

    def __repr__(self):
        return f'<Turno {self.Nome_turno}>'

    @classmethod
    def criar_turno(cls, nome_turno, horario_inicio, horario_fim, cor):
        novo_turno = cls(Nome_turno=nome_turno, HorarioInicio=horario_inicio, HorarioFim=horario_fim, Cor=cor)
        db.session.add(novo_turno)
        db.session.commit()
        return novo_turno

    @classmethod
    def listar_turnos(cls):
        return cls.query.all()

class Disponibilidade(db.Model):
    __tablename__ = 'disponibilidade'
    ID = db.Column(db.Integer, primary_key=True)
    ID_dia = db.Column(db.Integer, db.ForeignKey('dias.ID_dia'), nullable=False)
    ID_turno = db.Column(db.Integer, db.ForeignKey('turnos.ID_turno'), nullable=False)

    def __repr__(self):
        return f'<Disponibilidade {self.ID}>'

    @classmethod
    def adicionar_disponibilidade(cls, id_dia, id_turno):
        nova_disponibilidade = cls(ID_dia=id_dia, ID_turno=id_turno)
        db.session.add(nova_disponibilidade)
        db.session.commit()
        return nova_disponibilidade

    @classmethod
    def listar_disponibilidades(cls):
        return cls.query.all()