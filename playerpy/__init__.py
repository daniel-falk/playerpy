#!/usr/bin/env python3

import sys
from vi3o import Video

from playerpy.version import __version__
from playerpy.player import Player


def play(path, start_frame=0, replay=True):
    video = Video(path)
    p = Player(video, replay=replay)
    p.move(start_frame)
    p.play()


def play_cmd():
    if sys.argv[1] == "--version":
        print("Playerpy version: %s" % __version__)
        return
    play(sys.argv[1])


if __name__ == "__main__":
    play_cmd()
