
from sys import path
from typing import List
from numpy import uint8
path.append(".")
from utils.BinaryData import *
from utils.Image import *
from math import factorial
from random import SystemRandom
from itertools import combinations, permutations
from copy import deepcopy


class VC():
    TYPE  = uint8

    DARK = tuple(map(TYPE, ['0','0','0']))
    LIGHT = tuple(map(TYPE, ['255','255','255']))

    BLACK = list(map(TYPE, ['0','0','0']))
    WHITE = list(map(TYPE, ['255','255','255']))
    RED = list(map(TYPE, ['255','0','0']))
    GREEN = list(map(TYPE, ['0','255','0']))
    BLUE = list(map(TYPE, ['0','0','255']))
    CYAN = list(map(TYPE, ['0','255','255']))
    MAGENTA = list(map(TYPE, ['255','0','255']))
    YELLOW = list(map(TYPE, ['255','255','0']))

    translation = {
        (LIGHT, LIGHT, LIGHT): WHITE, 
        (DARK, LIGHT, LIGHT): YELLOW,
        (LIGHT, DARK, LIGHT): MAGENTA, 
        (LIGHT, LIGHT, DARK): CYAN, 
        (LIGHT, DARK, DARK): RED, 
        (DARK, LIGHT, DARK): GREEN, 
        (DARK, DARK, LIGHT): BLUE, 
        (DARK, DARK, DARK): BLACK
    }

    def __init__(self,n: int, k: int):
        self.n = n #liczba podobrazów
        self.k = k # liczba podobrazów koniecznych do odkrycia sekretu
        self.image: CImage
        self.resImages: List[CImage]
        self.m = 2**(self.k-1)
        self.r = factorial(2**(self.k-1))
        self.C0, self.C1 = [],[]
        self.S0, self.S1 = [],[]
        self.getCMatrices()
        self.m0 = self.m
        self.m1 = 1

    def __call__(self, img: CImage):
        self.setImage(img)
        img = CImage()
        img.width, img.height = self.image.get_width()*self.m0, self.image.get_height()*self.m1
        img.image_matrix = np.asarray([[self.DARK for j in range(img.width)] for i in range(img.height)])
        self.resImages = [deepcopy(img) for i in range(self.n)]
        return self.encrypt()
    
    def factors(self,n):
        i = int(n**0.5)
        while(n%i!=0):
            i-=1
        return i, n//i
    
    def max_min(self,m,n):
        m = m+n
        n = m-n
        m = m-n
        return m,n
    
    def add_colour(self, p1, p2):
        x,y,z = ((int(p1[0])*int(p2[0]))//255), ((int(p1[1])*int(p2[1]))//255), ((int(p1[2])*int(p2[2]))//255)
        return [uint8(x),uint8(y), uint8(z)]

    def setImage(self, img: CImage):
        self.image = img
    
    def permute(self, S, permutation):
        resS = deepcopy(S)
        for i in range(len(S)):
            for j in range(len(S[i])):
                resS[i][j] = S[i][permutation[j]]
        return resS

    def getSizeMulti3(self):
        return (3-(self.m%3))%3

    def getTriple(self, array, i, j, l):
        first = array[i][j][l]
        second = self.DARK
        third = self.DARK
        if((l+1)<self.m):
            second = array[i][j][l+1]
        if((l+2)<self.m):
            third = array[i][j][l+2]
        key = (first, second, third)
        return(self.translation[key])

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
        S0, S1 = [[self.LIGHT for j in range(self.m)] for i in range(self.k)],[[self.LIGHT for j in range(self.m)] for i in range(self.k)]
        for i in range(self.k):
            for j in range(self.m):
                if(e[i] in even[j]):
                    S0[i][j] = self.DARK
                if(e[i] in odd[j]):
                    S1[i][j] = self.DARK
        perms = permutations([i for i in range(self.m)])
        for permutation in perms:
            self.C0.append(self.permute(S0, permutation))
            self.C1.append(self.permute(S1, permutation))
        #extending
        colourC0 = [[[] for j in range(self.k)] for i in range(len(self.C0))]
        colourC1 = [[[] for j in range(self.k)] for i in range(len(self.C1))]
        extension = self.getSizeMulti3()
        for i in range(len(self.C0)):
            for j in range(self.k):
                for l in range(0,self.m+extension,3):
                    colour = self.getTriple(self.C0,i,j,l)
                    colourC0[i][j].append(colour)
                    colour = self.getTriple(self.C1,i,j,l)
                    colourC1[i][j].append(colour)
        self.C0 = colourC0
        self.C1 = colourC1
        self.m = len(self.C0[0][0])
        self.m0, self.m1 = self.factors(self.m)
        print(self.m0,self.m1)

    def getRandomShares(self, i, j):
        rand = SystemRandom()
        tmp = rand.randint(0,self.r-1)
        if(self.isBlack(self.image[i,j])):
            return self.C1[tmp]
        return self.C0[tmp]

    def isBlack(self, pixel):
        return pixel[0]==0 and pixel[1]==0 and pixel[2]==0

    def buildShares(self, i: int, j: int):
        newI, newJ = i*self.m1,j*self.m0
        shares = self.getRandomShares(i, j)
        for num in range(len(self.resImages)):
            current = self.resImages[num]
            for idxI in range(self.m1):
                for idxJ in range(self.m0):
                    current.image_matrix[newI+idxI][newJ+idxJ] = shares[num][(idxI+1)*idxJ]

    def encrypt(self):
        for i in range(self.image.height):
            for j in range(self.image.width):
                self.buildShares(i,j)
        for image in self.resImages:
            image.update_image()
        return self.resImages

    def combine(self, img1: CImage, img2: CImage):
        assert img1.height == img2.height and img1.width == img2.width
        res = deepcopy(img1)
        for i in range(img1.height):
            for j in range(img1.width):
                res.image_matrix[i][j] = self.add_colour(img1[i,j],img2[i,j])
        return res

    def combineShares(self):
        res = self.resImages[0]
        for i in range(1,len(self.resImages)):
            res = self.combine(res, self.resImages[i])
        res.update_image()
        return res

