# Class and support code for handling operations on an individual frame
import cv2
import time
import numpy as np

class Frame:
    def __init__(self, frame_data, camera_coordinates: tuple, target_resolution: tuple):
        self.process_time = time.time()
        self.data = frame_data
        self.target_resolution = target_resolution
        self.camera = self.data[camera_coordinates[1]:camera_coordinates[3], camera_coordinates[0]:camera_coordinates[2]]
        self.background = self._stretch_and_blur()
        self.focus = self._stretch_main(camera_coordinates[2] - camera_coordinates[0]) # Subtract the position of the left side of the camera from the right to get the camera width
        return

    def _stretch_and_blur(self):
        height = self.target_resolution[1]
        target_width = self.target_resolution[0]
        scale_factor = height / self.data.shape[0]
        target_dimensions = (int(self.data.shape[1] * scale_factor), height)
        bounding = self._calc_bounding_x(target_dimensions, target_width)
        return cv2.GaussianBlur(cv2.resize(self.data, target_dimensions)[0:target_dimensions[1], bounding[0]:bounding[1]], (51,51), 0) # Slice the background to crop out any data that lies outside of the target X resolution before blurring

    def _stretch_main(self, cam_width):
        # Since the scaling will attempt to keep the center at the same coordinates, double the camera width and add to original width to compensate and remove the camera from frame
        target_width = self.data.shape[1] + (cam_width / 2)
        aspect_ratio = target_width / self.data.shape[1]
        target_dimensions = (int(target_width), int(self.data.shape[0] * aspect_ratio))
        bounding = self._calc_bounding_x(target_dimensions, self.target_resolution[0])
        return cv2.resize(self.data, target_dimensions)[0:target_dimensions[1], bounding[0]:bounding[1]]

    def _calc_bounding_x(self, dim, target_width):
        center_x = dim[0] / 2 # Center of the current array
        half_target_width = target_width / 2 # half the desired width to calculate width bounds
        bounding = (int(center_x - half_target_width), int(center_x + half_target_width))
        return bounding

    def _center_y_on_background(self, src: cv2.Mat):
        target_center_y = int(self.target_resolution[1] / 2)
        center_y = int(src.shape[0] / 2)
        layered = self.background.copy()
        layered[target_center_y - center_y:center_y + target_center_y] = src
        return layered

    def _center_x_on_background(self, src: cv2.Mat):
        target_center_x = int(self.target_resolution[0] / 2)
        center_x = int(src.shape[1] / 2)
        layered = self.background.copy()
        layered[0:src.shape[0], target_center_x - center_x:center_x + target_center_x] = src
        return layered

    def _fit_camera_to_vacancy(self, height_difference):
        scale_factor = height_difference / self.camera.shape[0]
        target_width = int(self.camera.shape[1] * scale_factor)
        if target_width % 2 != 0:
            target_width = target_width - 1
        target_dimensions = (target_width, height_difference)

        return cv2.resize(self.camera, target_dimensions)

    def composite(self):
        self.background = self._center_y_on_background(self.focus)
        focus_center_y = int(self.focus.shape[0] / 2)
        background_center_y = int(self.target_resolution[1] / 2)
        camera = self._fit_camera_to_vacancy(background_center_y - focus_center_y)
        self.process_time = time.time() - self.process_time
        return self._center_x_on_background(camera)

    def display(self):
        cv2.imshow('Frame', cv2.resize(self.composite(), (360, 640)))
        cv2.waitKey(10)
