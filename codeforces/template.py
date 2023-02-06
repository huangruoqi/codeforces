"""
    Name    | Ruoqi Huang
    Contest | {contest}
    Problem | {problem}
    Time    | {time}
"""
def ii(num=False):
    i = input().split()
    if num:
        return int(i[0])
    try:
        return list(map(int, i))
    except Exception:
        return i


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)

for _ in range(ii(1)):
    pass
