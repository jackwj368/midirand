import mido

DRUM_NAMES = {
    36: "kick",
    38: "snare",
    42: "hat"
}

def load_template(path):
    mid = mido.MidiFile(path)
    events = []

    time_accum = 0

    for msg in mid:
        time_accum += msg.time

        if msg.type == "note_on" and msg.velocity > 0:
            if msg.note in [36, 38, 42]:
                events.append({
                    "time": time_accum,
                    "note": msg.note,
                    "velocity": msg.velocity,
                    "drum": DRUM_NAMES[msg.note],
                })

    return events

events = load_template("templates/lofi1.mid")

print("First 10 events:")
for e in events[:10]:
    print(e)