# Sanad - starter code (Phase 0: "Where are my keys?")

Follow the guide "Sanad_Phase0_Practical_Guide.docx" step by step.

| File | Step | What it does |
|---|---|---|
| config.py | all | Settings: camera, objects, rooms, thresholds |
| camera.py | 2 | Opens the camera (`python camera.py` shows a live view) |
| detector.py | 3 | Finds objects with YOLO-World (`python detector.py photo.jpg`) |
| rooms.py | 4 | Recognises the room from the home-tour photos (`python rooms.py build`) |
| motion.py | 5 | Decides when to look (only when something changes) |
| memory.py | 6 | SQLite memory log: object, room, time |
| voice.py | 7, 9 | Records, transcribes (Arabic) and speaks |
| arabic.py | 8 | Normalises Arabic and finds the object in the question |
| answer.py | 9 | Builds the short Arabic answer |
| watcher.py | 10 | Camera -> detect -> room -> log (Sanad's eyes) |
| assistant.py | 10 | Question -> answer (Sanad's voice). `--text` to type instead of speak |
| evaluate.py | 11 | Records test results and prints the success rate |

Quick start:
    python -m venv .venv
    .venv\Scripts\activate          (Windows)   |   source .venv/bin/activate  (Mac)
    pip install -r requirements.txt
    python camera.py
