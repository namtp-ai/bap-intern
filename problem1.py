import cv2
import matplotlib.pyplot as plt
from numpy import ndarray


def read_image(image_path: str) -> ndarray:
    '''
    Read an image from image_path
    Returned image is horizontal by default.
    '''
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    (h, w) = img.shape[:2]
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img = img[int(0.005*h):, :]
    else:
        img = img[int(0.005*h):, int(0.01*w) : int(0.95*w)]
    return img

def process_image(image: ndarray) -> ndarray:
    '''
    Processing the image, including 3 steps:
    - Convert image from BGR to gray.
    - Blur image.
    - Apply threshold.
    '''
    # convert image to gray
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur image slightly
    blurred = cv2.GaussianBlur(img_grey, (7, 7), 0)

    # adaptive threshold
    thresh = cv2.adaptiveThreshold(
            blurred,
            255,
	        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 21, 6
    )
    return thresh

img = read_image('problem1-data/input2.jpg')
thresh = process_image(img)


plt.figure(figsize=(20, 15))
plt.imshow(thresh)
plt.show()
