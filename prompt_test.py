"""Vision track: compare different English descriptions (prompts) for one object.

Usage:  python prompt_test.py keys "keys" "bunch of keys" "car keys" "key ring"
Shows the average best confidence of each prompt over all photos of that object.
"""
import glob, sys
import cv2
from ultralytics import YOLOWorld

obj, prompts = sys.argv[1], sys.argv[2:]
photos = sorted(glob.glob(f"test_photos/{obj}_*.jpg"))
if not photos:
    sys.exit(f"No photos found: test_photos/{obj}_*.jpg")
model = YOLOWorld("yolov8s-worldv2.pt")
images = [cv2.imread(p) for p in photos]
print(f"{len(photos)} photos of '{obj}'\n")
for p in prompts:
    model.set_classes([p])
    scores = []
    for img in images:
        r = model.predict(img, conf=0.05, verbose=False)[0]
        scores.append(max([float(b.conf[0]) for b in r.boxes], default=0.0))
    found = sum(s >= 0.25 for s in scores)
    print(f"{p:25s} average {sum(scores)/len(scores):.2f}   found {found}/{len(scores)}")
