import mido
import sys

DRUM_NAMES = {
    36: "kick",
    37: "snare",
    38: "hat"
}
STEPS_PER_BAR = 16
BEATS_PER_BAR = 4

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

def events_to_grid(events):
    grid = {
        "kick": [0] * STEPS_PER_BAR,
        "snare": [0] * STEPS_PER_BAR,
        "hat": [0] * STEPS_PER_BAR
    }

    for e in events:
        beat_time = e["time"] % BEATS_PER_BAR

        step = round(beat_time / BEATS_PER_BAR * STEPS_PER_BAR)

        if step == STEPS_PER_BAR:
            step = 0

        drum = e["drum"]
        grid[drum][step] = 1

    return grid

style = sys.argv[1] if len(sys.argv) > 1 else "lofi"

if style not in ["lofi", "trap", "house"]:
    print("Invalid style. Choose: lofi, trap, or house")
    exit()

path = f"templates/{style}.mid"
events = load_template(path)
grid = events_to_grid(events)

print(f"Loaded {style} template as grid:\n")

for drum, pattern in grid.items():
    print(drum.ljust(6), pattern)