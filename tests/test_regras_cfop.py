import unittest

from backend.regras_fiscais.cfop.regras_cfop import (
    cfop_eh_entrada,
    cfop_eh_saida,
    cfop_eh_servico,
)


class TestRegrasCfop(unittest.TestCase):
    def test_cfop_eh_entrada(self):
        self.assertIs(cfop_eh_entrada("1102"), True)
        self.assertIs(cfop_eh_entrada("5102"), False)

    def test_cfop_eh_saida(self):
        self.assertIs(cfop_eh_saida("5102"), True)
        self.assertIs(cfop_eh_saida("1102"), False)

    def test_cfop_eh_servico(self):
        self.assertIs(cfop_eh_servico("5102"), False)
        self.assertIs(cfop_eh_servico("1102"), False)
        self.assertIs(cfop_eh_servico("1933"), True)
        self.assertIs(cfop_eh_servico("5933"), True)


if __name__ == "__main__":
    unittest.main()
