"""Room recognition with CLIP image embeddings.

Home tour: take ~10 photos of each room from different angles and save them in
data/tour/<room name>/. Then run:  python rooms.py build
Sanad compares each new frame with these photos and picks the closest room.
"""
import os
import numpy as np
from PIL import Image
from config import ROOM_MIN_SIMILARITY

TOUR_DIR = "data/tour"
EMB_FILE = "data/room_embeddings.npz"


class RoomRecognizer:
    def __init__(self):
        import torch, open_clip
        self.torch = torch
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="laion2b_s34b_b79k")
        self.model.eval()
        self.rooms, self.embs = None, None
        if os.path.exists(EMB_FILE):
            data = np.load(EMB_FILE, allow_pickle=True)
            self.rooms, self.embs = list(data["rooms"]), data["embs"]

    def embed(self, pil_image):
        with self.torch.no_grad():
            x = self.preprocess(pil_image).unsqueeze(0)
            e = self.model.encode_image(x)
            e = e / e.norm(dim=-1, keepdim=True)
        return e[0].numpy()

    def build(self):
        rooms, embs = [], []
        for room in sorted(os.listdir(TOUR_DIR)):
            folder = os.path.join(TOUR_DIR, room)
            for f in os.listdir(folder):
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    rooms.append(room)
                    embs.append(self.embed(Image.open(os.path.join(folder, f)).convert("RGB")))
        np.savez(EMB_FILE, rooms=np.array(rooms), embs=np.stack(embs))
        self.rooms, self.embs = rooms, np.stack(embs)
        print(f"Saved {len(rooms)} tour photos for {len(set(rooms))} rooms")

    def predict(self, frame_bgr):
        """Return (room, similarity). Room is 'unknown' if nothing is close enough."""
        rgb = Image.fromarray(frame_bgr[:, :, ::-1])
        sims = self.embs @ self.embed(rgb)
        best = int(np.argmax(sims))
        room, score = self.rooms[best], float(sims[best])
        return (room if score >= ROOM_MIN_SIMILARITY else "unknown"), score


if __name__ == "__main__":
    import sys
    rr = RoomRecognizer()
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        rr.build()
    else:  # python rooms.py photo.jpg
        import cv2
        print(rr.predict(cv2.imread(sys.argv[1])))
