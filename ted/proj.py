import cv2
import numpy as np

img_path = './couple1.jpg'


image = cv2.imread(img_path)



for i in [0.1, 0.3, 0.5, 0.7, 0.9]:
    stylized_image = cv2.stylization(image, sigma_s=100, sigma_r=i)
    cv2.imwrite(f'stylized_couple1_{i}.jpg', stylized_image)
    

# 스케치 렌더링 결과를 저장하거나 다른 처리를 수행할 수 있습니다.