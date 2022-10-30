from vc import *
from random import randint, shuffle

def test_permute(n,m,vc: VC):
    permutation = [i for i in range(m)]
    shuffle(permutation)
    S = [[randint(1,100) for j in range(m)] for i in range(n)]
    newS = vc.permute(S, permutation)
    print(f"S = {S}\np = {permutation}\n=> {newS}")

# def test_simple():
    # vc = VC(3,3)
    # array = np.asarray([   [BLACK, OTHER, OTHER],
    #             [BLACK, BLACK, BLACK],
    #             [OTHER, BLACK, OTHER] ])
    # img = CImage()
    # img.update_matrix(array)
    # img.width, img.height = 3,3
    # img.update_image()

    # shares = vc(img)
    # decryptedImg = vc.combineShares()
    # decryptedImg.show_image()

def test_image(filename = "circles.png"):
    vc = VC(2,3)
    # vc = VC(3,6)
    print("--init")
    # path = f".\\algorithm\\k-images\\test_img\\{filename}"
    path = f"D:\\Rok_Akademicki_22-23\\Praca_Inzynierska\\doku\\obrazy\\{filename}"
    img = CImage()
    img.read_image(path)
    # img.show_image()
    print("--run")
    shares = vc(img)
    # print shares
    for share in shares:
        share.show_image()
    print("--shares")
    decryptedImg = vc.combineShares()
    print("--combined")
    # peint result image
    decryptedImg.show_image()
    print("--end")

def test_vectors(r=5,l=3):
    t = [i+1 for i in range(r)]
    vectors = [p for p in product(t, repeat=l)]
    if(len(vectors) != r**l):
        print("wrong vector construction!!!")
    print(len(vectors))
    # print(vectors)
    


# test_simple()
test_image()


# test_vectors()
# class testVC():
#     def __init__(self):
#         self.n = 3
#         self.k = 2

#     def newton(self,n,k):
#         return int(comb(n,k))
    
#     def getUVectors(self):
#         u0,u1 = [0]*(self.n+1),[0]*(self.n+1)
#         if(self.k%2==0): # k even
#             l = (self.k-2)//2
#             for i in range(l+1):
#                 u0[self.n-2*i] = self.newton(self.n-2*i-1,self.k-2*i-1)
#                 u1[self.n-2*i-1] = self.newton(self.n-2*i-2,self.k-2*i-2)
#             u0[0] = 1
#         else: # k odd
#             l0,l1 = (self.k-3)//2, (self.k-1)//2
#             for i in range(l0+1):
#                 u0[self.n-2*i-1] = self.newton(self.n-2*i-2,self.k-2*i-2)
#             u0[0] = 1
#             for i in range(l1+1):
#                 u1[self.n-2*i] = self.newton(self.n-2*i-1,self.k-2*i-1)
#         return u0,u1
    
#     def getBasicSMatrix(self,u): #!!!!!!
#         S = [[] for i in range(self.n)]
#         for j in range(len(u)):
#             if(u[j]>0):
#                 if(j>self.n):
#                     print("j>n!!!")
#                     break;
#                 col = [1]*j+[0]*(self.n-j)
#                 perms = multiset_permutations(col)
#                 for p in perms:
#                     for i in range(u[j]):
#                         for idx in range(self.n):
#                             S[idx].append(p[idx])
#         return S

# tv = testVC()
# u,v = tv.getUVectors()
# S0 = tv.getBasicSMatrix(u)
# print(S0)