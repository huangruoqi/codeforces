import sys
from codeforces import functions

if __name__ == "__main__":
    funcs = {k[2:]: v for k, v in functions.__dict__.items() if k[:2] == "f_"}
    name = sys.argv[1]
    args = sys.argv[2:]
    func = funcs.get(name)
    if func is not None:
        func(*args)
