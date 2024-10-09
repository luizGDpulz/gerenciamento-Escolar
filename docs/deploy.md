Clone o repositório do GitHub: Se ainda não tiver o código localmente, faça o clone do repositório:

```bash

git clone https://github.com/gdbarros94/gerenciamento-Escolar.git
cd gerenciamento-Escolar
```
Crie um arquivo requirements.txt se não existir (garanta que todas as dependências do seu projeto estão listadas, por exemplo, Flask):

```txt

Flask==2.1.1
```
(Substitua a versão do Flask pela que o projeto utiliza).

Construa a imagem Docker: No diretório onde está o Dockerfile, execute:

```bash

docker build -t class_manager .
```
Execute o contêiner: Depois de construir a imagem, inicie o contêiner com o comando:

```bash

    docker run -d -p 5000:5000 --name class_manager class_manager
```
Isso vai criar um contêiner chamado "class_manager", que expõe a aplicação Flask na porta 5000 do seu host local.

Verifique o funcionamento acessando ``` http://localhost:5000 ``` no navegador.
