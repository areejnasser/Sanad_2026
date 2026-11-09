"""Turn a memory record into a short, clear Arabic sentence."""
from datetime import datetime
from config import OBJECTS, LOW_CONFIDENCE


def say_time(t: datetime) -> str:
    hour = t.hour % 12 or 12
    part = "صباحاً" if t.hour < 12 else "مساءً"
    if t.minute == 0:
        return f"الساعة {hour} {part}"
    return f"الساعة {hour} و {t.minute} دقيقة {part}"


def say_day(t: datetime, now: datetime) -> str:
    days = (now.date() - t.date()).days
    if days == 0:
        return "اليوم"
    if days == 1:
        return "أمس"
    return f"قبل {days} أيام"


def compose(obj_key, record, now: datetime | None = None) -> str:
    now = now or datetime.now()
    if obj_key is None:
        return "ما فهمت أي غرض تقصد. قل مثلاً: وين نظارتي؟"
    name = OBJECTS[obj_key]["ar"]
    if record is None:
        return f"ما عندي سجل عن {name}. جرّب آخر مكان تتذكره."
    room = record["room"]
    where = "في مكان ما عرفته" if room == "unknown" else f"في {room}"
    text = f"آخر مرة شفت {name} {where}، {say_day(record['seen_at'], now)} {say_time(record['seen_at'])}."
    if record["confidence"] < LOW_CONFIDENCE:
        text += " بس أنا مو متأكد تماماً."
    return text
