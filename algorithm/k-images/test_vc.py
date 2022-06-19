from vc import *
from random import randint, shuffle

def test_permute(n,m,vc: VC):
    permutation = [i for i in range(m)]
    shuffle(permutation)
    S = [[randint(1,100) for j in range(m)] for i in range(n)]
    newS = vc.permute(S, permutation)
    print(f"S = {S}\np = {permutation}\n=> {newS}")

def test_simple():
    vc = VC(3,3)
    array = np.asarray([   [BLACK, OTHER, OTHER],
                [BLACK, BLACK, BLACK],
                [OTHER, BLACK, OTHER] ])
    img = CImage()
    img.update_matrix(array)
    img.width, img.height = 3,3
    shares = vc(img)
    # shares[0].show_image()
    decryptedImg = vc.combineShares()
    decryptedImg.show_image()

def test_image():
    vc = VC(3,3)
    print("--init")
    path = "D:\\Rok_Akademicki_21-22\\zz_pictures\\black-white-birds.jpg"
    img = CImage()
    img.read_image(path)
    img.show_image()
    print("--run")
    shares = vc(img)
    print("--shares")
    decryptedImg = vc.combineShares()
    print("--combined")
    decryptedImg.show_image()
    


# test_simple()
test_image()

# vc = VC(3,3)
# test_permute(3,3,vc)