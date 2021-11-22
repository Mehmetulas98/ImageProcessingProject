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
import os
from skimage.util import img_as_ubyte
from skimage.filters.rank import median
from skimage.morphology import disk, ball
from skimage.filters.rank import mean
from skimage.filters.rank import autolevel
from skimage.filters.rank import maximum, minimum, gradient
# Create your views here.


def ImageMorphology():

    noisy_image = img_as_ubyte(data.camera())

    closing = maximum(minimum(noisy_image, disk(5)), disk(5))
    opening = minimum(maximum(noisy_image, disk(5)), disk(5))
    grad = gradient(noisy_image, disk(5))

    # display results
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10),
                             sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(noisy_image, cmap=plt.cm.gray)
    ax[0].set_title('Original')

    ax[1].imshow(closing, cmap=plt.cm.gray)
    ax[1].set_title('Gray-level closing')

    ax[2].imshow(opening, cmap=plt.cm.gray)
    ax[2].set_title('Gray-level opening')

    ax[3].imshow(grad, cmap=plt.cm.gray)
    ax[3].set_title('Morphological gradient')

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.show()


def LocalAutolevel(image_name, im):
    noisy_image = asarray(im)
    #noisy_image = img_as_ubyte(data.camera())

    auto = autolevel(noisy_image.astype(np.uint16), disk(20))

    fig, ax = plt.subplots(ncols=2, figsize=(10, 5), sharex=True, sharey=True)

    ax[0].imshow(noisy_image, cmap=plt.cm.gray)
    ax[0].set_title('Original')

    ax[1].imshow(auto, cmap=plt.cm.gray)
    ax[1].set_title('Local autolevel')

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.savefig("static/media/"+image_name+"2323"+".png")
    plt.show()


def ImageSmoothing(image_name, im):

    noisy_image = asarray(im)
    loc_mean = mean(noisy_image, disk(10))

    fig, ax = plt.subplots(ncols=2, figsize=(10, 5), sharex=True, sharey=True)

    ax[0].imshow(noisy_image, vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[0].set_title('Original')

    ax[1].imshow(loc_mean, vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[1].set_title('Local mean $r=10$')

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.savefig("static/media/"+image_name+"2323"+".png")
    plt.show()


def NoiseRemoval(image_name, im):

    rng = np.random.default_rng()
    noisy_image = asarray(im)
    # noisy_image = img_as_ubyte(data.camera())
    noise = rng.random(noisy_image.shape)

    noisy_image[noise > 0.99] = 255
    noisy_image[noise < 0.01] = 0

    fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(noisy_image, vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[0].set_title('Noisy image')

    ax[1].imshow(median(noisy_image, disk(1)),
                 vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[1].set_title('Median $r=1$')

    ax[2].imshow(median(noisy_image, disk(5)),
                 vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[2].set_title('Median $r=5$')

    ax[3].imshow(median(noisy_image, disk(20)),
                 vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[3].set_title('Median $r=20$')

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.savefig("static/media/"+image_name+"2323"+".png")
    plt.show()


def GrayLevelHistogram(image_name, im):
    noisy_image = asarray(im)

    print(noisy_image.shape)
    hist, hist_centers = histogram(noisy_image)
    fig, ax = plt.subplots(ncols=1, figsize=(10, 5))
    ax.plot(hist_centers, hist, lw=2)
    ax.set_title('Gray-level histogram')
    plt.tight_layout()
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
            Context['values'] = [
                "GrayLevelHistogram", "NoiseRemoval", "ImageSmoothing", "LocalAutolevel"]
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
        # Take image from template
        upl_file = request.FILES['document']
        fs = FileSystemStorage()
        # Save image
        image_name = fs.save(upl_file.name, upl_file)
        # Originla image url
        Context['url'] = "media/"+image_name
        # Read image path for PIL
        pil_path = "media/"+image_name
        with Image.open(pil_path) as im:
            # Operation type
            optype = request.POST['optype']
            print("işlem türü : "+str(optype))

            if(optype == "GrayLevelHistogram"):
                GrayLevelHistogram(image_name=image_name, im=im)
            elif(optype == "NoiseRemoval"):
                NoiseRemoval(image_name=image_name, im=im)
            elif(optype == "ImageSmoothing"):
                ImageSmoothing(image_name=image_name, im=im)
            elif(optype == "LocalAutolevel"):
                LocalAutolevel(image_name=image_name, im=im)

            stringas = "/static/media/"
            cwd = os.getcwd()
            print(cwd)
            cwd = cwd.replace("'\'", "'/'")
            print(cwd)
            path = cwd + stringas
            Context['convertedurl'] = stringas + image_name+"2323" + ".png"

        if(operationtype == "Görüntü İyileştirme Yöntemleri"):
            print("giyy")
            Context['values'] = [
                "GrayLevelHistogram", "NoiseRemoval", "ImageSmoothing", "LocalAutolevel"]
            Context['controller'] = True
            return render(request, "main.html", Context)
