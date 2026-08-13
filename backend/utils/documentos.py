"""Utilitarios compartilhados para CPF e CNPJ."""


TIPOS_PESSOA = {"PF", "PJ"}


def normalizar_documento(documento: str) -> str:
    """Remove caracteres nao numericos de CPF/CNPJ."""
    return "".join(caractere for caractere in str(documento) if caractere.isdigit())


def normalizar_tipo_pessoa(tipo_pessoa: str) -> str:
    """Padroniza tipo de pessoa como PF ou PJ."""
    valor = str(tipo_pessoa).strip().upper()
    if valor not in TIPOS_PESSOA:
        raise ValueError("Tipo de pessoa deve ser PF ou PJ.")
    return valor


def validar_documento_estrutural(tipo_pessoa: str, documento: str) -> str:
    """Valida apenas a estrutura basica de CPF/CNPJ, sem digitos verificadores."""
    tipo_normalizado = normalizar_tipo_pessoa(tipo_pessoa)
    documento_normalizado = normalizar_documento(documento)

    if not documento_normalizado:
        raise ValueError("CPF/CNPJ e obrigatorio.")

    if tipo_normalizado == "PF" and len(documento_normalizado) != 11:
        raise ValueError("CPF deve conter 11 digitos.")

    if tipo_normalizado == "PJ" and len(documento_normalizado) != 14:
        raise ValueError("CNPJ deve conter 14 digitos.")

    return documento_normalizado
