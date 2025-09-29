import pytest
from calc import operations as ops

@pytest.mark.parametrize(
    "func,a,b,expected",
    [
        (ops.add, 2, 3, 5),
        (ops.add, -1.5, 0.5, -1.0),
        (ops.sub, 10, 4, 6),
        (ops.mul, 3, 4, 12),
        (ops.mul, 2.5, 2, 5.0),
        (ops.div, 9, 3, 3),
        (ops.div, 7, 2, 3.5),
    ],
)
def test_basic_ops(func, a, b, expected):
    assert func(a, b) == expected

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        ops.div(1, 0)
