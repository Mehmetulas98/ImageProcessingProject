import cv2
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image
from numpy import asarray
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import morphology
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


FILTERS = ["Hessian", "Gaussian", "UnsharpMask", "ThresholdYen", "ThresholdTriangle",
           "ThresholdSauvola", "ThresholdOtsu", "ThresholdNiblack", "ThresholdMultiotsu", "ThresholdMean"]
HISTOGRAM = ["GrayLevelHistogram"]
TRANSFORM = ["Swirl", "Rotate", "IntegralImage",
             "DownscaleLocalMean", "Iradon"]
INTENSITY = ["NoiseRemoval"]
MORPHOLOGY = ["Closing", "AreaClosing",
              "AreaOpening", "ConvexHullImage", "BinaryDilation", "BinaryOpening", "FloodFill", "Dilation", "Flood", "Erosion"]


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
            Context['values'] = FILTERS
            return render(request, "main.html", Context)
        elif(operationtype == "Histogram Görüntüleme ve Eşikleme"):
            Context['values'] = HISTOGRAM
            return render(request, "main.html", Context)
        elif(operationtype == "Uzaysal Dönüşüm İşlemleri"):
            Context['values'] = TRANSFORM
            return render(request, "main.html", Context)
        elif(operationtype == "Yoğunluk Dönüşümü İşlemleri"):
            Context['values'] = INTENSITY
            Context["IntensityControl"] = True
            return render(request, "main.html", Context)
        elif(operationtype == "Morfolojik İşlemler"):
            Context['values'] = MORPHOLOGY
            return render(request, "main.html", Context)
        elif(operationtype == "Video İşleme"):
            return redirect("video")
    else:

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
                Context['values'] = FILTERS
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
                Context['values'] = HISTOGRAM
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
                Context['values'] = TRANSFORM
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
                Context['values'] = INTENSITY
                Context['controller'] = True
                Context["IntensityControl"] = True
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
                Context['values'] = MORPHOLOGY
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
                elif(optype == "ConvexHullImage"):
                    ConvexHullImage(image_name=image_name,
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
