const formulario = document.querySelector("#formulario-prato");
const campoNome = document.querySelector("#nome");
const campoDescricao = document.querySelector("#descricao");
const campoPreco = document.querySelector("#preco");
const campoDisponivel = document.querySelector("#disponivel");
const botaoSalvar = document.querySelector("#botao-salvar");
const categoriaId = pegarParametro("categoriaId");
const pratoId = pegarParametro("id");

exigirLogin();

function configurarLinks() {
  const destino = categoriaId ? `pratos.html?categoriaId=${categoriaId}` : "gerenciamento.html";
  document.querySelector("#link-voltar").href = destino;
  document.querySelector("#link-cancelar").href = destino;
}

async function carregarPrato() {
  if (!categoriaId) {
    mostrarMensagem("Escolha uma categoria antes de continuar.");
    formulario.hidden = true;
    return;
  }

  if (!pratoId) {
    return;
  }

  document.querySelector("#titulo-pagina").textContent = "Editar prato";
  botaoSalvar.textContent = "Salvar alterações";

  try {
    const prato = await api.buscarPrato(pratoId);
    campoNome.value = prato.nome;
    campoDescricao.value = prato.descricao || "";
    campoPreco.value = String(prato.preco).replace(".", ",");
    campoDisponivel.checked = prato.disponivel;
  } catch (erro) {
    mostrarMensagem(erro.message);
    formulario.hidden = true;
  }
}

function precoValido(preco) {
  const formatoValido = /^\d+([,.]\d{1,2})?$/.test(preco);
  const valorNumerico = Number(preco.replace(",", "."));
  return formatoValido && valorNumerico > 0;
}

formulario.addEventListener("submit", async evento => {
  evento.preventDefault();
  esconderMensagem();

  const nome = campoNome.value.trim();
  const descricao = campoDescricao.value.trim();
  const preco = campoPreco.value.trim();

  if (!nome) {
    mostrarMensagem("Informe o nome do prato.");
    campoNome.focus();
    return;
  }

  if (!precoValido(preco)) {
    mostrarMensagem("O preço deve ser maior que zero e ter no máximo duas casas decimais.");
    campoPreco.focus();
    return;
  }

  definirBotaoCarregando(botaoSalvar, true);

  const dados = {
    nome,
    descricao: descricao || null,
    preco,
    disponivel: campoDisponivel.checked
  };

  try {
    if (pratoId) {
      await api.atualizarPrato(pratoId, { ...dados, categoria_id: Number(categoriaId) });
    } else {
      await api.criarPrato(categoriaId, dados);
    }

    window.location.href = `pratos.html?categoriaId=${categoriaId}`;
  } catch (erro) {
    mostrarMensagem(erro.message);
    definirBotaoCarregando(botaoSalvar, false);
  }
});

configurarLinks();
carregarPrato();
