import os
import numpy as np
import cv2


def font_alignment_check(image_path, save_path):
    img = cv2.imread(image_path)

    if img is None:
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # convert into single channel gray scale, edge detection required single channel

    grad = cv2.Laplacian(gray, cv2.CV_64F)
    # detects edges and stroke , sensitive to text thickness , Font weight, sharp transitions
    #cv2.CV_64F -> output stored at 64-bit float , prevents overflow/underflow

    grad = np.abs(grad)
    # take absolute value

    max_val = np.max(grad)
    if max_val == 0:
        cv2.imwrite(save_path, img)
        return

    grad = np.uint8(255 * grad / max_val)
    #255 -> scale to image range
    #np.unit8 -> convert to 8 bit image
    #clean image suitable for thresholding

    _, bw = cv2.threshold(grad, 40, 255, cv2.THRESH_BINARY)
    #cv2.threshold -> converts grayscale to binary image
    # 40 -> threshold value
    # 255 -> white pixel value
    # cv2.THRESH_BINARY -> simple threshold

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 3))
    # kernel -> connectivity of neighbouring pixels
    # 25 -> width , connects characters horizontally
    # 3 -> height -> preserves line separation
    # rectangle shape

    morph = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    # Merge characters into words
    # Merge words into lines

    contours, _ = cv2.findContours(
        morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    boxes = []  # stores bounding boxes
    heights = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)  # bounding rectangle -> x,y -> top-left , w -> width , h -> height

        if w > 40 and h > 12:  # filter out small noise, dots and thin lines keep text regions
            boxes.append((x, y, w, h))
            # box for later drawing
            heights.append(h)

    if len(heights) < 3:
        cv2.imwrite(save_path, img)
        return

    # not enough data to compare, avoids false positives
    median_h = np.median(heights)

    heatmap = np.zeros(gray.shape, dtype=np.float32)

    for (x, y, w, h) in (boxes):
        deviation = abs(h - median_h) / median_h
        heatmap[y:y+h, x:x+w] += deviation

    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)

    heatmap = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    output = cv2.addWeighted(img, 0.7, heatmap_color, 0.3, 0)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cv2.imwrite(save_path, output)
