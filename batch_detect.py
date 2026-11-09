"""Vision track: run the detector on every test photo and build the results table.

Photos must be named <object>_<n>.jpg, e.g. keys_1.jpg (capture.py does this).
.jpg / .jpeg / .png are accepted in any letter case. iPhone HEIC photos must be
converted to JPEG first (Finder: right-click > Quick Actions > Convert Image).
Usage:  python batch_detect.py
Output: data/vision_results.csv  +  annotated images in test_photos/results/
"""
import csv, glob, os
from collections import defaultdict
import cv2
from config import OBJECTS

CONF = 0.05          # low on purpose: we want to see weak detections too
PASS = 0.25          # same as DETECT_CONFIDENCE: what Sanad would really accept


def expected_object(path):
    base = os.path.splitext(os.path.basename(path))[0]
    return base.rsplit("_", 1)[0]


IMAGE_EXT = (".jpg", ".jpeg", ".png")


def main(detector=None):
    if detector is None:
        from detector import ObjectDetector
        detector = ObjectDetector()
    os.makedirs("data", exist_ok=True)
    os.makedirs("test_photos/results", exist_ok=True)
    rows, summary = [], defaultdict(lambda: [0, 0])
    if not os.path.isdir("test_photos"):
        print("Folder test_photos not found. Run this from the Sanad_2026 folder.")
        return
    files = sorted(f for f in glob.glob("test_photos/*") if os.path.isfile(f))
    if not files:
        print("test_photos is empty. Put your photos inside it first.")
        return
    skipped = []
    for path in files:
        name = os.path.basename(path)
        if name.startswith("."):
            continue                                   # hidden files like .DS_Store
        ext = os.path.splitext(name)[1].lower()
        if ext in (".heic", ".heif"):
            skipped.append((name, "HEIC photo: convert it to JPEG first")); continue
        if ext not in IMAGE_EXT:
            skipped.append((name, "not a photo")); continue
        obj = expected_object(path).lower()
        if obj not in OBJECTS:
            skipped.append((name, f"name must start with one of: {', '.join(OBJECTS)}")); continue
        img = cv2.imread(path)
        if img is None:
            skipped.append((name, "cannot open this image")); continue
        found = detector.detect(img, conf=CONF)
        own = [d["confidence"] for d in found if d["object"] == obj]
        best = round(max(own), 2) if own else 0.0
        others = sorted({d["object"] for d in found if d["object"] != obj and d["confidence"] >= PASS})
        passed = best >= PASS
        rows.append([name, obj, "yes" if passed else "no", best, " ".join(others)])
        summary[obj][0] += passed
        summary[obj][1] += 1
        if hasattr(detector, "model"):                 # save the photo with boxes drawn
            r = detector.model.predict(img, conf=PASS, verbose=False)[0]
            cv2.imwrite(f"test_photos/results/{name}", r.plot())
    with open("data/vision_results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["photo", "object", "found", "confidence", "other_objects_seen"])
        w.writerows(rows)
    print(f"\n{'object':10s} found   result")
    for obj in OBJECTS:
        if obj in summary:
            ok, n = summary[obj]
            print(f"{obj:10s} {ok}/{n}     {'PASS' if ok >= 3 * n / 5 else 'WEAK - try another prompt'}")
    if skipped:
        print(f"\nSkipped {len(skipped)} file(s):")
        for name, why in skipped:
            print(f"  {name:25s} {why}")
    if rows:
        print("\nDetails saved in data/vision_results.csv")
    else:
        print("\nNo photos were tested. Fix the names above and run again.")


if __name__ == "__main__":
    main()
