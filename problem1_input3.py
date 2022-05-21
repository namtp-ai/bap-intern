import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from scipy.signal import savgol_filter, find_peaks


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
    - Canny.
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
    canny = cv2.Canny(blurred, 20, 10)
    canny = cv2.Canny(canny, 20, 10)
    thresh = cv2.adaptiveThreshold(
            canny,
            255,
	        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 21, 6
    )
    return thresh

def horizontal_detect(thresh: ndarray, blank_image: ndarray) -> list:
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
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(blank_image, [c], -1, (36,255,12), 2)
    return cnts

def vertical_detect(thresh: ndarray, blank_image: ndarray) -> list:
    '''
    vertical_detect(table)
        Detecting all the vertical lines in the image `table`
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
    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(detect_vertical, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(blank_image, [c], -1, (36,255,12), 2)
    return cnts

def find_contours(thresh: ndarray) -> ndarray:
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
        Return an image only contains horizontal and vertical edges.
    '''
    h, w = thresh.shape[:2]
    blank_image = np.zeros((h, w, 3), np.uint8)
    horizontal_detect(thresh, blank_image)
    vertical_detect(thresh, blank_image)
    return blank_image
    
def histogram(blank_image: ndarray) -> ndarray:
    '''
    histogram(blank_image)
        Compute histogram along to the horizontal axis of the image
    -------------
    Parameters
    -------------
    blank_image: ndarray
    -------------
    Returns
    -------------
    A ndarray representing the histogram of pixel values along the horizontal axis.

    '''
    return np.sum(blank_image[:, :, 1], axis=0)

def predict_threshold(hist: ndarray) -> float:
    '''
    predict_threshold
    -------------
    Parameters
    -------------
    hist: ndarray
        A ndarray representing the histogram of pixel values along the horizontal axis.
    -------------
    Returns
    -------------
        Predicting a threshold that help define the gap between tables.
    '''
    weight = 5000
    hist, index = np.histogram(hist, round(len(hist)*10))

    max_hist1 = 0
    max_hist2 = 0

    max_index1 = 0
    max_index2 = 0
    
    for i in range(1, len(hist) - 1):
        pre = i - 1
        nex = i + 1
        while(hist[i] == hist[nex]):
            nex += 1
        if hist[i] > hist[pre] and hist[i] > hist[nex]:
            if(max_index1 == 0):
                max_hist1 = hist[i]
                max_index1 = i
            else:
                max_hist2 = hist[i]
                max_index2 = i
                break
        i = nex
            
    max_hist1 = index[max_index1]
    max_hist2 = index[max_index2]

    threshold = (weight * max_hist1 + max_hist2) / ((weight + 1))
    return threshold

def get_index(hist: ndarray, threshold: float) -> list:
    '''
    get_index(hist, threshold)
        Get index representing the horizontal coordinates to crop between tables.
    -------------
    Parameters
    -------------   
    hist: ndarray
        A ndarray representing the histogram of pixel values along the horizontal axis.
    threshold: float
        Predicting a threshold that help define the gap between tables.
    -------------
    Returns
    ------------- 
        List of indices used for cropping 
    '''
    e = np.where(hist > threshold, 1, 0)
    big_arr = []                    
    small_arr = []                  
    count = 0                       
    for i in range(len(e)):
        if(e[i] == 1):
            small_arr.append(i)
            count += 1
        elif(count != 0):
            big_arr.append([small_arr[0], small_arr[-1]])
            small_arr = []
            count = 0
    indices = []
    for i in big_arr:
        if (i[1] - i[0]) > 50:
            indices.append(i)
    return indices

def get_main_ques(img: ndarray, blank_image: ndarray, indices: list) -> tuple:
    '''
    get_main_ques(img, blank_image, indices)
        Get main questions (tables) from original image
    -------------
    Parameters
    -------------   
    img: ndarray
        Original image.
    blank_image: float
        Image that contains only horizontal and vertical edges.
    indices: list
        List contains indices representing horizontal coordinates to crop.
    -------------
    Returns
    ------------- 
        List of tuples including index and images containing single table (main question).
    '''
    main_ques = []
    main_ques_thresh = []
    for i, v in enumerate(indices):
        crop_table = img[:, v[0] - 15: v[1] + 15]
        crop_table_thresh = blank_image[:, v[0] - 10: v[1] + 10]
        main_ques.append((i+1, crop_table))
        main_ques_thresh.append((i+1, crop_table_thresh))
    return main_ques, main_ques_thresh

def get_rows(main_ques_thresh: list) -> list:
    '''
    get_rows(main_ques_thresh)
        Get rows in each table.
    -------------
    Parameters
    -------------   
    main_ques_thresh: list(tuple)
        List of tuples including index and images containing single table (main question).
    -------------
    Returns
    ------------- 
        List of images containing single rows of a table.
    '''
    total_rows = []
    for q in main_ques_thresh:
        index, table = q
        vertical_hist = np.sum(table[:, :, 1], axis=0)
        vertical_hist_smooth = savgol_filter(vertical_hist, 51, 3)
        vertical_peaks, _ = find_peaks(vertical_hist_smooth, distance=50)

        rows = []
        print('Question:', index, 'has', len(vertical_peaks)-1, 'rows')
        for i in range(len(vertical_peaks)-1):
            row = main_ques[index-1][1][:, vertical_peaks[i]+10: vertical_peaks[i+1]-10]
            rows.append(row)
        total_rows.append(rows)
    return total_rows

def horizontal_detect_table(table: ndarray) -> list:
    '''
    horizontal_detect_table(table)
        Detecting horizontal edges of cropped image.
    -------------
    Parameters
    -------------   
    table: ndarray
        Image cropped containg a table for a main question.
    -------------
    Returns
    ------------- 
        List of points in horizontal edges.
    '''
    img_grey = cv2.cvtColor(table, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img_grey, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
            blurred,
            255,
	        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 21, 6
    )
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    return cnts

def get_result(total_rows):
    '''
    get_result(main_ques)
        Get the result for this problem: Number of main questions and number of sub-anwsers in each main question.
    -------------
    Parameters
    -------------
    total_rows: list        
        List of images containing single rows of a table.
    -------------
    Returns
    -------------
    Print number of main questions and number of sub-anwsers in each main question
    '''
    index = 0
    for rows in total_rows:
        cells = 0
        index += 1
        for row in rows:
            horizons = horizontal_detect_table(row)
            col = int((len(horizons) - 1) / 2)
            cells += col
        print("Question: ", index, 'has', cells, 'subanswers')

if __name__ == '__main__':
    img = read_image('problem1-data/input3.jpg')
    thresh = process_image(img)
    blank_image = find_contours(thresh)
    hist = histogram(blank_image)
    threshold = predict_threshold(hist)
    indices = get_index(hist, threshold)
    main_ques, main_ques_thresh = get_main_ques(img, blank_image, indices)
    total_rows = get_rows(main_ques_thresh)
    get_result(total_rows)

    plt.figure(figsize=(20, 15))
    plt.imshow(img)
    plt.show()
