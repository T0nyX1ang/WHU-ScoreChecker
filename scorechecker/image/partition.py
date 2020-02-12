"""
Split an image into 4 parts.

The partition module is based on OpenCV's findContours function.
It will take an image into several parts firstly.
If parts > 4, it will merge closest parts together using a new metric.
If parts < 4, it will split parts that has greatest width/height ratio,
and greatest square.
The final parts will be ready to be recognized by the model.
"""

import cv2
import itertools


def _metric(x1, l1, x2, l2):
    """
    A 1-d metric to define the distance between two lines.

    'x1', 'x2' are coordinates, 'l1', 'l2' are lengths
    """
    return min([abs(x1 + l1 - x2), abs(x2 + l2 - x1), abs(x1 - x2)])


def _distance(rect1, rect2):
    """
    A 2d metric to define the distance between two rectangles.

    'rect1', 'rect2' are rectangles, containing a tuple (x, y, w, h).
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return (_metric(x1, w1, x2, w2), _metric(y1, h1, y2, h2))


def _merge(rect1, rect2):
    """
    Merge two seperate rectangles.

    'rect1', 'rect2' are rectangles, containing a tuple (x, y, w, h).
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    x = x1 if (x1 < x2) else x2
    y = y1 if (y1 < y2) else y2
    w = max(x1 + w1, x2 + w2) - x
    h = max(y1 + h1, y2 + h2) - y
    return (x, y, w, h)


def _split(rect):
    """
    Split a rectangle into two parts.

    'rect' is a rectangle, containing a tuple (x, y, w, h).
    """
    x, y, w, h = rect
    return ((x, y, int(w * 0.57), h),
            (x + w - int(w * 0.57), y, int(w * 0.57), h))  # make larger room


def partition(im):
    """
    Split a captcha image into 4 single letters if we can.

    'im' is a 0/1 valued image read and thresheld by OpenCV/numpy.
    This should be the only function to use.
    """
    contours = cv2.findContours(im, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[0]
    current_parts = [cv2.boundingRect(contour) for contour in contours]
    current_parts = [val for val in current_parts
                     if val[2] * val[3] > 9]  # remove small points

    while len(current_parts) > 4:
        comb_parts = list(itertools.combinations(current_parts, 2))
        val = min(comb_parts, key=lambda x: _distance(x[0], x[1]))
        merge_result = _merge(val[0], val[1])
        current_parts.remove(val[0])
        current_parts.remove(val[1])
        current_parts.append(merge_result)  # merge nearest rectangles

    while len(current_parts) < 4:
        val = max(current_parts, key=lambda x: (x[2] / x[3], x[2] * x[3]))
        sp_rect1, sp_rect2 = _split(val)
        current_parts.remove(val)
        current_parts.append(sp_rect1)
        current_parts.append(sp_rect2)  # replacing a single rectangle with two

    current_parts.sort(key=lambda x: (x[0], x[1]))
    return current_parts
