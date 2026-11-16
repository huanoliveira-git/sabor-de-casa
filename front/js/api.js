const URL_BASE = `${window.CONFIGURACAO.URL_API}/api`;

async function fazerRequisicao(caminho, opcoes = {}) {
  let resposta;
  const cabecalhos = { ...opcoes.headers };
  const token = pegarToken();

  if (opcoes.body !== undefined) {
    cabecalhos["Content-Type"] = "application/json";
  }

  if (token) {
    cabecalhos.Authorization = `Bearer ${token}`;
  }

  try {
    resposta = await fetch(`${URL_BASE}${caminho}`, {
      ...opcoes,
      headers: cabecalhos
    });
  } catch {
    throw new Error("O servidor não respondeu.");
  }

  if (resposta.status === 204) {
    return null;
  }

  let dados;

  try {
    dados = await resposta.json();
  } catch {
    dados = null;
  }

  if (!resposta.ok) {
    if (resposta.status === 401 && caminho !== "/auth/login") {
      removerToken();
      window.location.href = "login.html";
    }

    const detalhes = Array.isArray(dados?.detail)
      ? dados.detail.map(item => item.msg).join("; ")
      : dados?.detail;
    const mensagem = dados?.erro?.mensagem
      || detalhes
      || "O servidor não conseguiu concluir a operação.";
    throw new Error(mensagem);
  }

  return dados;
}

const api = {
  entrar(usuario, senha) {
    return fazerRequisicao("/auth/login", {
      method: "POST",
      body: JSON.stringify({ usuario, senha })
    });
  },

  listarCategorias() {
    return fazerRequisicao("/categorias");
  },

  buscarCategoria(id) {
    return fazerRequisicao(`/categorias/${id}`);
  },

  criarCategoria(categoria) {
    return fazerRequisicao("/categorias", {
      method: "POST",
      body: JSON.stringify(categoria)
    });
  },

  atualizarCategoria(id, categoria) {
    return fazerRequisicao(`/categorias/${id}`, {
      method: "PUT",
      body: JSON.stringify(categoria)
    });
  },

  excluirCategoria(id) {
    return fazerRequisicao(`/categorias/${id}`, { method: "DELETE" });
  },

  listarPratos(categoriaId) {
    return fazerRequisicao(`/categorias/${categoriaId}/pratos`);
  },

  buscarPrato(id) {
    return fazerRequisicao(`/pratos/${id}`);
  },

  criarPrato(categoriaId, prato) {
    return fazerRequisicao(`/categorias/${categoriaId}/pratos`, {
      method: "POST",
      body: JSON.stringify(prato)
    });
  },

  atualizarPrato(id, prato) {
    return fazerRequisicao(`/pratos/${id}`, {
      method: "PUT",
      body: JSON.stringify(prato)
    });
  },

  excluirPrato(id) {
    return fazerRequisicao(`/pratos/${id}`, { method: "DELETE" });
  }
};
