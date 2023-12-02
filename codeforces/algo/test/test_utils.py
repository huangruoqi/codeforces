from ..utils import gcd


def test_gcd():
    assert gcd(120, 56) == 8
    assert gcd(256, 96) == 32
