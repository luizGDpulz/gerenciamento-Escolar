# Tutorial: Como Fazer Merge de Pull Request Sem Conflitos em um Repositório Forkeado

## Pré-requisitos
- Um repositório forkeado no GitHub
- Git instalado na sua máquina
- Acesso ao repositório original (upstream) e ao fork (origin)
  
## Passo a Passo

### 1. **Clonar o repositório fork na sua máquina**

Primeiro, clone o repositório forkeado para o seu ambiente local:

```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
```

Entre na pasta do repositório:

```bash
cd NOME_DO_REPOSITORIO
```

### 2. **Adicionar o repositório original como upstream**

Adicione o repositório original (aquele que você forkeou) como um remote chamado `upstream`:

```bash
git remote add upstream https://github.com/ORIGINAL_USUARIO/NOME_DO_REPOSITORIO.git
```

Verifique se os remotes foram adicionados corretamente:

```bash
git remote -v
```

Isso deve mostrar algo assim:

```bash
origin    https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git (fetch)
origin    https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git (push)
upstream  https://github.com/ORIGINAL_USUARIO/NOME_DO_REPOSITORIO.git (fetch)
upstream  https://github.com/ORIGINAL_USUARIO/NOME_DO_REPOSITORIO.git (push)
```

### 3. **Buscar as atualizações do repositório original (upstream)**

Antes de começar a fazer o merge, certifique-se de buscar todas as atualizações do repositório original:

```bash
git fetch upstream
```

### 4. **Fazer checkout na branch onde deseja fazer o merge**

Verifique em qual branch você deseja fazer o merge. Se estiver na `main`, por exemplo, use:

```bash
git checkout main
```

### 5. **Mesclar a branch principal do repositório original ao fork**

Agora, faça o merge da branch principal do repositório original (upstream) para o seu fork. Normalmente, a branch principal é a `main`:

```bash
git merge upstream/main
```

Se houver conflitos, o Git avisará sobre os arquivos com problemas. Você precisará resolver manualmente.

### 6. **Resolver conflitos (se houver)**

1. Abra os arquivos com conflitos (indicados na saída do Git).
2. No arquivo, você verá seções marcadas com `<<<<<<<`, `=======`, e `>>>>>>>`. O conteúdo entre essas marcas representa as mudanças conflitantes.
3. Edite o arquivo para combinar as mudanças desejadas.
4. Após resolver os conflitos, marque o arquivo como resolvido:

```bash
git add NOME_DO_ARQUIVO
```

### 7. **Finalizar o merge**

Depois de resolver todos os conflitos e adicionar os arquivos, finalize o merge com o commit automático do Git:

```bash
git commit
```

Ou, se o merge foi feito sem conflitos, o Git fará o commit automaticamente.

### 8. **Enviar as mudanças para o seu fork**

Envie as mudanças para o seu fork no GitHub:

```bash
git push origin main
```

### 9. **Atualizar o pull request (se aplicável)**

Agora, o seu repositório forkeado está atualizado com as mudanças do repositório original, e você pode continuar trabalhando ou atualizar o pull request, se for o caso.

---

## Comandos resumidos

```bash
# Clonar o repositório forkeado
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO

# Adicionar o repositório original como upstream
git remote add upstream https://github.com/ORIGINAL_USUARIO/NOME_DO_REPOSITORIO.git

# Buscar as atualizações do upstream
git fetch upstream

# Fazer checkout na branch principal
git checkout main

# Fazer merge da branch principal do upstream para o fork
git merge upstream/main

# Resolver conflitos (se houver) e marcar arquivos resolvidos
git add NOME_DO_ARQUIVO

# Finalizar o merge
git commit

# Enviar para o fork
git push origin main
```

---
