from decimal import Decimal, InvalidOperation

PRECO_MAXIMO = Decimal("99999999.99")
DUAS_CASAS = Decimal("0.01")


def validar_texto_obrigatorio(valor: object, campo: str, limite: int) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"O campo {campo} é obrigatório.")
    texto = valor.strip()
    _validar_tamanho(texto, campo, limite)
    return texto


def validar_texto_opcional(valor: object, campo: str, limite: int) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise ValueError(f"O campo {campo} deve ser um texto.")
    texto = valor.strip()
    if not texto:
        return None
    _validar_tamanho(texto, campo, limite)
    return texto


def validar_preco(valor: object) -> Decimal:
    preco = _converter_para_decimal(valor)
    if preco <= 0:
        raise ValueError("O preço deve ser maior que zero.")
    if preco.as_tuple().exponent < -2:
        raise ValueError("O preço deve ter no máximo duas casas decimais.")
    if preco > PRECO_MAXIMO:
        raise ValueError("O preço informado é alto demais.")
    return preco.quantize(DUAS_CASAS)


def _validar_tamanho(texto: str, campo: str, limite: int) -> None:
    if len(texto) > limite:
        raise ValueError(f"O campo {campo} deve ter no máximo {limite} caracteres.")


def _converter_para_decimal(valor: object) -> Decimal:
    if valor is None or isinstance(valor, bool) or str(valor).strip() == "":
        raise ValueError("O campo preço é obrigatório.")
    try:
        preco = Decimal(str(valor).strip().replace(",", "."))
    except InvalidOperation:
        raise ValueError("O preço deve ser um número válido.") from None
    if not preco.is_finite():
        raise ValueError("O preço deve ser um número válido.")
    return preco
