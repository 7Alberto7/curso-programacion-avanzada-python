import pytest
from calculadora import dividir


def test_division_por_cero():
    with pytest.raises(ZeroDivisionError):
        dividir(10, 0)