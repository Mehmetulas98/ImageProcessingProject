from skimage.exposure import histogram
from numpy import asarray
from matplotlib import pyplot as plt


def GrayLevelHistogram(image_name, im, konum):
    noisy_image = asarray(im)
    print(noisy_image.shape)
    hist, hist_centers = histogram(noisy_image)
    fig, ax = plt.subplots(ncols=1, figsize=(10, 5))
    ax.plot(hist_centers, hist, lw=2)
    ax.set_title('Gray-level histogram')
    plt.tight_layout()
    plt.savefig("static/media/"+image_name)
    # plt.show()
