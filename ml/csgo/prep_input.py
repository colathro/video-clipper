import os
import cv2
import numpy as np
import ntpath
import ffmpeg
import shutil


class Processor:

    base_label = '0000000000'

    def __init__(self, filename, out_dir='./out', tmp_dir='./tmp'):
        self.filename = filename
        self.out_dir = out_dir
        self.tmp_dir = tmp_dir
        self.file_id = ntpath.basename(self.filename).split('.')[0]
        self.tmp_id_dir = os.path.join(tmp_dir, self.file_id)
        self.out_id_dir = os.path.join(out_dir, self.file_id)

    def run(self):
        # setup outputs/tmp dirs
        self.ensure_output_dir()
        self.ensure_tmp_dir()

        # do the work
        self.generate_screenshots()
        self.crop_screenshots()
        self.combine_images()

        # cleanup the stuff
        # self.clean_up_tmp_dir()

    def generate_screenshots(self):
        (ffmpeg.input(self.filename)
            .filter('fps', fps=1)
            .output(f'{self.tmp_id_dir}/%d.jpg',
                    video_bitrate='2500k',
                    sws_flags='bilinear',
                    start_number=0)
            .run())

    def crop_screenshots(self):
        img_files = os.listdir(self.tmp_id_dir)
        for img_file in img_files:
            img_file = os.path.join(self.tmp_id_dir, img_file)
            img = cv2.imread(img_file, flags=cv2.IMREAD_COLOR)

            # resizes top top right quadrant
            img = img[:((np.shape(img)[0]//2)),
                      ((np.shape(img)[1]//2)+(np.shape(img)[1]//4)):]

            cv2.imwrite(img_file, img)

    def combine_images(self):
        img_files = os.listdir(self.tmp_id_dir)

        # need images in order to combine them
        img_files.sort(key=lambda x: int(x.split(".")[0]))

        for i in range(0, len(img_files), 10):
            # iterate through in groups of 10
            images = img_files[i:i+10]

            # NEED 10
            if (len(images) < 10):
                continue
            output = cv2.imread(os.path.join(self.tmp_id_dir, images.pop(0)))
            for img_file in images:
                img = cv2.imread(os.path.join(self.tmp_id_dir, img_file))
                output = np.concatenate((output, img), axis=1)
            out_file_name = f'{self.file_id}_{i}_{i+10}_{self.base_label}.jpg'
            cv2.imwrite(os.path.join(self.out_id_dir, out_file_name), output)

    def ensure_output_dir(self):
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        os.mkdir(os.path.join(self.out_dir, self.file_id))

    def ensure_tmp_dir(self):
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        os.mkdir(self.tmp_id_dir)

    def clean_up_tmp_dir(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    data_dir = './raw_data'
    files = os.listdir(data_dir)
    for f in files:
        processor = Processor(os.path.join(data_dir, f))
        processor.run()
