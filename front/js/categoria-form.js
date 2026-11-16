const formulario = document.querySelector("#formulario-categoria");
const campoNome = document.querySelector("#nome");
const campoDescricao = document.querySelector("#descricao");
const botaoSalvar = document.querySelector("#botao-salvar");
const categoriaId = pegarParametro("id");

exigirLogin();

async function carregarCategoria() {
  if (!categoriaId) {
    return;
  }

  document.querySelector("#titulo-pagina").textContent = "Editar categoria";
  botaoSalvar.textContent = "Salvar alterações";

  try {
    const categoria = await api.buscarCategoria(categoriaId);
    campoNome.value = categoria.nome;
    campoDescricao.value = categoria.descricao || "";
  } catch (erro) {
    mostrarMensagem(erro.message);
    formulario.hidden = true;
  }
}

formulario.addEventListener("submit", async evento => {
  evento.preventDefault();
  esconderMensagem();

  const nome = campoNome.value.trim();
  const descricao = campoDescricao.value.trim();

  if (!nome) {
    mostrarMensagem("Informe o nome da categoria.");
    campoNome.focus();
    return;
  }

  definirBotaoCarregando(botaoSalvar, true);

  try {
    const dados = { nome, descricao: descricao || null };

    if (categoriaId) {
      await api.atualizarCategoria(categoriaId, dados);
    } else {
      await api.criarCategoria(dados);
    }

    window.location.href = "gerenciamento.html";
  } catch (erro) {
    mostrarMensagem(erro.message);
    definirBotaoCarregando(botaoSalvar, false);
  }
});

carregarCategoria();
