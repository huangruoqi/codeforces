def ii():
    i = input().split()
    try:
        if len(i) == 1:
            return int(i[0])
        return list(map(int, i))
    except Exception:
        if len(i) == 1:
            return i[0]
        return i


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)
