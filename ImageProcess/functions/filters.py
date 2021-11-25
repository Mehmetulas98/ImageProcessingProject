from skimage import io
from skimage.color import label2rgb
import numpy as np
from skimage.filters import threshold_mean
from skimage.filters import threshold_minimum
from skimage.filters import threshold_multiotsu
from skimage.filters import threshold_niblack
from skimage.filters import threshold_otsu
from skimage.filters import threshold_sauvola
from skimage.filters import threshold_triangle
from skimage.filters import threshold_yen
from skimage.filters import unsharp_mask
from skimage.filters import gaussian
from skimage.filters import hessian

SAVE_PATH = "static/media/"


def Hessian(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = hessian(noisy_image)
    io.imsave(SAVE_PATH+image_name, result)


def Gaussian(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = gaussian(noisy_image, sigma=1, mode='reflect')
    io.imsave(SAVE_PATH+image_name, result)


def UnsharpMask(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = unsharp_mask(noisy_image, radius=0.5, amount=2)
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdYen(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    thresh = threshold_yen(noisy_image)
    result = noisy_image <= thresh
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdTriangle(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    thresh = threshold_triangle(noisy_image)
    result = noisy_image > thresh
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdSauvola(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    t_sauvola = threshold_sauvola(noisy_image, window_size=15, k=0.7)
    result = noisy_image > t_sauvola
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdOtsu(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    thresh = threshold_otsu(noisy_image)
    result = noisy_image <= thresh
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdNiblack(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    q = 1
    result = threshold_niblack(noisy_image, k=0) * q
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdMultiotsu(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    thresh = threshold_multiotsu(noisy_image)
    regions = np.digitize(noisy_image, bins=thresh)
    result = label2rgb(regions)
    io.imsave(SAVE_PATH+image_name, result)


def ThresholdMean(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    thresh = threshold_mean(noisy_image)
    result = noisy_image > thresh
    io.imsave(SAVE_PATH+image_name, result)
