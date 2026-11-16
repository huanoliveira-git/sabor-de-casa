function pegarParametro(nome) {
  return new URLSearchParams(window.location.search).get(nome);
}

function mostrarMensagem(texto, tipo = "erro") {
  const elemento = document.querySelector("#mensagem");
  elemento.textContent = texto;
  elemento.className = `mensagem visivel mensagem-${tipo}`;
  elemento.scrollIntoView({ behavior: "smooth", block: "center" });
}

function esconderMensagem() {
  const elemento = document.querySelector("#mensagem");
  elemento.textContent = "";
  elemento.className = "mensagem";
}

function protegerTexto(texto = "") {
  const elemento = document.createElement("div");
  elemento.textContent = texto;
  return elemento.innerHTML;
}

function formatarPreco(valor) {
  const numero = Number(String(valor).replace(",", "."));

  return numero.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL"
  });
}

function definirBotaoCarregando(botao, carregando) {
  if (carregando) {
    botao.dataset.textoOriginal = botao.textContent;
    botao.textContent = "Aguarde...";
    botao.disabled = true;
    return;
  }

  botao.textContent = botao.dataset.textoOriginal || "Salvar";
  botao.disabled = false;
}
