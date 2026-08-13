# Regra inicial para apuração de ICMS:
#
# 1. Verificar se o ICMS está destacado.
# 2. CFOP iniciado com 1, 2 ou 3 representa entrada.
# 3. CFOP iniciado com 5, 6 ou 7 representa saída.
# 4. CFOP 1933 e 2933 devem ser desconsiderados, pois são serviços tomados.
# 5. CFOP 5933 e 6933 devem ser desconsiderados, pois são serviços prestados.
# 6. Entradas geram crédito de ICMS.
# 7. Saídas geram débito de ICMS.
# 8. O saldo será calculado assim:
#
#    saldo = debitos - creditos
#
# 9. Se o saldo for positivo, existe ICMS a pagar.
# 10. Se o saldo for negativo, existe saldo credor.
# 11. Se o saldo for zero, não há ICMS a pagar nem saldo credor.

# 12. Devoluções de venda também devem abater o valor do ICMS a pagar,
# pois representam o retorno de uma operação de saída.
#
# Exemplo:
# Débitos de ICMS nas saídas:       10.000,00
# Devoluções de venda:              2.000,00
# Créditos de ICMS nas entradas:    5.000,00
#
# Saldo = Débitos - Devoluções - Créditos
# Saldo = 10.000 - 2.000 - 5.000
# Saldo = 3.000 a pagar

