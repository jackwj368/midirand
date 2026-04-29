Drum Midi Generator

This is a Python project that makes drum MIDI loops based on different genres. Instead of just randomly placing notes everywhere, it actually uses templates so the loops still sound musical and make sense.

Current Genres Include:

  - Trap
  
  - House

The main goal of this project was to make a MIDI generator that doesn’t sound random or bad. A lot of generators just throw notes anywhere (drum monkey), but this one makes sure everything fits the genre.

To set the project up, run:

    pip install mido python-rtmidi
  
    python main.py

You will be presented with the genre options. Type one in, then select how long you want the loop to be (2, 4, or 8 bars). Then select the extremity of the loop, with the options being simple, medium, and too much. The result is going to be a .mid file that can be dragged into any piano roll.
