import argparse
import uuid
import os
import ffmpeg
import datetime
import shutil

from plugins.csgo import CSGO


def parse_args():
    parser = argparse.ArgumentParser(
        description='automatically trim video clips')
    parser.add_argument('--file', dest="file", type=str,
                        help='video file to process.')
    parser.add_argument('--game', dest="game", type=str,
                        help='game flag i.e. csgo')
    return parser.parse_args()


def map_game_to_parser(game):
    if game.lower() == "csgo":
        return CSGO()
    raise Exception(f'{game} is not a valid game.')


class ClipperSession:
    output = "./output"
    tmp = "./tmp"

    def __init__(self, filename, game):
        self.filename = filename
        self.game = game
        self.plugin = map_game_to_parser(self.game)
        self.id = str(uuid.uuid4())

    def run(self):
        try:
            self.ensure_output_dir()
            self.ensure_tmp_dir()
            self.generate_screenshots()
            self.process_screenshots()
            self.process_timestamps()
        finally:
            # self.clean_up_tmp_dir()
            print("done")

    def generate_screenshots(self):
        (ffmpeg.input(self.filename)
            .filter('fps', fps=10)
            .output(f'{self.tmp}/{self.id}/%d.jpg',
                    video_bitrate='2500k',
                    sws_flags='bilinear',
                    start_number=0)
            .run())

    def process_screenshots(self):
        img_files = os.listdir(f'{self.tmp}/{self.id}')

        # sort needs to be based on the int frame number NOT string
        img_files.sort(key=lambda x: int(x.split(".")[0]))

        for img in img_files:
            self.plugin.process_frame(f'{self.tmp}/{self.id}/{img}')
        print(self.plugin.output_frame_stamps)

    def process_timestamps(self):
        for frame_num in self.plugin.output_frame_stamps:
            start_seconds = (frame_num - 7.5) / 10
            stream = ffmpeg.input(self.filename)
            stream = ffmpeg.trim(stream, start=str(datetime.timedelta(
                seconds=start_seconds)), end=str(datetime.timedelta(seconds=start_seconds+1)), duration=1)
            stream = ffmpeg.setpts(stream, 'PTS-STARTPTS')
            stream = ffmpeg.output(stream,
                                   f'{self.output}/{self.id}/{self.plugin.output_frame_stamps.index(frame_num)}.mp4')
            ffmpeg.run(stream)

    def ensure_output_dir(self):
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        os.mkdir(os.path.join(self.output, self.id))

    def ensure_tmp_dir(self):
        if not os.path.exists(self.tmp):
            os.mkdir(self.tmp)
        os.mkdir(os.path.join(self.tmp, self.id))

    def clean_up_tmp_dir(self):
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)


if __name__ == "__main__":
    args = parse_args()
    session = ClipperSession(args.file, args.game)
    session.run()
