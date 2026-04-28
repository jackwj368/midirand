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

def maybe_add_note(pattern, step, chance):
    if random.random() < chance:
        pattern[step] = 1

def get_variation_settings(level):
    if level == "simple":
        return {
            "kick_chance": 0.03,
            "snare_chance": 0.02,
            "hat_chance": 0.06,
            "roll_chance": 0.03
        }

    if level == "spicy":
        return {
            "kick_chance": 0.08,
            "snare_chance": 0.04,
            "hat_chance": 0.12,
            "roll_chance": 0.08
        }

    if level == "chaos":
        return {
            "kick_chance": 0.14,
            "snare_chance": 0.08,
            "hat_chance": 0.20,
            "roll_chance": 0.15
        }





def randomize_trap(grid, bars, level):
    new_grid = {
        "kick": grid["kick"].copy(),
        "snare": grid["snare"].copy(),
        "hat": grid["hat"].copy()
    }

    settings = get_variation_settings(level)

    steps_per_16th = STEPS_PER_BEAT // 4

    for bar in range(bars):
        bar_start = bar * STEPS_PER_BAR

        # --- KICKS ---
        kick_spots_16th = [4, 7, 10, 11, 12, 15]
        for spot in kick_spots_16th:
            step = bar_start + spot * steps_per_16th
            if step < len(new_grid["kick"]):
                maybe_add_note(new_grid["kick"], step, settings["kick_chance"])

        # --- SNARES / CLAPS ---
        if bar % 2 == 1:
            snare_spots_16th = [12, 16]
        else:
            snare_spots_16th = [16]

        for spot in snare_spots_16th:
            step = bar_start + (spot - 1) * steps_per_16th
            if step < len(new_grid["snare"]):
                maybe_add_note(new_grid["snare"], step, settings["snare_chance"])

        # --- HI-HATS (16th fills) ---
        hat_spots = [1, 3, 5, 7, 9, 11, 13, 15]
        for spot in hat_spots:
            step = bar_start + spot
            if step < len(new_grid["hat"]):
                maybe_add_note(new_grid["hat"], step, settings["hat_chance"])

        # --- HI-HAT ROLLS ---
        roll_start = bar_start + 14 * steps_per_16th
        roll_end = bar_start + 16 * steps_per_16th

        if random.random() < settings["roll_chance"]:
            for step in range(roll_start, min(roll_end, TOTAL_STEPS), 2):
                new_grid["hat"][step] = 1

    return new_grid







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

path = f"templates/{style}.mid"
events = load_template(path)
grid = events_to_grid(events, bars, TOTAL_STEPS)




if style == "trap":
    grid = randomize_trap(grid, bars, level)




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