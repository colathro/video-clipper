import cv2
import numpy as np
import time
from skimage import filters


class CSGO:

    def __init__(self):
        self.frame_count = -1
        self.on_cooldown = False
        self.on_cooldown_count = 0
        self.kill_feed_cleared = False
        self.kill_feed_clear_count = 0
        self.output_frame_stamps = []
        self.search_template = cv2.imread("./plugins/assets/csgo_v5.jpg", 0)

    def process_frame(self, filename):
        self.frame_count += 1
        preprocessed_img = self.process_img(filename)
        if (self.is_frag_frame(preprocessed_img)):
            print(f"frag frame {self.frame_count}")
            self.output_frame_stamps.append(self.frame_count)

    def is_frag_frame(self, img):
        white_pixels = (img > 0.0).sum()
        if (white_pixels >= 450):
            if (self.kill_feed_cleared == False):
                self.kill_feed_clear_count = 0
            return False
        elif (white_pixels == 0):
            if (self.kill_feed_cleared == False):
                self.kill_feed_clear_count += 1
            if (self.kill_feed_clear_count >= 40 and self.kill_feed_cleared == False):
                self.kill_feed_cleared = True
            return False
        elif (white_pixels > 100 and self.kill_feed_cleared):
            self.kill_feed_cleared = False
            print(white_pixels)
            return True
        elif (white_pixels > 0 and self.kill_feed_cleared == False):
            self.kill_feed_clear_count = 0
        else:
            return False

    def process_img(self, filename):
        image = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
        image = image[:((np.shape(image)[0]//2)//2),
                      ((np.shape(image)[1]//2)+(np.shape(image)[1]//4)):]

        rMin = 74
        bMin = 34
        gMin = 34
        rMax = 255
        bMax = 48
        gMax = 48

        # Set minimum and max HSV values to display
        lower = np.array([rMin, gMin, bMin])
        upper = np.array([rMax, gMax, bMax])

        # Create HSV Image and threshold into a range.
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(rgb, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f"{filename}", image)
        return output
