# Documentação do Backend e Modelo de Entrega (UNIFOR - N695)

Este arquivo reúne o passo a passo para colocar o projeto no ar, o texto base seguindo os 13 tópicos do Modelo de Entrega do PDF da disciplina e o resumo dos testes realizados no backend.

---

## Parte A - Como publicar no Render e gerar o link para a equipe

O FastAPI já entrega os arquivos da pasta `front/` na rota `/` e responde pelas rotas da API em `/api`. Com isso, dá para subir o front e o backend juntos no mesmo serviço gratuito do Render.

1. Subam o projeto (`front/`, `backend/`, `render.yaml`, `README.md` e `.gitignore`) em um repositório público no GitHub.
2. Entrem em https://render.com usando a conta do GitHub.
3. Cliquem em **New +** -> **Web Service** e escolham o repositório.
4. Preencham os comandos do serviço:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`
5. Em **Environment Variables**, cadastrem as variáveis:
   - `DATABASE_URL` = string de conexão do Neon que está no `.env`
   - `ADMIN_USUARIO` = `admin`
   - `ADMIN_SENHA` = `admin123`
   - `JWT_SEGREDO` = uma chave secreta longa
6. Cliquem em **Deploy Web Service**. Quando finalizar, o Render gera o link público (ex.: `https://sabor-de-casa.onrender.com`).

---

## Parte B - Modelo de Entrega (Parte II do PDF da UNIFOR)

Substituam `SEU_USUARIO/SEU_REPO` pelo link do GitHub da equipe e coloquem os prints nos tópicos indicados.

### 1. Identificação (capa)
- **Instituição:** Universidade de Fortaleza (UNIFOR) - Centro de Ciências Tecnológicas
- **Disciplina:** N695 - Desenvolvimento de Plataformas Web
- **Turma:** *(preencher turma)*
- **Cenário escolhido:** Cenário 3 - Marmitaria com cardápio digital (*Sabor de Casa*)
- **Integrantes (Nome completo e Matrícula):**
  - *(Nome Completo 1 - Matrícula)*
  - *(Nome Completo 2 - Matrícula)*
  - *(Nome Completo 3 - Matrícula)*
  - *(Nome Completo 4 - Matrícula)*

### 2. Links de acesso
- **Repositório público no GitHub:** `https://github.com/SEU_USUARIO/SEU_REPO`
- **Aplicação publicada:** `https://SEU-APP.onrender.com`
- **Swagger da API:** `https://SEU-APP.onrender.com/docs`

### 3. Cenário escolhido e justificativa
Escolhemos o **Cenário 3: Marmitaria com cardápio digital ("Sabor de Casa")**. No problema descrito, a marmitaria recebia pedidos por aplicativo de mensagens mandando foto de um quadro escrito à mão. Sempre que um prato acabava ou mudava de valor, a foto antiga continuava circulando e gerava confusão nos pedidos. Escolhemos esse tema porque ele retrata uma situação comum em pequenos restaurantes e encaixa bem o relacionamento de 1 para N entre **Categoria** e **Prato**, separando o cardápio público da tela de administração.

### 4. Visão geral da solução
O sistema **Sabor de Casa** tem duas partes principais:
1. **Cardápio Público (`index.html`):** aberto para qualquer cliente, busca as categorias e os pratos disponíveis na API e mostra os valores formatados em reais.
2. **Painel de Gerenciamento (`login.html`, `gerenciamento.html`, `categoria-form.html`, `pratos.html`, `prato-form.html`):** exige login e permite criar, listar, pesquisar, editar e excluir categorias e pratos.

**Relação entre as entidades:**
- **Categoria (`id`, `nome`, `descricao`):** reúne vários pratos do cardápio.
- **Prato (`id`, `categoria_id`, `nome`, `descricao`, `preco`, `disponivel`):** fica ligado a uma categoria pela coluna `categoria_id` (`FOREIGN KEY ... ON DELETE RESTRICT`).

### 5. Ferramentas e stack utilizadas
- **Interface (Front-end):** HTML5, CSS3 e JavaScript puro consumindo a API com `fetch`.
- **Serviço Web (Back-end):** Python 3, FastAPI, Uvicorn, Pydantic e PyJWT.
- **Persistência dos dados:** Banco PostgreSQL hospedado no **Neon**, acessado com SQLAlchemy 2.0 e driver `psycopg`.
- **Hospedagem:** Render conectado ao banco do Neon.

