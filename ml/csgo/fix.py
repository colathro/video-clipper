import os
from glob import glob
import cv2
import numpy as np
import ntpath


original_image_files = [y for x in os.walk(
    './labeled') for y in glob(os.path.join(x[0], '*.jpg'))]

new_image_files = [y for x in os.walk(
    './out') for y in glob(os.path.join(x[0], '*.jpg'))]


def find_image(images, search_target):
    search_target = "_".join(search_target.split("_")[:3])
    for image in images:
        if (search_target in image):
            output = cv2.imread(image, flags=cv2.IMREAD_COLOR)
            return output


for og_image_path in original_image_files:
    og_image_filename = ntpath.basename(og_image_path)
    og_image = find_image(new_image_files, og_image_filename)
    cv2.imwrite(og_image_path, og_image)
