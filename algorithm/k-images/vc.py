from sys import path
from typing import List
path.append(".")
from utils.BinaryData import *
from utils.Image import *
from math import factorial
from random import SystemRandom
from itertools import combinations, permutations
from copy import deepcopy

# m0,m1?

class VC():
    def __init__(self,n: int, k: int):
        self.n = n #liczba podobrazów
        self.k = k # liczba podobrazów koniecznych do odkrycia sekretu
        self.image: CImage
        self.resImages: List[CImage]
        self.m = 2**(self.k-1)
        self.r = factorial(2**(self.k-1))
        self.C0, self.C1 = [],[]
        self.getCMatrices()
        self.m0,self.m1 = self.m,1

    def __call__(self, img: CImage):
        self.setImage(img)
        img = CImage()
        img.width, img.height = self.image.get_width()*self.m0, self.image.get_height()*self.m1
        img.image_matrix = [[(0,0,0) for j in range(img.width)] for i in range(img.height)]
        self.resImages = [deepcopy(img) for i in range(self.n)]
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
        for i in range(0,len(e)+1):
            for j in combinations(e,i):
                comb.append(j)
        even, odd = [], []
        for c in comb:
            if(len(c)%2==0):
                even.append(c)
            else:
                odd.append(c)
        e = [i for i in range(self.k)]
        S0, S1 = [[(1,1,1) for j in range(self.m)] for i in range(self.k)],[[(1,1,1) for j in range(self.m)] for i in range(self.k)]
        for i in range(self.k):
            for j in range(self.m):
                if(e[i] in even[j]):
                    S0[i][j] = (0,0,0)
                if(e[i] in odd[j]):
                    S1[i][j] = (0,0,0)
        perms = permutations([i for i in range(self.m)])
        for permutation in perms:
            self.C0.append(self.permute(S0, permutation))
            self.C1.append(self.permute(S1, permutation))
        # print(f"C0 = \n{self.C0}\nC1 = \n{self.C1}")
        # print("----------")

    def getRandomShares(self, i, j):
        # print(img.image_matrix)
        rand = SystemRandom()
        tmp = rand.randint(0,self.r-1)
        if(self.isBlack(self.image[i,j])):
            return self.C1[tmp]
        return self.C0[tmp]

    def isBlack(self, pixel):
        return pixel[0]==0 and pixel[1]==0 and pixel[2]==0

    def buildShares(self, i: int, j: int):
        #maybe m0 m1?
        newI, newJ = i,j*self.m
        shares = self.getRandomShares(i, j)
        for num in range(len(self.resImages)):
            current = self.resImages[num]
            for idx in range(self.m):
                current.image_matrix[newI][newJ+idx] = shares[num][idx]

    def encrypt(self):
        for i in range(self.image.height):
            for j in range(self.image.width):
                self.buildShares(i,j)
        return self.resImages

    def combine(self, img1: CImage, img2: CImage):
        assert img1.height == img2.height and img1.width == img2.width
        res = deepcopy(img1)
        for i in range(img1.height):
            for j in range(img1.width):
                if(img1[i,j] == (0,0,0) or img2[i,j] == (0,0,0)):
                    res.image_matrix[i][j] = (0,0,0)
                else:
                    res.image_matrix[i][j] = (1,1,1)
        return res

    def combineShares(self):
        res = self.resImages[0]
        for i in range(1,len(self.resImages)):
            res = self.combine(res, self.resImages[i])
        return res


vc = VC(3,3)
array = [   [(0,0,0),(1,1,1),(1,1,1)],
            [(0,0,0),(0,0,0),(0,0,0)],
            [(1,1,1),(0,0,0),(1,1,1)] ]
img = CImage()
img.update_matrix(array)
img.width, img.height = 3,3
# print(img.image_matrix)
shares = vc(img)
print("shares:")
shares = [share.image_matrix for share in shares]
# print(shares[0])
# img.show_image()
decryptedImg = vc.combineShares()
print(decryptedImg.image_matrix)