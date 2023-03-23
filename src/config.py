# config.py - Handle parsing and writing of json config data to store information used between runs
import json
import pathlib
import os
from platform import system

# Checks if a directory exists and makes it if not
def findMKDir(checkDir):
    if isinstance(checkDir, pathlib.Path):
        checkDir = checkDir
    else:
        try:
            checkDir = pathlib.Path(checkDir)
        except:
            print('Failed to create the pathlib instance')
            return
    if checkDir.exists():
        return checkDir
    else:
        if ("." in pathlib.PurePath(checkDir).name):
            checkFile = checkDir
            checkDir = checkDir.parents[0]
            checkDir.mkdir(parents=True, exist_ok=True)
            checkFile.touch()
            return checkFile
        checkDir.mkdir(parents=True, exist_ok=True)
        return checkDir

def get_data_dir() -> pathlib.Path:
    if system() == "Windows":
        data_dir = pathlib.Path(os.path.expandvars("%LOCALAPPDATA%")) / "ShortsCreator"
    else:
        data_dir = pathlib.Path.home() / ".config" / "ShortsCreator"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

class Config:
    def __init__(self):
        self.path = get_data_dir() / 'config.json'
        raw = self._load()
        self.camera_pos = tuple(raw['camera_coords'])
        self.target_x = raw['target_dim_x']
        self.target_y = raw['target_dim_y']
        return

    def _load(self):
        if (not self.path.exists()):
            print('Unable to find config file... You may need to create one first...')
            try:
                self.create()
                self._load()
            except:
                raise RuntimeError('Failure occurred while attempting to create the config file. Aborting')
        with open(self.path, 'rt') as read:
            return json.loads(read.read())

    def _write(self):
        with open(self.path, 'wt') as write:
            write.write(json.dumps({
                'camera_coords': self.camera_pos,
                'target_dim_x': self.target_x,
                'target_dim_y': self.target_y
            }, indent=2))
            print(f'Successfully saved config data to {str(self.path.absolute())}')
        return

    def create(self):
        cam_x1 = int(input('Upper-left X coordinate of the webcam: '))
        cam_y1 = int(input('Upper-left Y coordinate of the webcam: '))
        cam_x3 = int(input('Lower-right X coordinate of the webcam: '))
        cam_y3 = int(input('Lower-right Y coordinate of the webcam: '))
        resolution = input('Resolution to output shorts at, formatted like "1080x1920"\nWill default to 1080x1920. ')
        if (resolution == ''):
            resolution = '1080x1920'
        resolution = resolution.lower().split('x')
        self.camera_pos = (cam_x1, cam_y1, cam_x3, cam_y3)
        self.target_x = int(resolution[0])
        self.target_y = int(resolution[1])
        self._write()
        return