import mido

def grid_to_midi(grid, output_path, note_map, steps_per_beat, bpm=140):
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    ticks_per_beat = mid.ticks_per_beat
    ticks_per_step = ticks_per_beat // steps_per_beat

    tempo = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage("set_tempo", tempo=tempo, time=0))

    note_events = []

    for drum, pattern in grid.items():
        for step, is_active in enumerate(pattern):
            if is_active:
                note = note_map[drum]

                # note_on at this step
                note_events.append((step, "on", note))

                # note_off slightly later
                note_events.append((step + 1, "off", note))

    # Sort by step. If same step, note_off before note_on is safer.
    note_events.sort(key=lambda x: (x[0], 0 if x[1] == "off" else 1))

    last_step = 0

    for step, event_type, note in note_events:
        delta_steps = step - last_step
        delta_ticks = delta_steps * ticks_per_step

        if event_type == "on":
            msg = mido.Message(
                "note_on",
                note=note,
                velocity=100,
                time=delta_ticks
            )
        else:
            msg = mido.Message(
                "note_off",
                note=note,
                velocity=0,
                time=delta_ticks
            )

        track.append(msg)
        last_step = step

    mid.save(output_path)