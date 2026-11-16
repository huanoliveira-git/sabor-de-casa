const cardapio = document.querySelector("#cardapio");

function montarPratoPublico(prato) {
  return `
    <article class="prato-publico">
      <div>
        <h3>${protegerTexto(prato.nome)}</h3>
        <p>${protegerTexto(prato.descricao || "Prato disponível no cardápio.")}</p>
      </div>
      <strong class="preco">${formatarPreco(prato.preco)}</strong>
    </article>
  `;
}

function montarCategoriaPublica(categoria, pratos) {
  const disponiveis = pratos.filter(prato => prato.disponivel);
  const conteudo = disponiveis.length
    ? disponiveis.map(montarPratoPublico).join("")
    : '<p class="estado-lista">Nenhum prato disponível nesta categoria.</p>';

  return `
    <section class="categoria-publica">
      <div class="categoria-publica-titulo">
        <div>
          <h2>${protegerTexto(categoria.nome)}</h2>
          <p>${protegerTexto(categoria.descricao || "Veja as opções desta categoria.")}</p>
        </div>
      </div>
      <div class="grade-pratos">${conteudo}</div>
    </section>
  `;
}

async function carregarCardapio() {
  esconderMensagem();

  try {
    const categorias = await api.listarCategorias();

    if (categorias.length === 0) {
      cardapio.innerHTML = '<p class="estado-lista painel">O cardápio ainda não possui categorias.</p>';
      return;
    }

    const pratosPorCategoria = await Promise.all(
      categorias.map(categoria => api.listarPratos(categoria.id))
    );

    cardapio.innerHTML = categorias
      .map((categoria, indice) => montarCategoriaPublica(categoria, pratosPorCategoria[indice]))
      .join("");
  } catch (erro) {
    cardapio.innerHTML = '<p class="estado-lista painel">Não foi possível carregar o cardápio.</p>';
    mostrarMensagem(erro.message);
  }
}

carregarCardapio();
