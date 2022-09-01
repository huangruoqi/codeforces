from codeforces.shortcuts import gcd


def test_gcd():
    assert gcd(10, 24) == 2
    assert gcd(100, 250) == 50
    assert gcd(21, 28) == 7
