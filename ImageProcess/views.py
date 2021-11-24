import cv2
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image
from numpy import asarray
import numpy as np
from matplotlib import pyplot as plt
from skimage import data
from skimage.segmentation import flood, flood_fill
import os
from skimage import io
from skimage.util import img_as_ubyte
from skimage.filters.rank import median
from skimage.morphology import disk, ball
from skimage.filters.rank import mean
from skimage.filters.rank import autolevel
from skimage.filters.rank import maximum, minimum, gradient
from .models import Video
from skimage.filters import hessian
# Create your views here.

from ImageProcess.functions.filters import *
from ImageProcess.functions.VideoPro import *
from ImageProcess.functions.morphology import *
from ImageProcess.functions.transform import *
from ImageProcess.functions.intensity import *
from ImageProcess.functions.histogram import *


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
    # noisy_image = img_as_ubyte(data.camera())

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


def index(request):
    Context = {}
    if(request.method == 'POST'):
        return render(request, "main.html")
    else:
        return render(request, "index.html")


def main(request, operationtype):
    Context = {}
    print("request şekli :  " + str(request.method))
    if(request.method == "GET"):
        if(operationtype == "Görüntü İyileştirme Yöntemleri"):
            Context['values'] = [
                "Hessian", "Gaussian", "UnsharpMask", "ThresholdYen", "ThresholdTriangle", "ThresholdSauvola", "ThresholdOtsu", "ThresholdNiblack", "ThresholdMultiotsu", "ThresholdMean"]

            return render(request, "main.html", Context)
        elif(operationtype == "Histogram Görüntüleme ve Eşikleme"):
            Context['values'] = [
                "GrayLevelHistogram"]
            Context['controller'] = True
            return render(request, "main.html", Context)
        elif(operationtype == "Uzaysal Dönüşüm İşlemleri"):
            Context['values'] = ["Swirl", "Rotate",
                                 "IntegralImage ", "DownscaleLocalMean", "Iradon"]
            Context['controller'] = True
            return render(request, "main.html", Context)
        elif(operationtype == "Yoğunluk Dönüşümü İşlemleri"):
            Context['values'] = ["NoiseRemoval"]
            Context['controller'] = True
            Context["IntensityControl"] = True
            return render(request, "main.html", Context)
        elif(operationtype == "Morfolojik İşlemler"):
            Context['values'] = ["Closing", "AreaClosing",
                                 "AreaOpening ", "BinaryClosing", "BinaryDilation", "BinaryOpening", "FloodFill", "Dilation", "Flood", "Erosion"]
            Context['controller'] = True
            return render(request, "main.html", Context)
        elif(operationtype == "Video İşleme"):
            return redirect("video")
    else:
        ###
        # İNDİRME İŞLEMİNİN YAPILDIĞI YER
        # if 'download' in request.POST:
        #     print("İNDİRME İŞLEMİ")
        #     DownloadFile = request.POST.get("DownloadImage", "")
        #     print(DownloadFile)

        #     fs = FileSystemStorage()
        #     image_name = fs.save(DownloadFile.name, DownloadFile)
        #     return render(request, "main.html", Context)
        # ###

        # Take image from template
        try:
            upl_file = request.FILES['document']
        except:
            return render(request, "main.html", Context)

        fs = FileSystemStorage()
        # Save image
        image_name = fs.save(upl_file.name, upl_file)
        # Originla image url
        Context['url'] = "media/"+image_name
        # Read image path for PIL
        pil_path = "media/"+image_name
        with Image.open(pil_path) as im:
            optype = request.POST['optype']
            print("işlem türü : "+str(optype))
            if(operationtype == "Görüntü İyileştirme Yöntemleri"):
                Context['values'] = [
                    "Hessian", "Gaussian", "UnsharpMask", "ThresholdYen", "ThresholdTriangle", "ThresholdSauvola", "ThresholdOtsu", "ThresholdNiblack", "ThresholdMultiotsu", "ThresholdMean"]
                Context['controller'] = True

                if(optype == "ThresholdYen"):
                    ThresholdYen(image_name=image_name,
                                 im=im, konum=Context['url'])
                elif(optype == "UnsharpMask"):
                    UnsharpMask(image_name=image_name,
                                im=im, konum=Context['url'])
                elif(optype == "Hessian"):
                    Hessian(image_name=image_name, im=im, konum=Context['url'])
                elif(optype == "Gaussian"):
                    Hessian(image_name=image_name, im=im, konum=Context['url'])
                elif(optype == "ThresholdTriangle"):
                    ThresholdTriangle(image_name=image_name,
                                      im=im, konum=Context['url'])
                elif(optype == "ThresholdSauvola"):
                    ThresholdSauvola(image_name=image_name,
                                     im=im, konum=Context['url'])
                elif(optype == "ThresholdOtsu"):
                    ThresholdOtsu(image_name=image_name,
                                  im=im, konum=Context['url'])
                elif(optype == "ThresholdNiblack"):
                    ThresholdNiblack(image_name=image_name,
                                     im=im, konum=Context['url'])
                elif(optype == "ThresholdMultiotsu"):
                    ThresholdMultiotsu(image_name=image_name,
                                       im=im, konum=Context['url'])
                elif(optype == "ThresholdMean"):
                    ThresholdMean(image_name=image_name,
                                  im=im, konum=Context['url'])

                stringas = "/static/media/"
                cwd = os.getcwd()
                print(cwd)
                cwd = cwd.replace("'\'", "'/'")
                print(cwd)
                path = cwd + stringas
                Context['convertedurl'] = stringas + image_name
                return render(request, "main.html", Context)
            if(operationtype == "Histogram Görüntüleme ve Eşikleme"):
                Context['values'] = [
                    "GrayLevelHistogram"]
                if(optype == "GrayLevelHistogram"):
                    GrayLevelHistogram(image_name=image_name,
                                       im=im, konum=Context['url'])

                Context['controller'] = True
                stringas = "/static/media/"
                cwd = os.getcwd()
                print(cwd)
                cwd = cwd.replace("'\'", "'/'")
                print(cwd)
                path = cwd + stringas
                Context['convertedurl'] = stringas + image_name
                return render(request, "main.html", Context)
            if(operationtype == "Uzaysal Dönüşüm İşlemleri"):
                Context['values'] = ["Swirl", "Rotate",
                                     "IntegralImage ", "DownscaleLocalMean", "Iradon"]
                Context['controller'] = True
                if(optype == "Swirl"):
                    Swirl(image_name=image_name,
                          im=im, konum=Context['url'])
                elif(optype == "Rotate"):
                    Rotate(image_name=image_name,
                           im=im, konum=Context['url'])
                elif(optype == "IntegralImage"):
                    IntegralImage(image_name=image_name,
                                  im=im, konum=Context['url'])
                elif(optype == "DownscaleLocalMean"):
                    DownscaleLocalMean(image_name=image_name,
                                       im=im, konum=Context['url'])
                elif(optype == "Iradon"):
                    Iradon(image_name=image_name,
                           im=im, konum=Context['url'])
                stringas = "/static/media/"
                cwd = os.getcwd()
                print(cwd)
                cwd = cwd.replace("'\'", "'/'")
                print(cwd)
                path = cwd + stringas
                Context['convertedurl'] = stringas + image_name
                return render(request, "main.html", Context)
            if(operationtype == "Yoğunluk Dönüşümü İşlemleri"):
                Context['values'] = ["NoiseRemoval"]
                Context['controller'] = True
                # Get IntensityValueOne
                IntensityValueOne = request.POST.get('InsensityValueOne')
                if(optype == "NoiseRemoval"):
                    NoiseRemoval(image_name=image_name, im=im,
                                 konum=Context['url'], DiskValue=IntensityValueOne)
                stringas = "/static/media/"
                cwd = os.getcwd()
                print(cwd)
                cwd = cwd.replace("'\'", "'/'")
                print(cwd)
                path = cwd + stringas
                Context['convertedurl'] = stringas + image_name
                return render(request, "main.html", Context)
            if(operationtype == "Morfolojik İşlemler"):
                Context['values'] = ["Closing", "AreaClosing",
                                     "AreaOpening ", "BinaryClosing", "BinaryDilation", "BinaryOpening", "FloodFill", "Dilation", "Flood", "Erosion"]
                Context['controller'] = True
                if(optype == "Closing"):
                    Closing(image_name=image_name,
                            im=im, konum=Context['url'])
                elif(optype == "AreaClosing"):
                    AreaClosing(image_name=image_name,
                                im=im, konum=Context['url'])
                elif(optype == "AreaOpening"):
                    AreaOpening(image_name=image_name,
                                im=im, konum=Context['url'])
                elif(optype == "BinaryClosing"):
                    BinaryClosing(image_name=image_name,
                                  im=im, konum=Context['url'])
                elif(optype == "BinaryDilation"):
                    BinaryDilation(image_name=image_name,
                                   im=im, konum=Context['url'])
                elif(optype == "BinaryOpening"):
                    BinaryOpening(image_name=image_name,
                                  im=im, konum=Context['url'])
                elif(optype == "FloodFill"):
                    FloodFill(image_name=image_name,
                              im=im, konum=Context['url'])
                elif(optype == "Dilation"):
                    Dilation(image_name=image_name,
                             im=im, konum=Context['url'])
                elif(optype == "Flood"):
                    Flood(image_name=image_name,
                          im=im, konum=Context['url'])
                elif(optype == "Erosion"):
                    Erosion(image_name=image_name,
                            im=im, konum=Context['url'])

                stringas = "/static/media/"
                cwd = os.getcwd()
                print(cwd)
                cwd = cwd.replace("'\'", "'/'")
                print(cwd)
                path = cwd + stringas
                Context['convertedurl'] = stringas + image_name
                return render(request, "main.html", Context)
            if(operationtype == "Video İşleme"):
                return redirect("video")


def video(request):
    Context = {}
    if(request.method == "POST"):
        print("POST VİDEO")
        try:
            upl_file = request.FILES['video']
        except:
            return render(request, "video.html", Context)

        fs = FileSystemStorage()
        video_name = fs.save(upl_file.name, upl_file)
        print(upl_file)
        path = "media/" + str(upl_file)
        Context["VideoUrl"] = VideoProcess(path=path)
        return render(request, "video.html", Context)
    else:
        print("GET VİDEO")
        return render(request, "video.html", Context)
