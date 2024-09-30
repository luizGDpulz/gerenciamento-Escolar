Para documentar no GitHub o processo de inserção de dados no banco de dados `sistema_gerenciamento_escolar`, usando o código SQL fornecido, a documentação poderia ser estruturada da seguinte forma:

---

# Sistema de Gerenciamento Escolar - Inserção de Dados

Este projeto utiliza um banco de dados MySQL para gerenciar um sistema escolar, incluindo agendamentos, professores, salas, turmas e mais. Abaixo, você encontrará instruções detalhadas sobre como adicionar dados às principais tabelas do banco de dados.

## Estrutura do Banco de Dados

O banco de dados contém as seguintes tabelas:
- `agendamentos`
- `andares`
- `dias`
- `disponibilidade`
- `disponibilidade_professores`
- `predios`
- `professores`
- `recursos`
- `recursos_alugaveis`
- `recursos_alugaveis_disponibilidade`
- `salas`
- `turmas`
- `turma_dias`
- `turnos`
- `usuarios`

## Inserindo Dados no Banco de Dados

### 1. Inserindo dados na tabela `usuarios`
A tabela `usuarios` contém informações sobre os usuários do sistema (como professores e locatários).

```sql
INSERT INTO usuarios (Nome, Cargo, Email, Senha) 
VALUES ('Maria Silva', 'Professora', 'maria.silva@escola.com', 'senha123');
```

### 2. Inserindo dados na tabela `professores`
A tabela `professores` armazena informações sobre os professores.

```sql
INSERT INTO professores (Nome, Area, CargaHoraria, TipoContrato, ID_disponibilidade) 
VALUES ('Carlos Lima', 'Matemática', 40, 'Integral', NULL);
```

### 3. Inserindo dados na tabela `turmas`
A tabela `turmas` armazena informações sobre as turmas.

```sql
INSERT INTO turmas (Quantidade, Data_inicio, Data_fim, ID_turno, Curso, Cor) 
VALUES (30, '2024-01-10', '2024-12-15', 1, 'Matemática Avançada', '#FF5733');
```

### 4. Inserindo dados na tabela `salas`
A tabela `salas` armazena informações sobre as salas do prédio escolar.

```sql
INSERT INTO salas (Tipo, ID_andar, Capacidade) 
VALUES ('Laboratório', 2, 25);
```

### 5. Inserindo dados na tabela `agendamentos`
A tabela `agendamentos` gerencia o agendamento de recursos e salas.

```sql
INSERT INTO agendamentos (TimeStamp_inicio, ID_locatario, Tipo_locatario, ID_turma, TimeStamp_fim) 
VALUES ('2024-09-28 08:00:00', 1, 'Professor', 1, '2024-09-28 10:00:00');
```

### 6. Inserindo dados na tabela `recursos`
A tabela `recursos` armazena informações sobre os recursos disponíveis nas salas.

```sql
INSERT INTO recursos (Nome, ID_sala, Identificacao, Status) 
VALUES ('Projetor', 1, 'PJ-001', 'Disponível');
```

### 7. Inserindo dados na tabela `turnos`
A tabela `turnos` contém informações sobre os turnos de aulas.

```sql
INSERT INTO turnos (Nome_turno, HorarioInicio, HorarioFim, Cor) 
VALUES ('Matutino', '08:00:00', '12:00:00', '#FF5733');
```
