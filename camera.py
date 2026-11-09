"""Open the camera and read frames."""
import cv2
from config import CAMERA_SOURCE


def open_camera(source=CAMERA_SOURCE):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {source!r}. Check CAMERA_SOURCE in config.py")
    return cap


if __name__ == "__main__":
    # Step 2 test: show the live picture. Press q to quit.
    cap = open_camera()
    while True:
        ok, frame = cap.read()
        if not ok:
            print("No frame received"); break
        cv2.imshow("Sanad camera test", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release(); cv2.destroyAllWindows()
