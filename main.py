import cv2
import numpy as np


def roiCaptcha(captcha, pos=1):

    image = cv2.imread('sources/captchas/'+captcha+'.png')

    heigt = image.shape[0]
    width = image.shape[1]

    w = int(width/5)

    x1 = w * (pos-1)
    x2 = x1 + w

    roi = image[0:heigt, x1:x2]
    cv2.imwrite('sources/templates/roi'+str(pos)+".png", roi)


def removeLines(image):
    gray = cv2.bitwise_not(image)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 2))

    eroded = cv2.erode(gray.copy(), kernel)

    dilated = cv2.dilate(eroded, kernel)

    return dilated


def matchTemplate(captcha, target):

    src_image = cv2.imread('sources/captchas/'+captcha+'.png', 0)
    src_template = cv2.imread('sources/templates/'+target+'.png', 0)

    image = removeLines(src_image)
    template = removeLines(src_template)

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc

    x = top_left[0]
    y = top_left[1]

    bottom_right = (x+w, y+h)
    cv2.rectangle(image, top_left, bottom_right, (255, 0, 0), 1)

    roi = image[y:y+h, x:x+w]

    cv2.imshow('image', image)
    cv2.imshow('match', roi)

    points = [x+w/2, y+h/2]
    print(points)

    cv2.waitKey(0)


if __name__ == "__main__":

    #matchTemplate('captcha1', 'caracol3')

    matchTemplate('captcha6', 'camera2')