### 6. Interface
*(Colocar no PDF as capturas de tela das páginas:)*
1. Cardápio público (`index.html`).
2. Tela de login (`login.html`).
3. Lista de categorias no gerenciamento (`gerenciamento.html`).
4. Cadastro/edição de categoria (`categoria-form.html`).
5. Lista de pratos de uma categoria (`pratos.html`).
6. Cadastro/edição de prato (`prato-form.html`).

- **Links para o código da Interface no GitHub:**
  - Pasta do front: `https://github.com/SEU_USUARIO/SEU_REPO/tree/main/front`
  - Chamadas da API no front: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/front/js/api.js`

### 7. Serviço Web
A API foi feita em FastAPI com o prefixo `/api` e atende todas as operações de **Categoria** e **Prato**:

| Recurso | Método e Rota | O que faz | Acesso |
|---|---|---|---|
| Autenticação | `POST /api/auth/login` | Valida usuário/senha e devolve o token JWT | Público |
| Categoria | `GET /api/categorias` | Lista as categorias trazendo `total_pratos` | Público |
| Categoria | `GET /api/categorias/{id}` | Busca uma categoria pelo ID | Público |
| Categoria | `POST /api/categorias` | Cadastra uma nova categoria | Admin (JWT) |
| Categoria | `PUT /api/categorias/{id}` | Atualiza os dados de uma categoria | Admin (JWT) |
| Categoria | `DELETE /api/categorias/{id}` | Exclui uma categoria sem pratos | Admin (JWT) |
| Prato | `GET /api/categorias/{id}/pratos` | Lista os pratos da categoria | Público |
| Prato | `POST /api/categorias/{id}/pratos` | Cadastra um prato na categoria | Admin (JWT) |
| Prato | `GET /api/pratos/{id}` | Busca um prato pelo ID | Público |
| Prato | `PUT /api/pratos/{id}` | Atualiza um prato | Admin (JWT) |
| Prato | `DELETE /api/pratos/{id}` | Exclui um prato | Admin (JWT) |

- **Links para os arquivos do Serviço Web no GitHub:**
  - Arquivo principal: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/main.py`
  - Rotas de categorias: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/api/rotas/categorias.py`
  - Rotas de pratos: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/api/rotas/pratos.py`
  - Rota de login: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/api/rotas/autenticacao.py`
  - Camada de serviços: `https://github.com/SEU_USUARIO/SEU_REPO/tree/main/backend/app/servicos`

*(Colocar no PDF prints das requisições e respostas feitas no `/docs` ou na aba Network).*

### 8. Persistência dos dados
Os dados ficam salvos no banco PostgreSQL no **Neon**, nas tabelas `categoria` e `prato`. Além das validações no código Python, o próprio banco tem constraints para garantir os dados:
- Índice único `uq_categoria_nome_lower` em `lower(nome)` na tabela `categoria`.
- Chave estrangeira `prato_categoria_id_fkey` (`ON DELETE RESTRICT`).
- Check constraint `ck_prato_preco_positivo` (`preco > 0`).

O backend conversa com o banco pela pasta `app/dados`, usando sessões do SQLAlchemy e classes de repositório para separar o SQL do restante do código.

- **Links para o código de Persistência no GitHub:**
  - SQL das tabelas: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/banco/schema.sql`
  - Conexão com o banco: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/dados/banco.py`
  - Modelos (`Categoria` e `Prato`): `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/dados/modelos.py`
  - Repositório de categorias: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/dados/categoria_repositorio.py`
  - Repositório de pratos: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/dados/prato_repositorio.py`

### 9. Validação de entrada e tratamento de erros
Regras do Cenário 3 implementadas no projeto:
1. **Campos obrigatórios:** o nome da categoria e o nome/preço do prato são cobrados tanto no formulário quanto no Pydantic (`validar_texto_obrigatorio`), devolvendo erro `422` se vierem vazios.
2. **Preço maior que zero:** a função `validar_preco` aceita valores com vírgula ou ponto (`18,90` ou `18.90`), exige número maior que zero e com até duas casas decimais, retornando *"O preço deve ser maior que zero."* quando inválido.
3. **Nome de categoria sem repetição:** o método `_garantir_nome_unico` em `CategoriaServico` compara o nome usando `lower()` no banco e retorna status `409` se já existir outra categoria igual.
4. **Impedir exclusão de categoria com pratos:** antes de apagar, `_garantir_sem_pratos` verifica quantos pratos estão ligados à categoria e barra a exclusão com status `409` caso o total seja maior que zero.

