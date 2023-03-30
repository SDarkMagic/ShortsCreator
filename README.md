# Shorts Creator

## About - What is this project?

This project aims to create a relatively simple command line tool to automate the process of cutting and formatting Youtube shorts from stream VODs.


## Setup

Run `pipenv install` in the project directory. After doing so, all the necessary dependencies should be setup in the project's virtual environment.
Next, you will need to know the top left and lower right corner coordinates of your webcam with respect to the video resolution you record at. For example, if my
web cam is located in the lower right corner of my video, and my video has a resolution of 1920x1080, I would use (1570, 810), (1920, 1080) as my bounding coordinates.
Remember these positions, You **WILL** need them later.

For your first time running the program, you will be guided through some initial setup prompts. For each one, simply input the desired value and press enter. The program assumes
the coordinates will be in the first quadrant of a cartesian coordinate system representing the screen with the bottom left of the screen being the origin (0, 0)


## Usage

To run the program, use the command `pipenv run python src/__main__.py <start timestamp> <clip duration>` in this project's directory. Start timestamp **must** be formatted
in the form of "HH:MM:SS.mmmm" A value of 0 is assumed for any non-specified values reading from left to right. The desired duration must be a value formatted as "SS.mmmm"
representing the length of the clip, in seconds and milliseconds. This value will be added to the start timestamp and used to calculate the end timestamp of the clip.

Additionally, when running the command, an optional `-o` flag may be specified followed by an output path for the generated short. If none is provided, the new short will
simply be saved at the exact same location as the original video file with "edited_short" added to the filename.
