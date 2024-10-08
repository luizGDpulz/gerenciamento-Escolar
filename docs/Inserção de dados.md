# Inserção de Dados
---
Este documento descreve como realizar a inserção de dados nas tabelas do banco de dados do Sistema de Gerenciamento Escolar. Abaixo estão os exemplos de comandos SQL para cada uma das tabelas.
---
## Tabela `agendamentos`

Inserção de dados para agendamento de uma sala ou recurso:
```sql
INSERT INTO `agendamentos` (`ID_agendamento`, `TimeStamp_inicio`, `ID_locatario`, `Tipo_locatario`, `ID_turma`, `TimeStamp_fim`)
VALUES (1, '2024-10-01 08:00:00', 3, 'Professor', 2, '2024-10-01 10:00:00');
```

## Tabela `andares`

Inserção de um novo andar em um prédio:
```sql
INSERT INTO `andares` (`ID_andar`, `Numero`, `ID_predio`)
VALUES (1, 1, 1);
```

## Tabela `dias`

Inserção de dias da semana:
```sql
INSERT INTO `dias` (`ID_dia`, `Nome`)
VALUES (1, 'Segunda-feira'),
       (2, 'Terça-feira'),
       (3, 'Quarta-feira');
```

## Tabela `disponibilidade`

Inserção de disponibilidade para um dia e turno:
```sql
INSERT INTO `disponibilidade` (`ID_disponibilidade`, `ID_dia`, `ID_turno`)
VALUES (1, 1, 1);
```

## Tabela `disponibilidade_professores`

Inserção de disponibilidade de um professor:
```sql
INSERT INTO `disponibilidade_professores` (`ID_disponibilidade_professor`, `ID_professor`, `ID_disponibilidade`)
VALUES (1, 2, 1);
```

## Tabela `predios`

Inserção de um novo prédio:
```sql
INSERT INTO `predios` (`ID_predio`, `Nome`, `Andares`, `Cor`)
VALUES (1, 'Prédio A', 5, 'Azul');
```

## Tabela `professores`

Inserção de um novo professor:
```sql
INSERT INTO `professores` (`ID_professor`, `Nome`, `Area`, `CargaHoraria`, `TipoContrato`, `ID_disponibilidade`)
VALUES (1, 'João da Silva', 'Matemática', 40, 'Integral', 1);
```

## Tabela `recursos`

Inserção de recursos (por exemplo, projetores ou computadores) em uma sala:
```sql
INSERT INTO `recursos` (`ID_recurso`, `Nome`, `ID_sala`, `Identificacao`, `Status`)
VALUES (1, 'Projetor', 101, 'Proj-101', 'Disponível');
```

## Tabela `recursos_alugaveis`

Inserção de recursos alugáveis (como mesas e cadeiras):
```sql
INSERT INTO `recursos_alugaveis` (`ID_recurso_alugavel`, `Quantidade`, `Identificacao`, `Status`, `ID_sala`)
VALUES (1, 10, 'Mesa-101', 'Disponível', 101);
```

## Tabela `recursos_alugaveis_disponibilidade`

Inserção de disponibilidade para aluguel de recursos:
```sql
INSERT INTO `recursos_alugaveis_disponibilidade` (`ID_recurso_alugavel_disponibilidade`, `Data`, `ID_turno`, `ID_recurso_alugavel`, `ID_locatario`, `Tipo_locatario`)
VALUES (1, '2024-10-05', 1, 1, 2, 'Professor');
```

## Tabela `salas`

Inserção de salas:
```sql
INSERT INTO `salas` (`ID_sala`, `Tipo`, `ID_andar`, `Capacidade`)
VALUES (101, 'Laboratório', 1, 30);
```

## Tabela `turmas`

Inserção de turmas:
```sql
INSERT INTO `turmas` (`ID_turma`, `Quantidade`, `Data_inicio`, `Data_fim`, `ID_turno`, `Curso`, `Cor`)
VALUES (1, 30, '2024-01-10', '2024-06-30', 1, 'Matemática', 'Verde');
```

## Tabela `turma_dias`

Inserção dos dias da semana em que uma turma ocorre:
```sql
INSERT INTO `turma_dias` (`ID_turma_dia`, `ID_turma`, `ID_dia`)
VALUES (1, 1, 1),
       (2, 1, 3);
```

## Tabela `turnos`

Inserção de turnos:
```sql
INSERT INTO `turnos` (`ID_turno`, `Nome_turno`, `HorarioInicio`, `HorarioFim`, `Cor`)
VALUES (1, 'Matutino', '08:00:00', '12:00:00', 'Azul');
```

## Tabela `usuarios`

Inserção de usuários:
```sql
INSERT INTO `usuarios` (`ID_usuario`, `Nome`, `Cargo`, `Email`, `Senha`)
VALUES (1, 'Carlos Santos', 'Professor', 'carlos.santos@email.com', 'senha123');
```
