"""Event trigger: decide WHEN to look (only when something changes)."""
import time
import cv2
from config import MOTION_THRESHOLD, MOTION_COOLDOWN_S, PERIODIC_CHECK_S


class MotionTrigger:
    def __init__(self, threshold=MOTION_THRESHOLD, cooldown=MOTION_COOLDOWN_S,
                 periodic=PERIODIC_CHECK_S):
        self.threshold, self.cooldown, self.periodic = threshold, cooldown, periodic
        self.prev = None
        self.last_fire = float("-inf")    # so the very first frame is checked

    def _prep(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (320, 240))
        return cv2.GaussianBlur(gray, (21, 21), 0)

    def changed_fraction(self, frame) -> float:
        cur = self._prep(frame)
        if self.prev is None:
            self.prev = cur
            return 1.0                      # first frame: treat as a change
        diff = cv2.absdiff(self.prev, cur)
        self.prev = cur
        _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        return cv2.countNonZero(mask) / mask.size

    def should_capture(self, frame, now=None) -> bool:
        now = time.time() if now is None else now
        moved = self.changed_fraction(frame) >= self.threshold
        due = (now - self.last_fire) >= self.periodic
        if (moved and now - self.last_fire >= self.cooldown) or due:
            self.last_fire = now
            return True
        return False
