import argparse
import uuid
import os
import ffmpeg


def parse_args():
    parser = argparse.ArgumentParser(
        description='automatically trim video clips')
    parser.add_argument('--file', dest="file", type=str,
                        help='video file to process.')
    parser.add_argument('--game', dest="game", type=str,
                        help='game flag i.e. csgo')
    return parser.parse_args()


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
            .filter('fps', fps=.5)
            .output(f'{self.tmp}/{self.id}/%t.png',
                    video_bitrate='5000k',
                    sws_flags='bilinear',
                    start_number=0)
            .run())

    def ensure_output_dir(self):
        if os.path.exists(self.output):
            return
        os.mkdir(self.output)

    def ensure_tmp_dir(self):
        if os.path.exists(self.tmp):
            return
        os.mkdir(self.tmp)

    def clean_up_tmp_dir(self):
        if os.path.exists(self.tmp):
            os.rmdir(self.tmp)


if __name__ == "__main__":
    args = parse_args()
    session = ClipperSession(args.file, args.name)
    session.run()
