import cv2 #OpenCV

def noise_pattern_analysis(image_path, save_path):

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # image will be converted to single channel grayscale.
    # noise pattern are easier to detect in single channels

    denoised = cv2.GaussianBlur(img,(5,5),0)
    # (5,5) -> it's length and width
    # 0 -> x sigma -> smooths images gently , does not destroy noise pattern

    noise = cv2.absdiff(img, denoised)
    noise = cv2.normalize(noise, None, 0, 255, cv2.NORM_MINMAX)
    # 0 -> minimum range
    # 255 -> maximum range

    cv2.imwrite(save_path, noise)
