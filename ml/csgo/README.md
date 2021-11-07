# Clip Requirements:
1. 1280x720 pixels
2. 30 fps
3. killfeed unobstructed

## Data Prep Pipeline:

Videos are named like: {guid}.mp4

1. Entire video is split into screenshots for each second.
2. Each screenshot is trimmed to the top right quandrant.
3. 640x360 screenshots are what are expected.
4. 10 screenshots (seconds) are grouped into a single image.
5. Image is named as such: {guid}_{firstframe}_{lastframe}_0000000000.png


## Data Labeling:

1. The expected output of the model is [0,0,0,0,0,0,0,0,0,0]
2. Each bit in the array is True/False if that frame contains a frag.
3. The label is added to the video title: {guid}_{firstframe}_{lastframe}_0100000000.png
4. From a human's perspective it's fairly easy to tell when something pops into the kill feed representing a frag.
5. Labels is just flipping bits in the filename if sections have a frag happen.

This pattern enables easy parsing of the data origin file, section of video it targets, and the label.
