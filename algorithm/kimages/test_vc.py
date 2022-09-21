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

def test_image(filename = "really-big-picture.jpg"):
    vc = VC(4,4)
    print("--init")
    # path = f".\\algorithm\\k-images\\test_img\\{filename}"
    path = f"D:\\Rok_Akademicki_21-22\\Praca_Inzynierska\\Official_Repo\\vCryptography\\algorithm\\kimages\\test_img\\{filename}"
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
    


# test_simple()

test_image("penta.png")

# vc = VC(3,3)
# test_permute(3,3,vc)