- **Links para o código de Validação e Erros no GitHub:**
  - Funções de validação: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/esquemas/validadores.py`
  - Esquemas de entrada e saída: `https://github.com/SEU_USUARIO/SEU_REPO/tree/main/backend/app/esquemas`
  - Regras de categoria: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/servicos/categoria_servico.py`
  - Tratamento de erros HTTP: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/api/tratadores_erros.py`

*(Colocar no PDF os prints das mensagens de erro aparecendo na tela).*

### 10. Técnicas de clean code aplicadas
1. **Nomes significativos:** funções, classes e variáveis usam nomes diretos em português que deixam claro o papel de cada trecho (`listar_com_total_de_pratos`, `validar_texto_obrigatorio`, `_garantir_sem_pratos`).
   - Link: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/servicos/categoria_servico.py`
2. **Funções curtas com responsabilidade única:** cada função resolve apenas um passo (por exemplo, em `validadores.py`, converter o texto para decimal, checar o tamanho máximo e validar o preço ficam separados).
   - Link: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/esquemas/validadores.py`
3. **Separação em camadas (interface, serviço e dados):** a interface fica em `front/`, as rotas HTTP em `backend/app/api/`, as regras de negócio em `backend/app/servicos/` e o acesso ao banco em `backend/app/dados/`.
   - Link: `https://github.com/SEU_USUARIO/SEU_REPO/tree/main/backend/app`
4. **Ausência de código duplicado:** os métodos básicos de banco (`buscar_por_id`, `salvar`, `excluir`) ficam em `RepositorioBase` e são reaproveitados pelos dois repositórios.
   - Link: `https://github.com/SEU_USUARIO/SEU_REPO/blob/main/backend/app/dados/repositorio_base.py`

### 11. Declaração de uso de IA generativa
Declaramos que a equipe utilizou ferramentas de IA generativa como apoio durante o desenvolvimento para auxiliar na montagem da estrutura em camadas do backend em FastAPI, na configuração do SQLAlchemy com o banco Neon e na escrita dos scripts de teste. Todo o código foi revisado, testado e integrado pela equipe.

### 12. Considerações finais e aprendizados da equipe
O trabalho ajudou a equipe a praticar como o front-end conversa de verdade com uma API REST e um banco PostgreSQL na nuvem. As principais lições foram alinhar o formato dos dados e das mensagens de erro entre o JavaScript e o FastAPI, proteger as rotas de cadastro/edição/exclusão com token JWT e dividir o backend em camadas para facilitar a manutenção.

### 13. Referências
- FASTAPI. Documentação oficial: https://fastapi.tiangolo.com/
- SQLALCHEMY. Documentação oficial: https://docs.sqlalchemy.org/
- NEON. Documentação Serverless Postgres: https://neon.tech/docs
- MDN WEB DOCS. Fetch API: https://developer.mozilla.org/pt-BR/

---

## Parte C - Como os testes foram feitos

Para testar o backend sem depender apenas de cliques manuais, montamos dois arquivos de teste (`backend/executar_testes.py` e `backend/tests/test_api.py`), além do teste direto com o banco no Neon:

1. **Execução do script de testes das regras de negócio (`backend/executar_testes.py`):**
   Rodando `.\backend\.venv\Scripts\python.exe backend\executar_testes.py`, o script cria um banco em memória limpo e testa:
   - Login do administrador e validação do token JWT.
   - Rejeição de login com senha errada (`401`).
   - Criação, listagem, atualização e exclusão de categorias e pratos.
   - Bloqueio de categoria com nome repetido ignorando maiúsculas e minúsculas (`409`).
   - Bloqueio de prato com preço menor ou igual a zero (`422`).
   - Bloqueio de campos obrigatórios em branco (`422`).
   - Conversão de preço digitado com vírgula (`"18,90"` para `18.90`).
   - Bloqueio de exclusão de categoria que ainda tem pratos (`409`).

2. **Teste de conexão real com o Neon:**
   Com o servidor rodando em `http://127.0.0.1:8000`, a rota `GET /api/saude` executa `SELECT 1` no PostgreSQL do Neon e a rota `GET /api/categorias` retorna os dados reais gravados no banco.
