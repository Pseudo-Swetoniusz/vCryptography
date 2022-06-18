from vc import *
from random import randint, shuffle

def test_permute(n,m,vc: VC):
    permutation = [i for i in range(m)]
    shuffle(permutation)
    S = [[randint(1,100) for j in range(m)] for i in range(n)]
    newS = vc.permute(S, permutation)
    print(f"S = {S}\np = {permutation}\n=> {newS}")

vc = VC(3,3)
test_permute(3,3,vc)