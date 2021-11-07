import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage import feature
from skimage.util import random_noise
from skimage import filters
from skimage.filters import threshold_otsu

image = cv2.imread("./277.jpg", flags=cv2.IMREAD_COLOR)
image = image[:((np.shape(image)[0]//2)//2),
              ((np.shape(image)[1]//2)+(np.shape(image)[1]//4)):]

original_image = image.copy()

# shape(480, 720, 3)

""" for i in range(len(image)):
    for j in range(len(image[i])):
        if (image[i][j][0] >= 34 and image[i][j][0] <= 48):
            if (image[i][j][1] >= 34 and image[i][j][1] <= 48):
                if (image[i][j][2] >= 74):
                    image[i][j] = [255, 255, 255]
                else:
                    image[i][j] = [0, 0, 0]
            else:
                image[i][j] = [0, 0, 0]
        else:
            image[i][j] = [0, 0, 0] """

rMin = 74
bMin = 20
gMin = 20
rMax = 255
bMax = 60
gMax = 60

# Set minimum and max HSV values to display
lower = np.array([rMin, gMin, bMin])
upper = np.array([rMax, gMax, bMax])

# Create HSV Image and threshold into a range.
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
mask = cv2.inRange(rgb, lower, upper)
output = cv2.bitwise_and(image, image, mask=mask)

image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

white_pixels = (image > 0.0).sum()
print(white_pixels)
plt.imshow(image, interpolation='none')
plt.show()
