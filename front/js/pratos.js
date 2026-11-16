const categoriaId = pegarParametro("categoriaId");
const listaPratos = document.querySelector("#lista-pratos");
const campoPesquisa = document.querySelector("#pesquisa");
const filtroDisponibilidade = document.querySelector("#filtro-disponibilidade");
let pratos = [];

exigirLogin();

function montarCartaoPrato(prato) {
  const nome = protegerTexto(prato.nome);
  const descricao = protegerTexto(prato.descricao || "Sem descrição.");
  const classeDisponibilidade = prato.disponivel ? "disponivel" : "indisponivel";
  const textoDisponibilidade = prato.disponivel ? "Disponível" : "Indisponível";

  return `
    <article class="cartao">
      <div class="cartao-conteudo">
        <h2>${nome}</h2>
        <p>${descricao}</p>
        <p class="preco">${formatarPreco(prato.preco)}</p>
        <span class="etiqueta ${classeDisponibilidade}">${textoDisponibilidade}</span>
      </div>
      <div class="acoes">
        <a class="botao botao-secundario" href="prato-form.html?categoriaId=${categoriaId}&id=${prato.id}">Editar</a>
        <button class="botao botao-perigo" type="button" data-excluir="${prato.id}">Excluir</button>
      </div>
    </article>
  `;
}

function exibirPratos() {
  const termo = campoPesquisa.value.trim().toLowerCase();
  const filtro = filtroDisponibilidade.value;

  const filtrados = pratos.filter(prato => {
    const combinaNome = prato.nome.toLowerCase().includes(termo);
    const combinaDisponibilidade = filtro === "todos"
      || (filtro === "disponiveis" && prato.disponivel)
      || (filtro === "indisponiveis" && !prato.disponivel);

    return combinaNome && combinaDisponibilidade;
  });

  if (filtrados.length === 0) {
    listaPratos.innerHTML = '<p class="estado-lista">Nenhum prato encontrado.</p>';
    return;
  }

  listaPratos.innerHTML = filtrados.map(montarCartaoPrato).join("");
}

async function carregarPagina() {
  if (!categoriaId) {
    mostrarMensagem("Escolha uma categoria antes de continuar.");
    listaPratos.innerHTML = "";
    return;
  }

  document.querySelector("#link-novo-prato").href = `prato-form.html?categoriaId=${categoriaId}`;

  try {
    const [categoria, lista] = await Promise.all([
      api.buscarCategoria(categoriaId),
      api.listarPratos(categoriaId)
    ]);

    document.querySelector("#titulo-categoria").textContent = `Pratos de ${categoria.nome}`;
    pratos = lista;
    exibirPratos();
  } catch (erro) {
    listaPratos.innerHTML = '<p class="estado-lista">Erro ao carregar os pratos.</p>';
    mostrarMensagem(erro.message);
  }
}

async function excluirPrato(id, nome) {
  const confirmou = window.confirm(`Excluir o prato "${nome}"?`);

  if (!confirmou) {
    return;
  }

  try {
    await api.excluirPrato(id);
    pratos = pratos.filter(prato => String(prato.id) !== String(id));
    exibirPratos();
    mostrarMensagem("Prato excluído.", "sucesso");
  } catch (erro) {
    mostrarMensagem(erro.message);
  }
}

campoPesquisa.addEventListener("input", exibirPratos);
filtroDisponibilidade.addEventListener("change", exibirPratos);

listaPratos.addEventListener("click", evento => {
  const botao = evento.target.closest("[data-excluir]");

  if (botao) {
    const prato = pratos.find(item => String(item.id) === botao.dataset.excluir);

    if (prato) {
      excluirPrato(prato.id, prato.nome);
    }
  }
});

carregarPagina();
