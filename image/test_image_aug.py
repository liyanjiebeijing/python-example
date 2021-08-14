import imgaug as ia
from imgaug import augmenters as iaa
import cv2
import numpy as np
import time


def test_imgaug():
    image = cv2.imread('lena.png')
    images = [image, image, image, image]

    ia.seed(25)
    seq = iaa.Sequential([
        iaa.Affine(rotate=(-25, 25)),
        iaa.AdditiveGaussianNoise(scale=(0, 50)),
        iaa.Crop(percent=(0, 0.5)),
        iaa.JpegCompression(compression=(95, 95))
    ])
    images_aug = seq(images=images)

    cv2.imshow('aug', np.hstack(images_aug))
    cv2.waitKey()
    

def test_compress_aug():
    image = cv2.imread('lena.png')

    jpeg_aug = iaa.JpegCompression(compression=(50, 90))
    images_aug = jpeg_aug(image=image)

    cv2.imshow('compress_aug', images_aug)
    cv2.waitKey()


def test_compress_aug_perf():
    image = cv2.imread('lena.png')

    jpeg_aug = iaa.JpegCompression(compression=(50, 90))

    kPreTimes = 5
    for _ in range(kPreTimes):
        images_aug = jpeg_aug(image=image)

    #test batch = 1
    start = time.time()
    kTimes = 100
    for _ in range(kTimes):
        images_aug = jpeg_aug(image=image)
    stop = time.time()
    print('batch = 1 average cost: %.3fms' % ((stop - start) * 1000 / kTimes))


    #test batch = 10
    start = time.time()
    kBatch = 128
    kTimes = 10
    images = [image for _ in range(kBatch)]
    for _ in range(kTimes):
        images_augs = jpeg_aug(images=images)
    stop = time.time()
    print('batch = 1 average cost: %.3fms' % ((stop - start) * 1000 / kTimes))


if __name__ == '__main__':
    test_compress_aug()
    # test_compress_aug_perf()