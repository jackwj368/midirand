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

DEFAULT_BARS = 4
BEATS_PER_BAR = 4
STEPS_PER_BEAT = 4
# STEPS_PER_BAR = BEATS_PER_BAR * STEPS_PER_BEAT
# TOTAL_STEPS = BARS * STEPS_PER_BAR






def load_template(path):
    mid = mido.MidiFile(path)
    events = []

    ticks_per_beat = mid.ticks_per_beat

    for track in mid.tracks:
        tick_accum = 0

        for msg in track:
            tick_accum += msg.time

            if msg.type == "note_on" and msg.velocity > 0:
                if msg.note in DRUM_NAMES:
                    beat_time = tick_accum / ticks_per_beat

                    events.append({
                        "time": beat_time,
                        "note": msg.note,
                        "velocity": msg.velocity,
                        "drum": DRUM_NAMES[msg.note],
                    })

    events.sort(key=lambda e: e["time"])

    return events

def events_to_grid(events, bars, total_steps):
    grid = {
        "kick": [0] * total_steps,
        "snare": [0] * total_steps,
        "hat": [0] * total_steps
    }

    template_length_beats = max(e["time"] for e in events)
    template_bars = max(1, round(template_length_beats / BEATS_PER_BAR))

    total_beats = bars * BEATS_PER_BAR

    for repeat_bar in range(0, bars, template_bars):
        repeat_offset_beats = repeat_bar * BEATS_PER_BAR

        for e in events:
            beat_time = e["time"] + repeat_offset_beats

            if beat_time >= total_beats:
                continue

            step = round(beat_time * STEPS_PER_BEAT)

            if step >= total_steps:
                continue

            drum = e["drum"]
            grid[drum][step] = 1

    return grid

def combine_temp_and_max(temp_grid, max_grid, level):
    final_grid = {
        "kick": temp_grid["kick"].copy(),
        "snare": temp_grid["snare"].copy(),
        "hat": temp_grid["hat"].copy()
    }

    level_chances = {
        "simple": 0.05,
        "spicy": 0.18,
        "chaos": 0.4
    }

    chance = level_chances[level]

    for drum in final_grid:
        for step in range(len(final_grid[drum])):
            note_is_required = temp_grid[drum][step] == 1
            note_is_allowed = max_grid[drum][step] == 1

            if note_is_allowed and not note_is_required:
                if random.random() < chance:
                    final_grid[drum][step] = 1

    return final_grid







VALID_STYLES = ["lofi", "trap", "house"]
VALID_BAR_LENGTHS = [2, 4, 8]
VALID_LEVELS = ["simple", "spicy", "chaos"]

style = input("Choose a genre (lofi, trap, house): ").lower().strip()

if style not in VALID_STYLES:
    print("Choose a correct genre")
    exit()

try:
    bars = int(input("Choose pattern length in bars (2, 4, 8): ").strip())
except ValueError:
    print("Choose a valid pattern length")
    exit()

if bars not in VALID_BAR_LENGTHS:
    print("Choose a valid pattern length")
    exit()

level = input("Choose variation level (simple, spicy, chaos): ").lower().strip()

if level not in VALID_LEVELS:
    print("Choose a valid variation level")
    exit()

STEPS_PER_BAR = BEATS_PER_BAR * STEPS_PER_BEAT
TOTAL_STEPS = bars * STEPS_PER_BAR

if style not in ["lofi", "trap", "house"]:
    print("Invalid style. Choose: lofi, trap, or house")
    exit()

temp_path = f"templates/{style}_temp.mid"
max_path = f"templates/{style}_max.mid"

temp_events = load_template(temp_path)
max_events = load_template(max_path)

temp_grid = events_to_grid(temp_events, bars, TOTAL_STEPS)
max_grid = events_to_grid(max_events, bars, TOTAL_STEPS)

grid = combine_temp_and_max(temp_grid, max_grid, level)




# if style == "trap":
#     grid = randomize_trap(grid, bars, level)




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