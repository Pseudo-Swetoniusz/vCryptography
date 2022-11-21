import unittest
from sys import path
path.append(".")

from algorithm.kimages.vc import *
from random import randint, sample, shuffle


class TestVC(unittest.TestCase):
    def main(self):
        print("--init main")
        self.test_black_recon()
        # self.brec_2k()
        # self.brec_3k3n()
        # self.brec_3k4n()
        print("--end")

    def brec_2k(self):
        test_images = ["penta.png", "circles.png", "cat.png", "tcs.png"]
        nvalues = [2, 3, 4, 5, 6]
        for n in nvalues:
            for name in test_images:
                print(f"--test{name}/2/{n}")
                self.test_black_recon(name,2,n)
    def brec_3k3n(self):
        test_images = ["penta.png", "circles.png", "cat.png", "tcs.png"]
        for name in test_images:
            print(f"--test{name}/3/3")
            self.test_black_recon(name,3,3)

    def brec_3k4n(self):
        # test_images = ["penta.png", "circles.png", "cat.png", "tcs.png"]
        test_images = ["circles.png"]
        for name in test_images:
            print(f"--test{name}/3/4")
            self.test_black_recon(name,3,4)

    def isBlack(self, pixel):
        return pixel[0]==0 and pixel[1]==0 and pixel[2]==0

    def test_decrypted_recon(self, vc: VC, img, decryptedImg):
        height, width = img.get_height(), img.get_width()
        w_scale, h_scale = vc.m0, vc.m1
        black, nonblack = 0,0
        wrong = []
        for i in range(height):
            for j in range(width):
                if(self.isBlack(img.image_matrix[i][j])):
                    black+=1
                    start = (i*h_scale, j*w_scale) #???
                    for p in range(h_scale):
                        for q in range(w_scale):
                            if(not self.isBlack(decryptedImg.image_matrix[start[0]+p][start[1]+q])):
                                wrong.append([(i,j),(start[0]+p,start[1]+q),img.image_matrix[i][j],decryptedImg.image_matrix[start[0]+p][start[1]+q]])
                else:
                    nonblack+=1
        
        if(len(wrong)==0):
            return "PASSED"
        return "FAILED"
        

    def test_black_recon(self,filename = "rec.png",k=3,n=4):
        #REDO: black recon perfect just for all shares combined
        print("--test_black_recon start")
        vc = VC(k,n)
        path = f"D:\\Rok_Akademicki_22-23\\Praca_Inzynierska\\doku\\obrazy\\{filename}"
        img = CImage()
        img.read_image(path)
        shares = vc(img)
        decryptedImg = vc.combineShares()

        test_num = 3
        for t in range(test_num):
            x = randint(k,n)
            indices = sample([i for i in range(n)],x)
            res = self.test_decrypted_recon(vc,img,vc.combineSharesByIdx(indices))
            print(f"{x}/{n} {res}")
        print("--test_black_recon end")
        # 3/4 FAILED
        # 3/4 FAILED
        # 3/4 FAILED
        # --test_black_recon end


