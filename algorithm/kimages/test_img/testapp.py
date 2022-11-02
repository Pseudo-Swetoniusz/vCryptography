from msilib.schema import Error
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
        self.testAddColour()
        self.testGetSizeMulti3()
        self.testPermute(16,20)
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
    
    def testGetUVectors(self):
        pass

    def testGetBasicSMatrix(self,u):
        pass

    def testGetCMarticesImproved(self):
        pass

    def testColourCMatricesImproved(self):
        pass

    def testBuildShares(self, i: int, j: int):
        pass

    def testEncrypt(self):
        pass
    
    def testCombine(self, img1: CImage, img2: CImage):
        pass

        
        

if __name__ == '__main__':
    # test = TestVC()
    # test.main()
    test = TestUnitVC()
    test.main()