"""
    Name    | {name}
    Contest | {contest}
    Problem | {problem}
    Time    | {time}
    URL     | {url}
"""


def ii():
    s = tuple(map(int, input().split()))
    return s[0] if len(s) == 1 else s


for _ in range(ii()):
    pass
