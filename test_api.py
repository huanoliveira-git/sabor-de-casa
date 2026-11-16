def criar_categoria(cliente, nome="Marmitas", descricao="Pratos do dia"):
    return cliente.post("/api/categorias", json={"nome": nome, "descricao": descricao})


def criar_prato(cliente, categoria_id, **campos):
    dados = {"nome": "Frango grelhado", "descricao": None, "preco": "18,90", "disponivel": True}
    dados.update(campos)
    return cliente.post(f"/api/categorias/{categoria_id}/pratos", json=dados)


def test_login_com_senha_errada_retorna_401(cliente):
    resposta = cliente.post("/api/auth/login", json={"usuario": "admin", "senha": "x"})
    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Usuário ou senha inválidos."


def test_escrita_sem_token_retorna_401(cliente):
    resposta = criar_categoria(cliente)
    assert resposta.status_code == 401


def test_token_invalido_retorna_401(cliente):
    cliente.headers["Authorization"] = "Bearer token-falso"
    assert criar_categoria(cliente).status_code == 401


def test_crud_completo_de_categoria(admin):
    criada = criar_categoria(admin)
    assert criada.status_code == 201
    categoria_id = criada.json()["id"]
    assert criada.json()["total_pratos"] == 0

    assert admin.get(f"/api/categorias/{categoria_id}").json()["nome"] == "Marmitas"

    editada = admin.put(
        f"/api/categorias/{categoria_id}", json={"nome": "Executivos", "descricao": ""}
    )
    assert editada.status_code == 200
    assert editada.json() == {
        "id": categoria_id,
        "nome": "Executivos",
        "descricao": None,
        "total_pratos": 0,
    }

    assert admin.delete(f"/api/categorias/{categoria_id}").status_code == 204
    assert admin.get(f"/api/categorias/{categoria_id}").status_code == 404


def test_listagem_e_publica_e_traz_total_de_pratos(admin):
    categoria_id = criar_categoria(admin).json()["id"]
    criar_prato(admin, categoria_id)
    admin.headers.pop("Authorization")

    lista = admin.get("/api/categorias")
    assert lista.status_code == 200
    assert lista.json()[0]["total_pratos"] == 1


def test_nome_de_categoria_obrigatorio(admin):
    resposta = criar_categoria(admin, nome="   ")
    assert resposta.status_code == 422
    assert resposta.json()["detail"] == "O campo nome é obrigatório."


def test_nome_de_categoria_nao_pode_repetir_ignorando_maiusculas(admin):
    criar_categoria(admin, nome="Marmitas")
    resposta = criar_categoria(admin, nome="  MARMITAS ")
    assert resposta.status_code == 409
    assert "Já existe uma categoria" in resposta.json()["detail"]


def test_editar_categoria_mantendo_o_proprio_nome(admin):
    categoria_id = criar_categoria(admin, nome="Marmitas").json()["id"]
    resposta = admin.put(f"/api/categorias/{categoria_id}", json={"nome": "marmitas"})
    assert resposta.status_code == 200


def test_nao_exclui_categoria_com_pratos(admin):
    categoria_id = criar_categoria(admin).json()["id"]
    criar_prato(admin, categoria_id)
    resposta = admin.delete(f"/api/categorias/{categoria_id}")
    assert resposta.status_code == 409
    assert "ainda possui 1 prato" in resposta.json()["detail"]


def test_crud_completo_de_prato(admin):
    categoria_id = criar_categoria(admin).json()["id"]
    criado = criar_prato(admin, categoria_id)
    assert criado.status_code == 201
    prato = criado.json()
    assert prato["preco"] == "18.90"
    assert prato["disponivel"] is True

    lista = admin.get(f"/api/categorias/{categoria_id}/pratos")
    assert [item["id"] for item in lista.json()] == [prato["id"]]

    editado = admin.put(
        f"/api/pratos/{prato['id']}",
        json={
            "nome": "Frango",
            "descricao": "Com arroz",
            "preco": "20",
            "disponivel": False,
            "categoria_id": categoria_id,
        },
    )
    assert editado.status_code == 200
    assert editado.json()["preco"] == "20.00"
    assert editado.json()["disponivel"] is False

    assert admin.delete(f"/api/pratos/{prato['id']}").status_code == 204
    assert admin.get(f"/api/pratos/{prato['id']}").status_code == 404


def test_preco_deve_ser_maior_que_zero(admin):
    categoria_id = criar_categoria(admin).json()["id"]
    resposta = criar_prato(admin, categoria_id, preco="0")
    assert resposta.status_code == 422
    assert resposta.json()["detail"] == "O preço deve ser maior que zero."


def test_preco_com_mais_de_duas_casas_e_recusado(admin):
    categoria_id = criar_categoria(admin).json()["id"]
    resposta = criar_prato(admin, categoria_id, preco="10,999")
    assert resposta.status_code == 422


def test_campos_obrigatorios_do_prato(admin):
    categoria_id = criar_categoria(admin).json()["id"]
    resposta = admin.post(f"/api/categorias/{categoria_id}/pratos", json={"descricao": "x"})
    assert resposta.status_code == 422
    assert "nome é obrigatório" in resposta.json()["detail"]
    assert "preço é obrigatório" in resposta.json()["detail"]


def test_prato_em_categoria_inexistente_retorna_404(admin):
    resposta = criar_prato(admin, 999)
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Categoria não encontrada."


def test_front_e_servido_na_raiz(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "Sabor de Casa" in resposta.text
