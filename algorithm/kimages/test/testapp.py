from msilib.schema import Error
import unittest
from sys import path
path.append(".")

from algorithm.kimages.vc import *
from random import randint, shuffle


class TestVC(unittest.TestCase):

    def main(self):
        print("--init main")
        test_images = ["penta.png", "circles.png", "cat.png"]
        # kvalues = [2,3,4]
        kvalues = [4]
        for k in kvalues:
            for name in test_images:
                print(f"--test{name}/{k}")
                self.test_image(name,k)
        print("--end")

    def isBlack(self, pixel):
        return pixel[0]==0 and pixel[1]==0 and pixel[2]==0

    def test_image(self,filename = "penta.png",k=3):
        vc = VC(k,k)
        path = f"D:\\Rok_Akademicki_22-23\\Praca_Inzynierska\\doku\\obrazy\\{filename}"
        img = CImage()
        img.read_image(path)
        shares = vc(img)
        decryptedImg = vc.combineShares()
        
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
        
        print(len(wrong), black, nonblack)
        self.assertTrue(len(wrong)==0)



if __name__ == '__main__':
    test = TestVC()
    test.main()