# playerpy - Simple and extendable video player using python

A simple video player for Linux with quick key-bindings for play, reverse,
single frame step forward and backwards, goto frame number, save frame etc.
The player class is easily extendible for other projects, e.g. data annotation
tools.

# How to install
You can install playerpy directly from pypi with pip:
```bash
pip install playerpy
```

Thats it! You can also clone the git repo and install from source:

```bash
git clone https://github.com/daniel-falk/playerpy.git
pip install playerpy/
```

If you get into dependency problems, make sure you have the following installed:
```bash
sudo apt-get install libjpeg62-turbo-dev libavcodec-dev libswscale-dev libffi-dev
```

# How to use

## To run from command line:
```bash
playerpy <VIDEO FILE PATH>
```

## To run from a script
```python
from playerpy import play
play(<VIDEO FILE PATH>)  # string or pathlib.Path
```

## Key bindinigs
* SPACE - pause/play
* ENTER - step single frame in paused mode
* g -> [0-9]+ -> ENTER - jump to frame number
* RIGHT ARROW - increase speed
* LEFT ARROW - decrease speed
* r - reverse playback speed
* s - save current frame to disk as JPG


## Example view

Frame number is seen in top of video. Cursor position and pixel intensities are seen in the window footer.
![example view](https://github.com/daniel-falk/playerpy/blob/images/images/playerpy.png "Example view of window: Surveillance view credits to https://viratdata.org/")

# How to subclass

todo

# Todo

- [ ] Add footer showing total number of frames
- [ ] Better readme
- [x] Upload release to pypi to make "pip installable"
