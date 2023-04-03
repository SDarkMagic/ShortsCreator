# main program
import argparse
from moviepy.editor import *
import pathlib
import video

RESOLUTION_X = 1080
RESOLUTION_Y = 1920

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', help='Path to source video file.')
    parser.add_argument('start_time', help='Timestamp to begin short from, formatted as hh:mm:ss.mm')
    parser.add_argument('duration', help='Length of the outputted short formatted as ss.mm. If no value or 0 is provided, the entire remaining time of the video will be used.', nargs='?', default='0')
    parser.add_argument('-o --output', type=str, dest='output', default=None, help='Path to export the modified video file to. Defaults to the current directory.')

    args = parser.parse_args()
    base = video.Video(pathlib.Path(args.file_in), args.start_time, args.duration)
    if args.output != None:
        args.output = pathlib.Path(args.output)
    base.save(args.output)
    return

if __name__ == '__main__':
    main()