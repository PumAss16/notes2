import pytest
from app import add, divide

# Тесты для сложения
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(0, 0) == 0

# Тесты для ния
def test_divide_success():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    # Проверяем, что при делении на ноль выбрасывается исключение
    with pytest.raises(ValueError, match="На ноль делить нельзя!"):
        divide(10, 0)