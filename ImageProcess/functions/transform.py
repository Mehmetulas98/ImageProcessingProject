from skimage import io
from skimage.color import label2rgb
import numpy as np
from skimage.io import imread
from skimage.transform import rotate
from skimage.transform import swirl
from skimage.transform import integral_image
from skimage.transform import downscale_local_mean
from skimage.transform import iradon
SAVE_PATH = "static/media/"


def Swirl(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = swirl(noisy_image)
    io.imsave(SAVE_PATH+image_name, result)


def Rotate(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = rotate(noisy_image, 2, resize=True)
    io.imsave(SAVE_PATH+image_name, result)


def IntegralImage(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = integral_image(noisy_image)
    io.imsave(SAVE_PATH+image_name, result)


def DownscaleLocalMean(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = downscale_local_mean(noisy_image, (2, 3))
    io.imsave(SAVE_PATH+image_name, result)


def Iradon(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = iradon(noisy_image)
    io.imsave(SAVE_PATH+image_name, result)
