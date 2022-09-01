from codeforces.shortcuts import ii
import os


def test_list_input():
    assert execute_test("1 2 3") == str([1, 2, 3])
    assert execute_test("ab cd ef") == str(["ab", "cd", "ef"])
    assert execute_test("1") == str(1)


p = "codeforces/test/{}.txt"


def execute_test(test_input):
    inf = open(p.format("in"), "w")
    inf.write(test_input)
    inf.close()
    cmd = f'python codeforces/test/test_ii.py < {p.format("in")}'
    os.system(cmd)
    os.remove(p.format("in"))
    outf = open(p.format("out"))
    output = outf.read()
    outf.close()
    os.remove(p.format("out"))
    return output


if __name__ == "__main__":
    p = "codeforces/test/out.txt"
    outf = open(p.format("out"), "w")
    print(os.getcwd())
    outf.write(str(ii()))
    outf.close()
