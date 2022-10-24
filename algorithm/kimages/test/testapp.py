import unittest
from sys import path
path.append(".")

from algorithm.kimages.vc import *
from random import randint, shuffle


class TestVC(unittest.TestCase):

    def main(self):
        result = self.test_image()

    def isBlack(self, pixel):
        return pixel[0]==0 and pixel[1]==0 and pixel[2]==0

    def test_image(self,filename = "penta.png",k=3):
        vc = VC(k,k)
        print("--init")
        path = f"D:\\Rok_Akademicki_22-23\\Praca_Inzynierska\\doku\\obrazy\\{filename}"
        img = CImage()
        img.read_image(path)
        shares = vc(img)
        decryptedImg = vc.combineShares()
        
        height, width = img.get_height(), img.get_width()
        new_height, new_width = decryptedImg.get_height(), decryptedImg.get_width()
        w_scale, h_scale = new_width//width, new_height//height
        black, nonblack = 0,0
        wrong = []
        for i in range(height):
            for j in range(width):
                if(self.isBlack(img.image_matrix[i][j])):
                    black+=1
                    start = (i*h_scale, j*w_scale) #???
                    for p in range(start[0]):
                        for q in range(start[1]):
                            if(not self.isBlack(decryptedImg.image_matrix[start[0]+p][start[1]+q])):
                                wrong.append([(i,j),(start[0]+p,start[1]+q),img.image_matrix[i][j],decryptedImg.image_matrix[start[0]+p][start[1]+q]])
                            # self.assertTrue(self.isBlack(decryptedImg.image_matrix[start[0]+p][start[1]+q]))
                else:
                    nonblack+=1
        print("--end")
        print(len(wrong), len(wrong)/black*100, "%")
        print(wrong)
        return black,nonblack



if __name__ == '__main__':
    unittest.main()