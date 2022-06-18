from sys import path
from typing import List
path.append(".")
from utils.BinaryData import *
from utils.Image import *
from math import factorial
from random import SystemRandom
from itertools import combinations, permutations
from copy import deepcopy

class VC():
    def __init__(self,n: int, k: int):
        self.n = n #liczba podobrazów
        self.k = k # liczba podobrazów koniecznych do odkrycia sekretu
        self.image: CImage
        self.resImages: List[CImage]
        self.m = 2**(self.k-1)
        self.r = factorial(2**(self.k-1))
        self.C0, self.C1 = [],[]
        # self.getCMatrices()
        self.m0,self.m1 = self.m,1

    def __call__(self, img: CImage):
        self.setImage(img)
        self.resImages = [CImage(self.image.get_width()*self.m0, self.image.get_height()*self.m1)]
        return self.encrypt()

    def setImage(self, img: CImage):
        self.image = img
    
    def permute(self, S, permutation):
        resS = deepcopy(S)
        for i in range(len(S)):
            for j in range(len(S[i])):
                resS[i][j] = S[i][permutation[j]]
        return resS

    def getCMatrices(self):
        e = {i for i in range(self.k)}
        comb = []
        for i in range(1,len(e)+1):
            for j in combinations(e,i):
                comb.append(j)
        even, odd = [], []
        for c in comb:
            if(len(c)%2==0):
                even.append(c)
            else:
                odd.append(c)
        e = [i for i in range(self.k)]
        S0, S1 = [[0 for j in range(self.m)] for i in range(self.k)],[[0 for j in range(self.m)] for i in range(self.k)]
        for i in range(self.k):
            for j in range(self.m):
                if(e[i] in even[j]):
                    S0[i][j] = 1
                if(e[i] in odd[j]):
                    S1[i][j] = 1
        perms = permutations([i for i in range(self.m)])
        for permutation in perms:
            self.C0.append(self.permute(S0, permutation))
            self.C1.append(self.permute(S1, permutation))

    def getRandomShares(self, i, j):
        tmp = SystemRandom.randint(0,self.r-1)
        if(self.isBlack(self.image[i,j])):
            return self.C1[tmp]
        return self.C0[tmp]

    def isBlack(self, pixel):
        return pixel[0]==0 and pixel[1]==0 and pixel[2]==0

    def buildShares(self, i: int, j: int):
        newI, newJ = i*self.m0,j*self.m1
        shares = self.getRandomShares(i, j)
        for num in range(len(self.resImages)):
            current = self.resImages[num]
            assert len(current[newI:(newI+self.m1)][newJ:(newJ+self.m0)]) == len(shares[num])
            current[newI:(newI+self.m1)][newJ:(newJ+self.m0)] = shares[num]

    def encrypt(self):
        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                self.buildShares(i,j)

        for img in self.resImages:
            img.show_image()

    def combine(self, img1: CImage, img2: CImage):
        #IMPLEMENT
        return img1

# vc = VC(2,2)
# array = [[1,0,1],[0,1,0],[1,1,0]]
# img = CImage()
# img.show_image()