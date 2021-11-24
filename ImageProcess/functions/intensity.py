from skimage import io
from skimage.color import label2rgb
import numpy as np
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import hough_line
from skimage.draw import line
from skimage.io import imread
from skimage import io
from skimage.filters.rank import median
from skimage.morphology import disk

import os
SAVE_PATH = "static/media/"


def NoiseRemoval(image_name, im, konum, DiskValue):
    noisy_image = io.imread(konum, as_gray=True)
    noise = np.random.random(noisy_image.shape)
    noisy_image[noise > 0.99] = 1
    noisy_image[noise < 0.01] = 0
    fig, ax = plt.subplots(ncols=1, figsize=(10, 7), sharex=True, sharey=True)
    ax.imshow(median(noisy_image, disk(int(DiskValue))),
              vmin=0, vmax=255, cmap=plt.cm.gray)
    ax.set_title('Median $r=1$')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(SAVE_PATH+image_name)
    # plt.show()
    #io.imsave("static/media/"+image_name, result)
