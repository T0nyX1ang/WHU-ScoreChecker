"""
Process an image.

This module provides image to graybits, Otsu threshold and image resizing
function. All of the functions here are implemented by OpenCV.
"""
import cv2


def otsu(im):
    """
    Otsu algorithm.

    This algorithm thresholds an image to 0/1 value.
    """
    return cv2.threshold(im, 0, 255,
                         cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]


def preprocess(im):
    """
    Image pre-processing part.

    This module converts an image to graybits.
    """
    decode_im = cv2.imdecode(im, cv2.COLOR_RGBA2BGR)
    median_im = cv2.medianBlur(decode_im, 3)  # de-noising
    gray_im = cv2.cvtColor(median_im, cv2.COLOR_BGR2GRAY)  # to graybits
    return otsu(gray_im)


def resize(im, width, height):
    """
    Resize an image to a fixed size.

    This module resizes an image to 'width' * 'height'.
    """
    imh, imw = im.shape[0:2]
    # resize based on width-height radio.
    prew, preh = (width, int(imh * width / imw)) \
        if (width / imw < height / imh) else (int(imw * height / imh), height)
    padw, padh = (width - prew, height - preh)
    resize_im = cv2.resize(im, (prew, preh))
    padding_im = cv2.copyMakeBorder(resize_im, padh // 2, padh - padh // 2,
                                    padw // 2, padw - padw // 2,
                                    cv2.BORDER_CONSTANT, (0, 0, 0))
    return padding_im
