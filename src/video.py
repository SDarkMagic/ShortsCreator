# Class and utils for handling video data
import config
import pathlib
import cv2
#import threading
import util
from moviepy.editor import *
from frame import Frame

class Video:
    def __init__(self, video_source: pathlib.Path, start: None, duration: None):
        self.config = config.Config()
        self.target_res = (self.config.target_x, self.config.target_y)
        self.file = video_source
        self.current_frame = 0
        self.raw = VideoFileClip(str(self.file.absolute()))
        self.clip = self._split(start, duration)
        self.fps = self.raw.fps
        return

    def _split(self, start: str, duration: float):
        # Perform several transformations and operations on time strings to get accurate start and end timestamps
        start_ms = util.timestring_to_ms(start)
        end = util.ms_to_timestring(start_ms + (float(duration) * 1000))
        return self.raw.subclip(t_start=start, t_end=end)

    def save_sequence(self, output: pathlib.Path or None):
        hFile = cv2.VideoCapture(str(self.file.absolute()))
        writer = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
        self.fps = hFile.get(cv2.CAP_PROP_FPS)
        self.frames = hFile.get(cv2.CAP_PROP_FRAME_COUNT)

        if (output == None):
            output = self.file.with_name(f'{self.file.name.split(".")[0]}-edited_short.mp4')

        hOutput = cv2.VideoWriter(str(output.absolute()), writer, self.fps, self.target_res)
        while True:
            self.current_frame += 1
            ret, frame = hFile.read()
            if not ret:
                break
            f = Frame(frame, self.config.camera_pos, self.target_res)
            hOutput.write(f.composite())
            print(f'Estimated Time remaining: {int(((self.frames - self.current_frame) * f.process_time) * 1000)} seconds')
            del f
        hFile.release()
        hOutput.release()
        return

    def display(self):
        hFile = cv2.VideoCapture(str(self.file.absolute()))
        self.fps = hFile.get(cv2.CAP_PROP_FPS)
        while True:
            ret, frame = hFile.read()
            if not ret:
                break
            f = Frame(frame, self.config.camera_pos, self.target_res)
            f.display()
            del f
        hFile.release()
        return

    def save(self, output: pathlib.Path or None):
        if (output == None):
            output = self.file.with_name(f'{self.file.name.split(".")[0]}-edited_short.mp4')
        edited = self.clip.fl(self._process_frame)
        edited.write_videofile(str(output.absolute()))
        return

    def _process_frame(self, gf, t):
        frame = gf(t)
        f = Frame(frame, self.config.camera_pos, self.target_res)
        return f.composite()