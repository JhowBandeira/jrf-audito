"""Utilitarios simples para Unidade Federativa brasileira."""

UFS_BRASILEIRAS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
}


def normalizar_uf(uf: str | None) -> str | None:
    """Normaliza UF para maiusculo e valida siglas brasileiras."""
    if uf is None:
        return None
    valor = str(uf).strip().upper()
    if not valor:
        return None
    if valor not in UFS_BRASILEIRAS:
        raise ValueError("UF deve ser uma sigla brasileira valida.")
    return valor
