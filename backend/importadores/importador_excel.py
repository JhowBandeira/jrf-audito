# import significa "importe" ou "traga" uma biblioteca para dentro do nosso codigo.
#
# pandas e uma biblioteca pronta, criada por outros desenvolvedores.
# Ela possui diversas ferramentas para trabalhar com tabelas, arquivos Excel (.xlsx) e CSV (.csv).
#
# as pd cria um apelido para a biblioteca pandas.
# Isso significa que, em vez de escrever:
#
# pandas.read_excel()
#
# escreveremos apenas:
#
# pd.read_excel()
#
# pathlib ajuda a trabalhar com caminhos de arquivo de forma mais organizada,
# sem depender de uma pasta fixa dentro do codigo.

from pathlib import Path

import pandas as pd


EXTENSOES_EXCEL_SUPORTADAS = {".xlsx", ".xlsm", ".xltx", ".xltm"}


# pd significa pandas.
# read significa ler.
# read_excel significa ler Excel.
# header significa cabecalho.
# header=2 informa que o cabecalho esta na terceira linha do Excel.
# O Python comeca contando do zero:
# 0 = primeira linha
# 1 = segunda linha
# 2 = terceira linha
#
# A funcao abaixo recebe o caminho do arquivo como parametro.
# Assim o importador nao fica preso a uma planilha especifica.
# A funcao apenas le o arquivo e retorna a tabela.
# Quem chamar a funcao decide se quer imprimir, salvar, auditar ou normalizar.


def importar_excel(caminho_arquivo, header=0):
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo Excel nao encontrado: {caminho}")

    if not caminho.is_file():
        raise ValueError(f"O caminho informado nao e um arquivo: {caminho}")

    if caminho.suffix.lower() not in EXTENSOES_EXCEL_SUPORTADAS:
        extensoes = ", ".join(sorted(EXTENSOES_EXCEL_SUPORTADAS))
        raise ValueError(f"Extensao de Excel nao suportada. Use: {extensoes}")

    return pd.read_excel(caminho, header=header)
