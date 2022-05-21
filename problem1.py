from tkinter.tix import Tree
import cv2
import matplotlib.pyplot as plt
from numpy import ndarray


def read_image(image_path: str) -> ndarray:
    '''
    read_image(image_path)
    Read an image from image_path.
    -------------
    Parameters
    -------------
    image_path: str
        `image_path` refers to the path that links to input image.
    -------------
    Return
    -------------
    ndarray
        Ndarray formatted image that is horizontal by default.
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
    process_image(image)
    Processing the image, including 3 steps:
    - Convert image from BGR to gray.
    - Blur image.
    - Apply threshold.
    -------------
    Parameters
    -------------
    image: ndarray
        `image` refers to the image that needs processing.
    -------------
    Return
    -------------
    ndarray
        Ndarray formatted image that is processed (gray -> blur -> thresh).
    '''
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img_grey, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(
            blurred,
            255,
	        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 21, 6
    )
    return thresh

def find_contours(thresh: ndarray) -> list:
    '''
    -------------
    Parameters
    -------------
    thresh: ndarray
        `thresh` refers to the image that processed by method `process_image`.
    -------------
    Return
    -------------
    ndarray
        Return list, or tree of lists of points.
    '''
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]
    return contours

def find_all_coordinates(contours) -> list:
    '''
    -------------
    Parameters
    -------------
    contours: list
        `contours` refers to the list of points found by findContours.
    -------------
    Return
    -------------
    list
        Return list of all coordinates of tables.
    '''
    rect = []
    all_coordinates = []

    for c in contours:
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        if area > 10000:
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            if len(approx) == 4:
                rect.append(approx)
            elif len(approx) >= 6 and len(approx) <= 8:
                rect.append(approx)

    for i in rect:
        table = []
        for j in i:
            x, y = j[0]
            table.append(x)
            table.append(y)
        all_coordinates.append(table)
    return all_coordinates

def find_crop_coordinates(img, tables):
    '''
    -------------
    Parameters
    -------------
    img: ndarray
        `img` refers to the original image.
    tables: list
        `tables` refers to all coordinates of the tables.
    -------------
    Return
    -------------
    list[tuple]        
        Return list of tuples, each includes index of main question and cropped image of that table.
    '''
    crop_coordinates = []
    main_ques = []

    for table in tables:
        x = []
        y = []
        for i in range(len(table)): 
            if i % 2 == 0:
                x.append(table[i])
            else:
                y.append(table[i]) 
        top_left_x = min(x)
        top_left_y = min(y)
        bot_right_x = max(x)
        bot_right_y = max(y)
        crop_coordinates.append([top_left_x, top_left_y, bot_right_x, bot_right_y])
    crop_coordinates = sorted(crop_coordinates, key = lambda x: x[:][0])

    for i in range(len(crop_coordinates)):
        top_left_x, top_left_y, bot_right_x, bot_right_y = crop_coordinates[i]
        crop_table = img[top_left_y - 15 : bot_right_y + 15, top_left_x - 15 : bot_right_x + 15]
        main_ques.append((i + 1, crop_table))
    return main_ques

def horizontal_detect(table):
    '''
    horizontal_detect(table)
        Detecting all the horizontal lines in the image `table`
    -------------
    Parameters
    -------------
    table: ndarray
        `table` refers to the cropped image containing a table of one main question.
    -------------
    Returns
    -------------
    Return list or tree of list containing points of horizontal lines
    '''
    # Process image
    thresh = process_image(table)

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    return cnts

def vertical_detect(table):
    '''
    vertical_detect(table)
        Detecting all the horizontal lines in the image `table`
    -------------
    Parameters
    -------------
    table: ndarray
        `table` refers to the cropped image containing a table of one main question.
    -------------
    Returns
    -------------
    Return list or tree of list containing points of vertical lines
    '''
    # Process image
    thresh = process_image(table)

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(detect_vertical, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    return cnts

def get_result(main_ques):
    '''
    get_result(main_ques)
        Get the result for this problem: Number of main questions and number of sub-anwsers in each main question.
    -------------
    Parameters
    -------------
    main_ques: list[tuple]        
        `main_ques` includes index of main question and cropped image of that table.
    -------------
    Returns
    -------------
    Print number of main questions and number of sub-anwsers in each main question
    '''
    answers = []
    for q in main_ques:
        index, table = q
        v = vertical_detect(table)
        h = horizontal_detect(table)
        #if len(v) == 2:
        b = []
        for i in range(len(v)):
            a = []
            for j in v[i]:
                a.append(j[0][-1])
            b.append(max(a) - min(a))
        c = max(b) - min(b)
        if c < 50:
            answers.append((index, ((len(v) - 1) * (len(h) - 1) / 2)))
        else:
            temp1 = len(v) - 2
            last_horizontal = []
            for i in h[-1]:
                last_horizontal.append(i[0][0])
            last = max(last_horizontal) - min(last_horizontal)

            temp2 = 0
            idx = 0
            for i in range(len(h) - 1):
                first_horizontal = []
                for j in h[i]:
                    first_horizontal.append(j[0][0])
                first = max(first_horizontal) - min(first_horizontal)
                
                if abs(first - last) < 10:
                    temp2 = idx
                    break 
                else:
                    idx += 1
            answers.append((index, temp1 * (len(h) - 1) / 2 + (temp2 - 1) / 2))
    for answer in answers:
        print('Main question', answer[0], 'includes ', int(answer[-1]), 'subanswer cells')

if __name__ == '__main__':
    img = read_image('problem1-data/input2.jpg')
    thresh = process_image(img)
    contours = find_contours(thresh)
    all_coordinates = find_all_coordinates(contours)
    main_ques = find_crop_coordinates(img, all_coordinates)
    get_result(main_ques)

    plt.figure(figsize=(20, 15))
    plt.imshow(img)
    plt.show()
