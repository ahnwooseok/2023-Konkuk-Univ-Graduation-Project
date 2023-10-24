import cv2
import numpy as np



img_path = '/Users/ahnwooseok/Downloads/github/2023-Konkuk-Univ-Graduation-Project/peter/AdobeStock_94274587_welsh_corgi_pembroke_CD.jpg'


image = cv2.imread(img_path)



for i in [0.1, 0.7, 0.75, 0.8, 0.85 ,0.9, 0.95]:
    stylized_image = cv2.stylization(image, sigma_s=100, sigma_r=i)
    cv2.imwrite(f'stylized_couple1222_{i}.jpg', stylized_image)