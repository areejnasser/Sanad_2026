"""Object detection with YOLO-World (open-vocabulary: classes are given as text)."""
from config import OBJECTS, DETECT_CONFIDENCE


class ObjectDetector:
    def __init__(self, weights="yolov8s-worldv2.pt"):
        from ultralytics import YOLOWorld          # imported here so other steps run without it
        self.model = YOLOWorld(weights)            # downloads the weights the first time
        self.keys = list(OBJECTS)
        self.model.set_classes([OBJECTS[k]["prompt"] for k in self.keys])

    def detect(self, frame, conf=DETECT_CONFIDENCE):
        """Return a list of {"object", "confidence", "box"} for one frame."""
        result = self.model.predict(frame, conf=conf, verbose=False)[0]
        found = []
        for box in result.boxes:
            idx = int(box.cls[0])
            found.append({"object": self.keys[idx],
                          "confidence": float(box.conf[0]),
                          "box": [round(v) for v in box.xyxy[0].tolist()]})
        return found


if __name__ == "__main__":
    # Step 3 test: python detector.py photo.jpg
    import sys, cv2
    det = ObjectDetector()
    img = cv2.imread(sys.argv[1])
    for d in det.detect(img):
        print(d)
