from http import HTTPStatus


class ErroAplicacao(Exception):
    status_http = HTTPStatus.BAD_REQUEST

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class RecursoNaoEncontrado(ErroAplicacao):
    status_http = HTTPStatus.NOT_FOUND


class ConflitoDeDados(ErroAplicacao):
    status_http = HTTPStatus.CONFLICT


class NaoAutenticado(ErroAplicacao):
    status_http = HTTPStatus.UNAUTHORIZED
