import sys
from codeforces import functions
print(functions.__dict__)

if __name__=='__main__':
    funcs = {}
    name = sys.argv[1]
    args = sys.argv[2:]
    func = funcs.get(name, *args)
    if func is not None: func()