class TestUnitVC(unittest.TestCase):
    vc = VC(2,2)

    def main(self):
        print("--init main")
        # turn off init!!!
        self.testFactors()
        # self.testAddColour()
        # self.testGetSizeMulti3()
        # self.testPermute(16,20)
        print("--end")
    
    def getRandPixel(self):
        return list(map(self.vc.TYPE, [randint(0,255),randint(0,255),randint(0,255)]))

    def testFactors(self,t=100):
        print("--factors")
        for test in range(t):
            m = randint(1,10000)
            x,y = self.vc.factors(m)
            self.assertEqual(x*y,m)

    def testAddColour(self,t=100):
        print("--add colours")
        p1 = self.getRandPixel()
        p2 = self.getRandPixel()
        p = self.vc.addColour(p1,p2)
        p = list(map(self.vc.TYPE2,p))
        p1 = list(map(self.vc.TYPE2,p1))
        p2 = list(map(self.vc.TYPE2,p2))
        self.assertTrue(p[0]<256 and p[1]<256 and p[2]<256)
        self.assertTrue(p[0]>=0 and p[1]>=0 and p[2]>=0)
        b = (p[0] == (p1[0]*p2[0])//255 and p[1] == (p1[1]*p2[1])//255 and p[2] == (p1[2]*p2[2])//255)
        if(not b):
            print("FAILS: ",p,p1,p2)
        self.assertTrue(b)

    def testPermute(self,n,m):
        print("--permute")
        permutation = [i for i in range(m)]
        shuffle(permutation)
        S = [[randint(1,100) for j in range(m)] for i in range(n)]
        newS = self.vc.permute(S, permutation)
        for col in range(m):
            for i in range(n):
                self.assertEqual(newS[i][col], S[i][permutation[col]])

    def testGetSizeMulti3(self,t=100):
        print("--extension")
        for i in range(t):
            self.vc.m = randint(0,10000)
            x = self.vc.getSizeMulti3()
            self.assertTrue(x>=0 and x<3)
            self.assertTrue((x+self.vc.m)%3==0)


class TestAlgos(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAlgos, self).__init__(*args, **kwargs)
        self.vc = None

    def main(self, testnum=5):
        filenames = ["rec","tcs-large"]
        print("--init main")
        for f in filenames:
            path = f"D:\Rok_Akademicki_22-23\Praca_Inzynierska\Official_Repo\\vCryptography\\algorithm\kimages\\test_img\\{f}.png"
            img = CImage()
            img.read_image(path)
            
            for n in range(2,6):
                for k in range(2,n+1):
                    vc = VC(k,n)
                    self.runAllImproved(vc,img)
                    print(f"PASSED I: {k},{n}: {f}")

            for n in range(2,5):
                vc = VC(2,n,mode=2)
                self.runAll2k(vc,img)
                print(f"PASSED M: 2,{n}: {f}")
            
            for k in range(3,5):
                vc = VC(k,k,mode=2)
                self.runAllkk(vc,img)
                print(f"PASSED M: {k},{k}: {f}")
            
            for n in range(2,5):
                for k in range(2,n+1):
                    vc = VC(k,n)
                    self.runAllClassic(vc,img)
                    print(f"PASSED C: {k},{n}: {f}")

    def runAllImproved(self,vc,img):
        self.testGetCMarticesImproved(vc)
        u,v = self.testGetUVectors(vc)
        self.testGetBasicSMatrix(vc,u)
        self.testGetBasicSMatrix(vc,v)
        self.testColourCMatrices(vc)
        
        res = vc(img)
        self.testEncrypt(vc,res)
        # self.testResult(vc,res,True)

    def runAll2k(self,vc,img):
        self.testk2CMatrices(vc)
        self.testColourCMatrices(vc)
        res = vc(img)
        self.testEncrypt(vc,res)

    def runAllkk(self,vc,img):
        self.testkCMatrices(vc)
        self.testColourCMatrices(vc)
        res = vc(img)
        self.testEncrypt(vc,res)

    def runAllClassic(self,vc,img):
        self.testkCMatrices(vc)
        self.testknCMatrices(vc)
        self.testColourCMatrices(vc)
        res = vc(img)
        self.testEncrypt(vc,res)

    def testGetUVectors(self,vc: VC):
        u,v = vc.getUVectors()
        self.assertEqual(vc.n+1, len(u), len(v))
        return u,v

    def testGetCMarticesImproved(self, vc: VC):
        vc.C0,vc.C1 = [],[]
        vc.m = 0
        vc.r = 0
        vc.getCMatricesImproved()
        C0,C1 = vc.C0,vc.C1
        expR = factorial(vc.m)
        self.assertEqual(len(C0), len(C1))
        self.assertEqual(len(C1),vc.r)
        self.assertEqual(vc.r,expR)
        self.assertEqual(len(C0[0]), len(C1[0]))
        self.assertEqual(len(C1[0]),vc.n)
        self.assertEqual(len(C0[0][0]), len(C1[0][0]))
        self.assertEqual(len(C1[0][0]),vc.m)

    def testGetBasicSMatrix(self,vc: VC, u):
        S = vc.getBasicSMatrix(u)
        newU = [0 for i in range(vc.n+1)]
        self.assertEqual(vc.n+1,len(u))
        for col in range(len(S[0])):
            w = 0 #wielokrotnosc kolumny
            for i in range(len(S)):
                if(S[i][col]==vc.DARK):
                    w += 1
            newU[w]+=1
        for i in range(vc.n+1):
            self.assertEqual(newU[i],u[i]*vc.newton(vc.n,i))

    def testk2CMatrices(self, vc: VC):
        vc.C0, vc.C1 = [],[]
        vc.S0, vc.S1 = [],[]
        vc.k2CMatrices()
        self.assertEqual(vc.m0*vc.m1,vc.m)
        self.assertEqual(vc.r, factorial(vc.m))
        self.assertEqual(vc.m,len(vc.C0[0][0]))
        self.assertEqual(vc.m,len(vc.C1[0][0]))
        self.assertEqual(vc.m,vc.n)
        self.assertEqual(vc.n,len(vc.C0[0]))
        self.assertEqual(vc.n,len(vc.C1[0]))
        self.assertEqual(vc.r,len(vc.C0))
        self.assertEqual(vc.r,len(vc.C1))
    
    def testkCMatrices(self, vc: VC):
        vc.m = 2**(vc.k-1)
        vc.r = factorial(2**(vc.k-1))
        vc.C0, vc.C1 = [],[]
        vc.S0, vc.S1 = [],[]
        vc.m0 = vc.m
        vc.m1 = 1
        vc.kCMatrices()
        self.assertEqual(vc.m0*vc.m1,vc.m)
        self.assertEqual(vc.r, factorial(vc.m))
        self.assertEqual(vc.m,len(vc.C0[0][0]))
        self.assertEqual(vc.m,len(vc.C1[0][0]))
        self.assertEqual(vc.m,2**(vc.k-1))
        self.assertEqual(vc.k,len(vc.C0[0]))
        self.assertEqual(vc.k,len(vc.C1[0]))
        self.assertEqual(vc.r,len(vc.C0))
        self.assertEqual(vc.r,len(vc.C1))

    def testknCMatrices(self, vc: VC):
        vc.l = ceil(log(vc.n,vc.k))+2
        vc.hashes = []
        vc.knCMatrices()
        self.assertEqual(vc.m0*vc.m1,vc.m)
        self.assertEqual(vc.r, factorial(vc.m)**vc.l)
        self.assertEqual(vc.m,len(vc.C0[0][0]))
        self.assertEqual(vc.m,len(vc.C1[0][0]))
        self.assertEqual(vc.n,len(vc.C0[0]))
        self.assertEqual(vc.n,len(vc.C1[0]))
        self.assertEqual(vc.r,len(vc.C0))
        self.assertEqual(vc.r,len(vc.C1))
    
    def testColourCMatrices(self, vc: VC):
        vc.colourCMatrices()
        self.assertEqual(vc.r, len(vc.C0))
        self.assertEqual(len(vc.C0), len(vc.C1))
        self.assertEqual(len(vc.C0[0]),len(vc.C1[0]))
        self.assertEqual(len(vc.C1[0]), vc.n)
        self.assertEqual(len(vc.C0[0][0]),len(vc.C1[0][0]))
        self.assertEqual(vc.m,len(vc.C0[0][0]))
        self.assertEqual(vc.m,vc.m0*vc.m1)

    def testBuildShares(self, vc: VC, i: int, j: int):
        imgI, imgJ = i*vc.m1,j*vc.m0
        for imgIdx in range(len(vc.resImages)):
            for p in range(vc.m1):
                for q in range(vc.m0):
                    self.assertEqual(vc.resImages[imgIdx][imgI+p][imgJ+q], vc.share[imgIdx][vc.m1*p+q])

    def testEncrypt(self, vc: VC, resImages):
        self.assertEqual(len(resImages),vc.n)
    
    def testCombine(self, vc: VC, img1: CImage, img2: CImage):
        img3 = vc.combine(img1, img2)
        for i in range(len(img3)):
            for j in range(len(img3[0])):
                self.assertEqual(vc.addColour(img1[i][j],img2[i][j]),img3[i][j])

    def testResult(self, vc: VC, img, pbr = False):
        # orig czarny -> res czarny
        # res kolor -> orig biały
        # procentowo?
        pass
        

if __name__ == '__main__':
    # test = TestVC()
    # test.main()
    # test = TestUnitVC()
    test = TestAlgos()
    test.main()