import mido
import sys

DRUM_NAMES = {
    36: "kick",
    37: "snare",
    38: "hat"
}

def load_template(path):
    mid = mido.MidiFile(path)
    events = []

    time_accum = 0

    for msg in mid:
        time_accum += msg.time

        if msg.type == "note_on" and msg.velocity > 0:
            if msg.note in DRUM_NAMES:
                events.append({
                    "time": time_accum,
                    "note": msg.note,
                    "velocity": msg.velocity,
                    "drum": DRUM_NAMES[msg.note],
                })

    return events

style = sys.argv[1] if len(sys.argv) > 1 else "lofi"

if style not in ["lofi", "trap", "house"]:
    print("Invalid style. Choose: lofi, trap, or house")
    exit()

path = f"templates/{style}.mid"
events = load_template(path)

print(f"Loaded {style} template")
print("First 10 events:")

for e in events[:10]:
    print(e)