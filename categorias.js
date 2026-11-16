const listaCategorias = document.querySelector("#lista-categorias");
const campoPesquisa = document.querySelector("#pesquisa");
let categorias = [];

exigirLogin();

function montarCartaoCategoria(categoria) {
  const nome = protegerTexto(categoria.nome);
  const descricao = protegerTexto(categoria.descricao || "Sem descrição.");
  const quantidade = Number(categoria.total_pratos);
  const textoQuantidade = Number.isFinite(quantidade)
    ? quantidade === 1 ? "1 prato" : `${quantidade} pratos`
    : "Ver pratos cadastrados";

  return `
    <article class="cartao">
      <div class="cartao-conteudo">
        <h2>${nome}</h2>
        <p>${descricao}</p>
        <strong>${textoQuantidade}</strong>
      </div>
      <div class="acoes">
        <a class="botao botao-principal" href="pratos.html?categoriaId=${categoria.id}">Ver pratos</a>
        <a class="botao botao-secundario" href="categoria-form.html?id=${categoria.id}">Editar</a>
        <button class="botao botao-perigo" type="button" data-excluir="${categoria.id}">Excluir</button>
      </div>
    </article>
  `;
}

function exibirCategorias() {
  const termo = campoPesquisa.value.trim().toLowerCase();
  const filtradas = categorias.filter(categoria => categoria.nome.toLowerCase().includes(termo));

  if (filtradas.length === 0) {
    listaCategorias.innerHTML = '<p class="estado-lista">Nenhuma categoria encontrada.</p>';
    return;
  }

  listaCategorias.innerHTML = filtradas.map(montarCartaoCategoria).join("");
}

async function carregarCategorias() {
  esconderMensagem();

  try {
    categorias = await api.listarCategorias();
    exibirCategorias();
  } catch (erro) {
    listaCategorias.innerHTML = '<p class="estado-lista">Erro ao carregar as categorias.</p>';
    mostrarMensagem(erro.message);
  }
}

async function excluirCategoria(id, nome) {
  const confirmou = window.confirm(`Excluir a categoria "${nome}"?`);

  if (!confirmou) {
    return;
  }

  try {
    await api.excluirCategoria(id);
    categorias = categorias.filter(categoria => String(categoria.id) !== String(id));
    exibirCategorias();
    mostrarMensagem("Categoria excluída.", "sucesso");
  } catch (erro) {
    mostrarMensagem(erro.message);
  }
}

campoPesquisa.addEventListener("input", exibirCategorias);

listaCategorias.addEventListener("click", evento => {
  const botao = evento.target.closest("[data-excluir]");

  if (botao) {
    const categoria = categorias.find(item => String(item.id) === botao.dataset.excluir);

    if (categoria) {
      excluirCategoria(categoria.id, categoria.nome);
    }
  }
});

carregarCategorias();
