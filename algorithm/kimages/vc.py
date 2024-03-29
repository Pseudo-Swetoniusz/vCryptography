
from typing import List
from numpy import uint8,uint16
from utils.BinaryData import *
from utils.Image import *
from math import factorial
from random import SystemRandom
from itertools import combinations, permutations
from copy import deepcopy
from math import log, ceil

from scipy.special import comb
from sympy.utilities.iterables import multiset_permutations


class VC():
    TYPE = uint8  
    TYPE2 = uint16

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
        (DARK, DARK, LIGHT): BLUE, 
        (DARK, LIGHT, DARK): GREEN, 
        (LIGHT, DARK, DARK): RED, 
        (DARK, DARK, DARK): BLACK
    }

    def __init__(self,k: int, n: int, mode: int = 3):
        self.n = n #liczba podobrazów
        self.k = k # liczba podobrazów koniecznych do odkrycia sekretu
        self.image: CImage
        self.resImages: List[CImage]
        self.m = 2**(self.k-1)
        self.r = factorial(2**(self.k-1))
        self.l = ceil(log(n,k))+2
        self.hashes = []
        self.C0, self.C1 = [],[]
        self.S0, self.S1 = [],[]
        self.m0 = self.m
        self.m1 = 1
        self.getCMatrices(mode)

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
    
    def addColour(self, p1, p2):
        a = list(map(self.TYPE2,p1))
        b = list(map(self.TYPE2,p2))
        x,y,z = ((a[0]*b[0])//255), ((a[1]*b[1])//255), ((a[2]*b[2])//255)
        return [self.TYPE(x),self.TYPE(y), self.TYPE(z)]

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

    def getVector(self):
        t = tuple(1 for i in range(self.l))
        return t
    
    def incrementVector(self,t):
        newT = [t[i] for i in range(self.l)]
        for i in range(self.l):
            if(newT[i]+1<=self.r):
                newT[i] = newT[i]+1
                break
            else:
                newT[i] = 1
        return tuple(newT[i] for i in range(self.l))

    def constructHashes(self):
        for i in range(self.l):
            p = 331
            rand = SystemRandom()
            coeffs = [rand.randint(0,p) for i in range(self.k)]
            self.hashes.append(coeffs)
    
    def getHashFunction(self):
        rand = SystemRandom()
        h = rand.randint(0,self.l-1)
        return h

    def solve(self, h, x):
        coeffs = self.hashes[h]
        res = 0
        for coeff in coeffs:
            res = res * x + coeff % self.k
        return res%self.k

    def newton(self,n,k):
        return int(comb(n,k))
    
    def getUVectors(self):
        u0,u1 = [0]*(self.n+1),[0]*(self.n+1)
        if(self.k%2==0): # k even
            l = (self.k-2)//2
            for i in range(l+1):
                u0[self.n-2*i] = self.newton(self.n-2*i-1,self.k-2*i-1)
                u1[self.n-2*i-1] = self.newton(self.n-2*i-2,self.k-2*i-2)
            u0[0] = 1
        else: # k odd
            l0,l1 = (self.k-3)//2, (self.k-1)//2
            for i in range(l0+1):
                u0[self.n-2*i-1] = self.newton(self.n-2*i-2,self.k-2*i-2)
            u0[0] = 1
            for i in range(l1+1):
                u1[self.n-2*i] = self.newton(self.n-2*i-1,self.k-2*i-1)
        return u0,u1
    
    def getBasicSMatrix(self,u):
        S = [[] for i in range(self.n)]
        for j in range(len(u)):
            if(u[j]>0 and j<=self.n):
                col = [self.DARK]*j+[self.LIGHT]*(self.n-j)
                perms = multiset_permutations(col)
                for p in perms:
                    for i in range(u[j]):
                        for idx in range(self.n):
                            S[idx].append(p[idx])
        return S
            
    def getCMatricesImproved(self):
        u0,u1 = self.getUVectors()
        S0,S1 = self.getBasicSMatrix(u0),self.getBasicSMatrix(u1)
        self.m = len(S0[0])
        perms = permutations([i for i in range(self.m)])
        for permutation in perms:
            self.C0.append(self.permute(S0, permutation))
            self.C1.append(self.permute(S1, permutation))
        self.m0, self.m1 = self.factors(self.m)
        self.r = len(self.C0)
    
    def kCMatrices(self):
        self.m = 2**(self.k-1)
        self.r = factorial(2**(self.k-1))
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
        perms = permutations([i for i in range(self.m)]) #permuting columns
        self.m = len(S0[0])
        for permutation in perms:
            self.C0.append(self.permute(S0, permutation))
            self.C1.append(self.permute(S1, permutation))
        self.m1, self.m0 = self.factors(self.m)

    def k2CMatrices(self):
        self.m = self.n
        self.m0 = self.m
        self.m1 = 1
        S0 = [[self.LIGHT if j>0 else self.DARK for j in range(self.m)] for i in range(self.n)]
        S1 = [[self.LIGHT if j!=i else self.DARK for j in range(self.m)] for i in range(self.n)]

        perms = permutations([i for i in range(self.m)])
        for permutation in perms:
            self.C0.append(self.permute(S0, permutation))
            self.C1.append(self.permute(S1, permutation))
        self.r = len(self.C0)

    def knCMatrices(self):
        self.constructHashes()
        expC0, expC1 = [[[[]for i in range(self.m)] for i in range(self.n)] for i in range(self.r**self.l)],[[[[]for i in range(self.m)] for i in range(self.n)] for i in range(self.r**self.l)]
        t = self.getVector()
        for tidx in range(self.r**self.l):
            for i in range(self.n):
                for j in range(self.m):
                    h = self.getHashFunction()
                    expC0[tidx][i][j] = self.C0[t[j%self.l]-1][self.solve(h,i)][j]
                    h = self.getHashFunction()
                    expC1[tidx][i][j] = self.C1[t[j%self.l]-1][self.solve(h,i)][j]
            t = self.incrementVector(t)
        self.C0 = expC0
        self.C1 = expC1
        self.r = len(self.C0)

    def colourCMatrices(self):
        colourC0 = [[[] for j in range(self.n)] for i in range(self.r)]
        colourC1 = [[[] for j in range(self.n)] for i in range(self.r)]
        extension = self.getSizeMulti3()
        for i in range(self.r):
            for j in range(self.n):
                for l in range(0,self.m+extension,3):
                    colour = self.getTriple(self.C0,i,j,l)
                    colourC0[i][j].append(colour)
                    colour = self.getTriple(self.C1,i,j,l)
                    colourC1[i][j].append(colour)
        self.C0 = colourC0
        self.C1 = colourC1
        self.m = len(self.C0[0][0])
        self.m1, self.m0 = self.factors(self.m)
    
    def improved(self):
        self.getCMatricesImproved()
        self.colourCMatrices()

    def conditional(self):
        if(self.k==2):
            self.k2CMatrices()
            self.colourCMatrices()
        elif(self.k==self.n):
            self.kCMatrices()
            self.colourCMatrices()
        else:
            self.naorShamir()

    def naorShamir(self):
        self.kCMatrices()
        self.knCMatrices()
        self.colourCMatrices()

    def getCMatrices(self, mode = 3):
        if(mode==1):
            self.naorShamir()
        elif(mode==2):
            self.conditional()
        else:
            self.improved()
        
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
        res = deepcopy(img1)
        for i in range(img1.height):
            for j in range(img1.width):
                res.image_matrix[i][j] = self.addColour(img1[i,j],img2[i,j])
        return res

    def combineShares(self):
        res = deepcopy(self.resImages[0])
        for i in range(1,len(self.resImages)):
            res = self.combine(res, self.resImages[i])
        res.update_image()
        return res

    def combineSharesByIdx(self, indices):
        if(len(indices)<1):
            return None
        if(len(indices)==1):
            return self.resImages[indices[0]]
        res = deepcopy(self.resImages[indices[0]])
        for i in range(1,len(indices)):
            if(indices[i]<len(self.resImages)):
                res = self.combine(res, self.resImages[indices[i]])
        res.update_image()
        return res


