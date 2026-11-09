"""Sanad's eyes: watch the camera and log where objects are seen.

Run:  python watcher.py
"""
import time
import cv2
from camera import open_camera
from motion import MotionTrigger
from memory import Memory


def run(detector, rooms, memory, frames, show=False):
    """frames: any iterable of BGR images (camera or test images)."""
    trigger = MotionTrigger()
    for frame in frames:
        if not trigger.should_capture(frame):
            continue
        detections = detector.detect(frame)
        if not detections:
            continue
        room, score = rooms.predict(frame)
        for d in detections:
            memory.add(d["object"], room, d["confidence"])
            print(f"[{time.strftime('%H:%M:%S')}] {d['object']} in {room} "
                  f"(object {d['confidence']:.2f}, room {score:.2f})")
        if show:
            cv2.imshow("Sanad", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


def camera_frames(cap):
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        yield frame


if __name__ == "__main__":
    from detector import ObjectDetector
    from rooms import RoomRecognizer
    cap = open_camera()
    try:
        run(ObjectDetector(), RoomRecognizer(), Memory(), camera_frames(cap), show=True)
    finally:
        cap.release(); cv2.destroyAllWindows()
