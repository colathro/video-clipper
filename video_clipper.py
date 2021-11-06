import argparse
import uuid
import os
import ffmpeg
import shutil


def parse_args():
    parser = argparse.ArgumentParser(
        description='automatically trim video clips')
    parser.add_argument('--file', dest="file", type=str,
                        help='video file to process.')
    parser.add_argument('--game', dest="game", type=str,
                        help='game flag i.e. csgo')
    return parser.parse_args()


def map_game_to_parser(game):
    return


class ClipperSession:
    output = "./output"
    tmp = "./tmp"

    def __init__(self, filename, game):
        self.filename = filename
        self.game = game
        self.id = str(uuid.uuid4())

    def run(self):
        try:
            self.ensure_output_dir()
            self.ensure_tmp_dir()
            self.generate_screenshots()
        finally:
            self.clean_up_tmp_dir()

    def generate_screenshots(self):
        (ffmpeg.input(self.filename)
            .filter('fps', fps=4)
            .output(f'{self.tmp}/{self.id}/%d.jpg',
                    video_bitrate='2500k',
                    sws_flags='bilinear',
                    start_number=0)
            .run())

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
