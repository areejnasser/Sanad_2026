"""Sanad - central settings. Edit this file first."""

# Camera: 0 = laptop webcam. For a phone used as a webcam (DroidCam / Iriun),
# try 1 or 2. For the "IP Webcam" Android app use its URL, e.g.
# "http://192.168.1.20:8080/video"
CAMERA_SOURCE = 0

# Objects Sanad looks for.
#   prompt   : English text given to the detector (YOLO-World understands text)
#   ar       : how Sanad says the object in answers
#   keywords : Arabic stems the user may say (after normalisation, see arabic.py)
OBJECTS = {
    "glasses": {"prompt": "eyeglasses", "ar": "نظارتك",
                "keywords": ["نظاره", "نظارت", "نظارات"]},
    "keys":    {"prompt": "keys",       "ar": "مفاتيحك",
                "keywords": ["مفتاح", "مفاتيح"]},
    "phone":   {"prompt": "cell phone", "ar": "جوالك",
                "keywords": ["جوال", "تلفون", "موبايل", "هاتف"]},
    "wallet":  {"prompt": "wallet",     "ar": "محفظتك",
                "keywords": ["محفظ", "بوك"]},
    "remote":  {"prompt": "remote control", "ar": "الريموت",
                "keywords": ["ريموت", "جهاز التحكم"]},
    "medicine":{"prompt": "medicine box", "ar": "علبة الدواء",
                "keywords": ["دوا", "علاج", "حبوب"]},
    "cup":     {"prompt": "cup",        "ar": "كوبك",
                "keywords": ["كوب", "كاس", "فنجان"]},
    "bag":     {"prompt": "handbag",    "ar": "شنطتك",
                "keywords": ["شنط"]},
    "watch":   {"prompt": "wristwatch", "ar": "ساعتك",
                "keywords": ["ساعتي", "ساعه اليد"]},
    "cane":    {"prompt": "walking cane", "ar": "عصاك",
                "keywords": ["عصا", "عكاز"]},
}

# Room names (Arabic, as Sanad will say them). Filled during the home tour.
ROOMS = ["الصالة", "المطبخ", "غرفة النوم", "الحمام", "المدخل"]

# Detection
DETECT_CONFIDENCE = 0.25      # ignore detections below this
LOW_CONFIDENCE = 0.45         # below this, Sanad says it is "not sure"

# Event trigger
MOTION_THRESHOLD = 0.02       # fraction of pixels that must change (2%)
MOTION_COOLDOWN_S = 3         # seconds between two triggered captures
PERIODIC_CHECK_S = 60         # also check once a minute even without motion

# Room recognition
ROOM_MIN_SIMILARITY = 0.75    # below this the room is "unknown"

# Storage
DB_PATH = "data/sanad.db"
SAVE_IMAGES = False           # privacy: keep text only (see design rationale)
