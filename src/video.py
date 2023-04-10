# Class and utils for handling video data
import config
import pathlib
import cv2
import av
import util
from moviepy.editor import *
from frame import Frame

class Video:
    def __init__(self, video_source: pathlib.Path, start: None, duration: None):
        self.config = config.Config()
        self.target_res = (self.config.target_x, self.config.target_y)
        self.file = video_source
        self.current_frame = 0
        self.container = av.open(str(self.file.absolute()))
        self._edit(start, duration)
        self.container.close()
        self.raw = VideoFileClip(str(self.file.absolute()))
        self.clip = self._split(start, duration)
        self.fps = self.raw.fps
        return

    def _split(self, start: str, duration: float):
        # Perform several transformations and operations on time strings to get accurate start and end timestamps
        start_ms = util.timestring_to_ms(start)
        if duration == None or int(duration) == 0:
            end_ms = self.raw.duration
            end = util.ms_to_timestring(self.raw.duration * 1000)
        else:
            end_ms = start_ms + (float(duration) * 1000)
            end = util.ms_to_timestring(end_ms)
        return self.raw.subclip(t_start=start, t_end=end)

    def _calc_times(self, start: str, duration: float):
        # Perform several transformations and operations on time strings to get accurate start and end timestamps
        start_ms = util.timestring_to_ms(start)
        if duration == None or int(duration) == 0:
            end_ms = self.container.duration / 1000
        else:
            end_ms = start_ms + (float(duration) * 1000)
        return start_ms, end_ms

    def _edit(self, start: str, duration: float):
        streams = {'video': {}, 'audio': {}}
        output = av.open(f'{self.file.name.split(".")[0]}-edited_short.mp4', mode='w')
        start_ms, end_ms = self._calc_times(start, duration)
        # Because we have the millisecond duration already, we need to multiply it by the base_time denominator so it's maintained (Something to do with av.time_base being used here I assume)
        self.container.seek(start_ms * 1000)
        for packet in self.container.demux():
            if packet.dts == None:
                continue
            print(packet.dts)
            if packet.dts <= end_ms:
                new_packets = []
                for frame in packet.decode():
                    if (isinstance(frame.format, av.VideoFormat)):
                        f = Frame(frame.to_rgb().to_ndarray(), self.config.camera_pos, (self.config.target_x, self.config.target_y))
                        if (frame.index not in streams['video'].keys()):
                            streams['video'][frame.index] = output.add_stream(av.codec.Codec('mpeg4', 'w'))
                        # Perform image operations on the frame data
                        f.display()
                        #new_packets.append(streams['video'][frame.index].encode(av.video.frame.VideoFrame.from_ndarray(f.composite())))
                    elif (isinstance(frame.format, av.AudioFormat)):
                        # Handle the audio track
                        pass
                    else:
                        # Add the track to an output container without modification
                        pass
            else:
                break

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

    def _parse_audio(self):
        for packet in self.container.demux():
            for frame in packet.decode():
                print(frame.format, frame.dts, frame.index)
                pass