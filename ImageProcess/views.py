from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image
from numpy import asarray
import numpy as np
from matplotlib import pyplot as plt
from skimage.exposure import histogram
from skimage import data
from skimage.segmentation import flood, flood_fill

# Create your views here.


def asd(image_name):
    checkers = data.checkerboard()

    # Fill a square near the middle with value 127, starting at index (76, 76)
    filled_checkers = flood_fill(checkers, (76, 76), 127)

    fig, ax = plt.subplots(ncols=2, figsize=(10, 5))

    ax[0].imshow(checkers, cmap=plt.cm.gray)
    ax[0].set_title('Original')

    ax[1].imshow(filled_checkers, cmap=plt.cm.gray)
    ax[1].plot(76, 76, 'wo')  # seed point
    ax[1].set_title('After flood fill')

    plt.savefig("static/media/"+image_name+"2323"+".png")
    plt.show()


def index(request):
    Context = {}
    if(request.method == 'POST'):
        # OperationType = request.POST.get("document", "")
        return render(request, "main.html")
        # if(OperationType == "Görüntü İyileştirme Yöntemleri"):

        #     return render(request, "main.html")
        # elif(OperationType == "Histogram Görüntüleme ve Eşikleme"):
        #     Context['values'] = ["yöntem 3", "yöntem 4"]
        #     return render(request, "main.html", Context)
    else:

        return render(request, "index.html")


def main(request, operationtype):
    Context = {}
    # print(request.method)
    # if(operationtype == "Görüntü İyileştirme Yöntemleri"):
    #     print("kontrol 1")
    #     Context['values'] = ["yöntem 1", "yöntem 2", "yarrak"]
    #     Context['controller'] = True

    #     return render(request, "main.html", Context)
    # elif(request.method == 'POST'):
    #     print("kontrol 2")
    # print("kontrol 3")

    # return render(request, "main.html")
    print("request şekli :  " + str(request.method))
    if(request.method == "GET"):
        # burada işlemin foto gönderme
        if(operationtype == "Görüntü İyileştirme Yöntemleri"):
            print("giy")
            Context['values'] = ["yöntem 1", "yöntem 2", "yarrak"]
            Context['controller'] = True
            return render(request, "main.html", Context)
        elif(operationtype == "Histogram Görüntüleme ve Eşikleme"):
            Context['values'] = ["yöntem 4", "yöntem 5", "yarraksdsd"]
            Context['controller'] = True
            return render(request, "main.html", Context)

    else:

        if 'download' in request.POST:
            print("İNDİRME İŞLEMİ")
            # BURADA İNDİRECEK

            return render(request, "main.html", Context)

            # Burada ilgili işlerler

            # fotoyu formdan alma
        upl_file = request.FILES['document']
        print(upl_file)
        # # Foto bilgilerini kullanıp fotoyu kaydetme
        fs = FileSystemStorage()
        image_name = fs.save(upl_file.name, upl_file)
        Context['url'] = "media/"+image_name

        pil_path = "media/"+image_name
        with Image.open(pil_path) as im:
            asd(image_name=image_name)
            stringas = "/static/media/"

            Context['convertedurl'] = stringas + image_name+"2323" + ".png"

        if(operationtype == "Görüntü İyileştirme Yöntemleri"):
            print("giyy")
            Context['values'] = ["yöntem 1", "yöntem 2", "yarrak"]
            Context['controller'] = True
            return render(request, "main.html", Context)
