"""Sanad's voice: answer "where is my ...?" questions from the memory log.

Run:  python assistant.py          (voice: press Enter, then speak)
      python assistant.py --text   (type the question - for testing)
"""
import sys
from arabic import find_object
from answer import compose
from memory import Memory


def answer_question(question, memory):
    obj = find_object(question)
    record = memory.last_seen(obj) if obj else None
    return compose(obj, record)


if __name__ == "__main__":
    text_mode = "--text" in sys.argv
    memory = Memory()
    if not text_mode:
        import voice
    while True:
        if text_mode:
            q = input("سؤالك (اكتب خروج للإنهاء): ").strip()
        else:
            input("اضغط Enter ثم اسأل سند...")
            q = voice.transcribe(voice.record())
            print("سمعت:", q)
        if q in ("خروج", "exit"):
            break
        reply = answer_question(q, memory)
        print("سند:", reply)
        if not text_mode:
            voice.speak(reply)
