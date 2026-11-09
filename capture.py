"""Vision track: take test photos of one object.

Usage:  python capture.py keys        (takes 5 photos: keys_1.jpg ... keys_5.jpg)
        python capture.py keys 3      (takes 3 photos)
Between photos, move the object to a new place / light / distance.
"""
import os, sys, time
import cv2
from camera import open_camera
from config import OBJECTS

name = sys.argv[1]
count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
if name not in OBJECTS:
    sys.exit(f"Unknown object '{name}'. Use one of: {', '.join(OBJECTS)}")

os.makedirs("test_photos", exist_ok=True)
cap = open_camera()
time.sleep(2)                                   # let the camera adjust to the light
for i in range(1, count + 1):
    input(f"[{i}/{count}] Place the {name}, then press Enter...")
    for _ in range(10):                         # skip old frames
        cap.read()
    ok, frame = cap.read()
    path = f"test_photos/{name}_{i}.jpg"
    if ok:
        cv2.imwrite(path, frame)
        print("   saved", path)
    else:
        print("   camera error, try again")
cap.release()
