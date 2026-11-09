"""Step 11: record test results and compute the success rate.

Usage: python evaluate.py add glasses المطبخ المطبخ 3.2
       (object, true room, room Sanad said, response seconds)
       python evaluate.py report
"""
import csv, os, sys
FILE = "data/test_results.csv"

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    if sys.argv[1] == "add":
        obj, true_room, said_room, secs = sys.argv[2:6]
        new = not os.path.exists(FILE)
        with open(FILE, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["object", "true_room", "sanad_room", "correct", "seconds"])
            w.writerow([obj, true_room, said_room, int(true_room == said_room), secs])
    else:
        rows = list(csv.DictReader(open(FILE, encoding="utf-8")))
        ok = sum(int(r["correct"]) for r in rows)
        avg = sum(float(r["seconds"]) for r in rows) / len(rows)
        print(f"Correct: {ok}/{len(rows)} = {100*ok/len(rows):.0f}%   Average response: {avg:.1f} s")
