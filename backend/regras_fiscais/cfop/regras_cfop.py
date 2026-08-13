# ============================================================
# FUNÃ‡Ã•ES
# ============================================================

# def significa "define" (definir).
# Ela Ã© utilizada para criar uma funÃ§Ã£o.

# Exemplo:
#
# def calcular_icms():
#
# Pense em uma calculadora.
# Ela possui vÃ¡rios botÃµes:
#
# +
# -
# Ã—
# Ã·
#
# Cada botÃ£o faz apenas uma tarefa.
#
# Uma funÃ§Ã£o funciona da mesma forma.
# Ela Ã© um bloco de cÃ³digo criado para executar uma tarefa especÃ­fica.


# ============================================================
# RETURN
# ============================================================

# return significa:
#
# retornar
# ou
# devolver
#
# Ele devolve o resultado da funÃ§Ã£o.

# Exemplo:
#
# def nome():
#     return "Jhonatan"
#
# TraduÃ§Ã£o:
#
# Crie uma funÃ§Ã£o chamada nome().
# Depois devolva a informaÃ§Ã£o "Jhonatan".


# ============================================================
# IN
# ============================================================

# in significa:
#
# em
# dentro de
# estÃ¡ dentro de
#
# Ele verifica se um valor pertence a uma lista,
# uma tupla ou outra coleÃ§Ã£o.

# Exemplo:
#
# if cfop in lista:
#
# TraduÃ§Ã£o:
#
# O CFOP estÃ¡ dentro da lista?

# Imagine uma caixa contendo:

# 1933
# 2933
# 5933
# 6933

# Pergunta:
#
# 1933 estÃ¡ dentro dessa caixa?
#
# Se sim:
#
# True
#
# Se nÃ£o:
#
# False


# ============================================================
# STR
# ============================================================

# str significa String.
#
# String Ã© um texto.

# Exemplo:

# 5102

# Ã€s vezes o Excel lÃª esse valor como nÃºmero.
# Outras vezes lÃª como texto.

# Para evitar problemas fazemos:

# str(cfop)

# TraduÃ§Ã£o:
#
# Transforme esse valor em texto.


# ============================================================
# STRIP
# ============================================================

# strip() significa remover espaÃ§os.

# Exemplo:

# "   5102   "

# Depois do strip():

# "5102"

# Ele remove espaÃ§os do comeÃ§o e do final do texto.


# ============================================================
# STARTSWITH
# ============================================================

# starts = comeÃ§a
# with = com
#
# startswith = comeÃ§a com

# Exemplo:

# cfop.startswith(("1","2","3"))

# TraduÃ§Ã£o:

# O CFOP comeÃ§a com:
#
# 1
# 2
# ou
# 3 ?

# Se sim:

# True

# Caso contrÃ¡rio:

# False


# ============================================================
# FUNÃ‡ÃƒO CFOP DE ENTRADA
# ============================================================

# def
# Crie uma funÃ§Ã£o chamada:
#
# "CFOP Ã© entrada?"

# cfop
# Receba um CFOP.

# str
# Transforme em texto.

# strip
# Remova espaÃ§os.

# return
# Devolva:

# True

# se comeÃ§ar com:

# 1
# 2
# 3

# Caso contrÃ¡rio:

# False.


def cfop_eh_entrada(cfop):
    cfop = str(cfop).strip()
    return cfop.startswith(("1", "2", "3"))


# ============================================================
# FUNÃ‡ÃƒO CFOP DE SAÃDA
# ============================================================

# Funciona exatamente como a anterior.

# A diferenÃ§a Ã© que agora verificamos se o CFOP
# comeÃ§a com:

# 5
# 6
# 7

# Se comeÃ§ar:

# True

# Caso contrÃ¡rio:

# False.


def cfop_eh_saida(cfop):
    cfop = str(cfop).strip()
    return cfop.startswith(("5", "6", "7"))


# ============================================================
# FUNÃ‡ÃƒO CFOP DE SERVIÃ‡O
# ============================================================

# Aqui nÃ£o usamos startswith().

# Por quÃª?

# Porque nÃ£o queremos saber se o CFOP
# comeÃ§a com um nÃºmero.

# Queremos saber se ele Ã© exatamente:

# 1933
# 2933
# 5933
# 6933

# Para isso utilizamos:

# in

# TraduÃ§Ã£o:

# O CFOP estÃ¡ dentro desta lista?

# Se estiver:

# True

# Caso contrÃ¡rio:

# False.


def cfop_eh_servico(cfop):
    cfop = str(cfop).strip()
    return cfop in ("1933", "2933", "5933", "6933")


# ============================================================
# TESTES
# ============================================================

# Testando CFOP de entrada


# Testando CFOP de saÃ­da


# Testando CFOP de serviÃ§o






