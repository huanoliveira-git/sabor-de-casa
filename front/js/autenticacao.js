const CHAVE_TOKEN = "sabor_de_casa_token";

function salvarToken(token) {
  localStorage.setItem(CHAVE_TOKEN, token);
}

function pegarToken() {
  return localStorage.getItem(CHAVE_TOKEN);
}

function removerToken() {
  localStorage.removeItem(CHAVE_TOKEN);
}

function exigirLogin() {
  if (window.CONFIGURACAO.MODO_VISUALIZACAO) {
    return true;
  }

  if (!pegarToken()) {
    window.location.href = "login.html";
    return false;
  }

  return true;
}

document.addEventListener("click", evento => {
  const botaoSair = evento.target.closest("[data-sair]");

  if (botaoSair) {
    removerToken();
    window.location.href = "index.html";
  }
});
