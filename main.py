import mido
import sys
import random
from midi_export import grid_to_midi

DRUM_NAMES = {
    36: "kick",
    37: "snare",
    38: "hat"
}

NOTE_MAP = {
    "kick": 36,
    "snare": 37,
    "hat": 38
}

BARS = 2
BEATS_PER_BAR = 4
STEPS_PER_BEAT = 4
STEPS_PER_BAR = BEATS_PER_BAR * STEPS_PER_BEAT
TOTAL_STEPS = BARS * STEPS_PER_BAR






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
        "kick": [0] * TOTAL_STEPS,
        "snare": [0] * TOTAL_STEPS,
        "hat": [0] * TOTAL_STEPS
    }

    total_beats = BARS * BEATS_PER_BAR

    for e in events:
        beat_time = e["time"] % total_beats

        step = round(beat_time * STEPS_PER_BEAT)

        if step >= TOTAL_STEPS:
            step = step % TOTAL_STEPS

        drum = e["drum"]
        grid[drum][step] = 1

    return grid

def maybe_add_note(pattern, step, chance):
    if random.random() < chance:
        pattern[step] = 1






def randomize_trap(grid):
    new_grid = {
        "kick": grid["kick"].copy(),
        "snare": grid["snare"].copy(),
        "hat": grid["hat"].copy()
    }

    steps_per_16th = STEPS_PER_BEAT // 4

    for bar in range(BARS):
        bar_start = bar * STEPS_PER_BAR

        # genre-safe extra kick spots
        kick_spots_16th = [4, 7, 10, 11, 12, 15]
        for spot in kick_spots_16th:
            step = bar_start + spot * steps_per_16th
            maybe_add_note(new_grid["kick"], step, 0.25)

        # light ghost snare/clap before beat 4 or end of bar
        snare_spots_16th = [12, 16]
        for spot in snare_spots_16th:
            step = bar_start + (spot - 1) * steps_per_16th
            maybe_add_note(new_grid["snare"], step, 0.15)

        # hat roll zones: late in phrases
        roll_start = bar_start + 14 * steps_per_16th
        roll_end = bar_start + 16 * steps_per_16th

        if random.random() < 0.35:
            for step in range(roll_start, min(roll_end, TOTAL_STEPS), 2):
                new_grid["hat"][step] = 1

    return new_grid







style = sys.argv[1] if len(sys.argv) > 1 else "lofi"

if style not in ["lofi", "trap", "house"]:
    print("Invalid style. Choose: lofi, trap, or house")
    exit()

path = f"templates/{style}.mid"
events = load_template(path)
grid = events_to_grid(events)




if style == "trap":
    grid = randomize_trap(grid)




print(f"Loaded {style} template as grid:\n")

for drum, pattern in grid.items():
    active_steps = [i for i, val in enumerate(pattern) if val == 1]
    print(drum.ljust(6), active_steps[:50])

output_file = f"{style}_generated.mid"

grid_to_midi(
    grid,
    output_file,
    NOTE_MAP,
    STEPS_PER_BEAT,
    bpm=140
)

print(f"\nExported MIDI file: {output_file}")