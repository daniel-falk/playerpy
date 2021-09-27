from vi3o.debugview import DebugViewer
from vi3o.utils import Frame
from vi3o.image import imsave
from pyglet.window import key as keysym
import numpy as np


class Player(DebugViewer):
    def __init__(self, video, replay=True, **args):
        try:
            frame = video[0]
        except (TypeError, KeyError):
            raise ValueError("Can't access frame 0 in video, is video a Video object?")
        if not isinstance(frame, (Frame, np.ndarray)):
            raise ValueError("First frame in video does not seem to be a vi3o Frame object.")

        self._replay = replay
        self._video = video
        self._index = 0
        self._update = 1
        self._paused = False
        self._len = len(video)
        self._goto_frame_parser = NumberParser(keysym.G)
        super().__init__(**args)

    def play(self):
        for frame in self._iterate():
            self.view(frame)

    def move(self, index):
        self._index = index

    def len(self):
        return self._len

    def _dispatch_events(self):
        """Override dispatch_events in DebugViewer to overwrite window name

        ...since this is called after DebugViewer sets the window name but before
        the window is rendered. This shows correct frame index and frame time.
        """
        idx = self._index
        frame = self._video[idx]
        real_time = frame.systime if hasattr(frame, "systime") else float("nan")
        rel_time = frame.timestamp if hasattr(frame, "timestamp") else float("nan")
        frame_info = "%d - %f - %f" % (idx, real_time, rel_time)
        text = "{} - {} - speed: {}".format(self.name, frame_info, self._update)
        self.window.set_caption(text)
        super()._dispatch_events()

    def on_key_press(self, key, modifiers):
        """Override parent method for key press in window
        """
        idx = self._goto_frame_parser.update(key)
        if not isinstance(idx, bool):
            self._index = idx - self._update  # Iterator will advance once
            return
        elif idx == True:
            return

        if key == keysym.R:
            self._set_update(step=-self._update)
        elif key == keysym.RIGHT:
            self._set_update(inc=1)
        elif key == keysym.LEFT:
            self._set_update(inc=-1)
        elif key == keysym.SPACE:
            self._paused = not self._paused
        elif key == keysym.ENTER:
            self._index += 1
        elif key == keysym.S:
            self._dump_frame()  # Save current frame to disk
            self._index -= self._update  # Iterator will step once
        else:
            return super().on_key_press(key, modifiers)
        DebugViewer.step_counter += 1

    def _set_update(self, inc=None, step=None):
        if inc is not None and step is not None:
            raise ValueError("Specify either inc or step, not both")
        if inc is None and step is None:
            raise ValueError("Specify either inc or step")
        if inc is None or self._paused:
            # if paused, inc from 0..
            self._update = step or inc
        else:
            self._update += inc

    def _iterate(self):
        def next_index():
            next_idx = self._index + self._update
            if not self._replay:
                return next_idx
            return next_idx % len(self._video)

        try:
            while True:
                self._index = next_index()
                yield self._video[self._index]
        except IndexError:
            pass

    def _dump_frame(self):
        frame = self._video[self._index]
        imsave(frame, "playerpy_frame_%s_%d.jpg" % (
                hash(str(self._video.filename)),
                self._index
            )
        )


class NumberParser:
    """Parse a number from key-presses
    """
    def __init__(self, start_key):
        self.start_key = start_key
        self.buffer = []
        self._goto_frame_active = False

    def update(self, key):
        """Add a number to the parsing

        Returns: False if not in the sequence,
                 True if in the sequence,
                 An integer if parsing finished
        """
        if not self._goto_frame_active:
            if key == self.start_key:
                self._goto_frame_active = True
                return True
            else:
                return False
        elif key in (keysym.ENTER, keysym.NUM_ENTER):
            buff = self._stop()
            if len(buff) == 0:
                return False
            return int("".join(map(str, buff)))
        elif self._get_num(key) is not None:
            self.buffer.append(self._get_num(key))
            return True

        self._stop()
        return False

    def _stop(self):
        buff = self.buffer
        self.buffer = []
        self._goto_frame_active = False
        return buff

    def _get_num(self, key):
        """Get integer from key
        """
        # This might use implementation defined behaviur in pyglet...
        if keysym._0 <= key <= keysym._9:
            return key - keysym._0
        if keysym.NUM_0 <= key <= keysym.NUM_9:
            return key - keysym.NUM_0
        return None


