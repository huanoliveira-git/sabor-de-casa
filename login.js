const formularioLogin = document.querySelector("#formulario-login");
const campoUsuario = document.querySelector("#usuario");
const campoSenha = document.querySelector("#senha");
const botaoEntrar = document.querySelector("#botao-entrar");

if (pegarToken()) {
  window.location.href = "gerenciamento.html";
}

formularioLogin.addEventListener("submit", async evento => {
  evento.preventDefault();
  esconderMensagem();

  const usuario = campoUsuario.value.trim();
  const senha = campoSenha.value;

  if (!usuario || !senha) {
    mostrarMensagem("Informe o usuário e a senha.");
    return;
  }

  definirBotaoCarregando(botaoEntrar, true);

  try {
    const resposta = await api.entrar(usuario, senha);
    salvarToken(resposta.access_token);
    window.location.href = "gerenciamento.html";
  } catch (erro) {
    mostrarMensagem(erro.message);
    definirBotaoCarregando(botaoEntrar, false);
  }
});
