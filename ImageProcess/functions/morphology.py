from skimage import io
from skimage.color import label2rgb
from skimage.morphology import disk, ball
from skimage.morphology import flood_fill
from skimage.morphology import diamond
from skimage.morphology import erosion
from skimage.morphology import flood
from skimage.morphology import closing
from skimage.morphology import area_closing
from skimage.morphology import area_opening
from skimage.morphology import square
from skimage.morphology import binary_closing
from skimage.morphology import binary_dilation
from skimage.morphology import binary_erosion
from skimage.morphology import binary_opening
from skimage.morphology import dilation
from skimage.morphology import convex_hull_image
import numpy as np
from skimage.io import imread
from skimage import io


def Closing(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = closing(noisy_image, square(3))
    io.imsave("static/media/"+image_name, result)


def AreaClosing(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = area_closing(noisy_image, 8, connectivity=1)
    io.imsave("static/media/"+image_name, result)


def AreaOpening(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = area_opening(noisy_image, 8, connectivity=1)
    io.imsave("static/media/"+image_name, result)


def ConvexHullImage(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = convex_hull_image(noisy_image)
    io.imsave("static/media/"+image_name, result)


def BinaryDilation(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = binary_dilation(noisy_image)
    io.imsave("static/media/"+image_name, result)


def BinaryOpening(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = binary_opening(noisy_image)
    io.imsave("static/media/"+image_name, result)


def FloodFill(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = flood_fill(noisy_image, (0, 0), 5)
    io.imsave("static/media/"+image_name, result)


def Dilation(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = dilation(noisy_image)
    io.imsave("static/media/"+image_name, result)


def Flood(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = flood(noisy_image, (1, 1), connectivity=1)
    io.imsave("static/media/"+image_name, result)


def Erosion(image_name, im, konum):
    noisy_image = io.imread(konum, as_gray=True)
    result = erosion(noisy_image)
    io.imsave("static/media/"+image_name, result)
