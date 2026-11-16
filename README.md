# Sabor de Casa - Cardápio Digital

Projeto da disciplina **N695 - Desenvolvimento de Plataformas Web (UNIFOR)**, referente ao **Cenário 3: Marmitaria com cardápio digital**.

## O que o sistema faz

- Cardápio público separado por categorias (mostra apenas os pratos marcados como disponíveis).
- Login com token JWT para entrar na área administrativa.
- Cadastro, listagem, busca, edição e exclusão de categorias.
- Cadastro, listagem, busca, filtro por disponibilidade, edição e exclusão de pratos.
- Validações pedidas no cenário:
  - Campos obrigatórios verificados no front e na API.
  - Preço do prato maior que zero (`> 0`).
  - Nome de categoria sem repetição (comparação ignorando maiúsculas e minúsculas).
  - Bloqueio ao tentar excluir uma categoria que ainda tenha pratos cadastrados.

## Estrutura de pastas

```
projeto sabor de casa/
|-- front/
|   |-- index.html
|   |-- login.html
|   |-- gerenciamento.html
|   |-- categoria-form.html
|   |-- pratos.html
|   |-- prato-form.html
|   |-- css/estilos.css
|   `-- js/
|       |-- config.js
|       |-- autenticacao.js
|       |-- api.js
|       |-- comum.js
|       |-- inicio.js
|       |-- login.js
|       |-- categorias.js
|       |-- categoria-form.js
|       |-- pratos.js
|       `-- prato-form.js
`-- backend/
    |-- .env.example
    |-- requirements.txt
    |-- executar_testes.py
    |-- banco/
    |   `-- schema.sql
    `-- app/
        |-- main.py
        |-- config.py
        |-- erros.py
        |-- api/
        |   |-- dependencias.py
        |   |-- tratadores_erros.py
        |   `-- rotas/
        |       |-- autenticacao.py
        |       |-- categorias.py
        |       |-- pratos.py
        |       `-- saude.py
        |-- esquemas/
        |   |-- validadores.py
        |   |-- autenticacao.py
        |   |-- categoria.py
        |   `-- prato.py
        |-- servicos/
        |   |-- autenticacao_servico.py
        |   |-- categoria_servico.py
        |   `-- prato_servico.py
        `-- dados/
            |-- banco.py
            |-- modelos.py
            |-- repositorio_base.py
            |-- categoria_repositorio.py
            `-- prato_repositorio.py
```

## Como rodar na máquina

1. Entre na pasta `backend` e ative o ambiente virtual:
   ```powershell
   cd backend
   .\.venv\Scripts\activate
   ```
2. Crie o arquivo `.env` a partir do `.env.example` e preencha `DATABASE_URL` (string de conexão do Neon), `ADMIN_USUARIO`, `ADMIN_SENHA` e `JWT_SEGREDO`.
3. Suba o servidor:
   ```powershell
   uvicorn app.main:app --reload
   ```
4. Abra no navegador:
   - Sistema: http://127.0.0.1:8000
   - Documentação das rotas (Swagger): http://127.0.0.1:8000/docs
