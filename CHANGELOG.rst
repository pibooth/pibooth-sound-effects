=========
Changelog
=========

0.1.0
-----

- Support of pibooth 2.1 and 3.0, Python 3.10 or later is now required.
- Fix ``finish.wav`` never played when entering the ``finish`` state.
- Add ``capture_delay`` option to synchronize the capture sound with the camera shutter (#11).
- Compute the countdown duration from the audio mixer settings instead of assuming 44.1 kHz.
- Regenerate the countdown sound when the preview delay is changed from the settings menu.
- Do not crash pibooth when no audio device is available or the sounds folder is missing.
- Document how to play a looping sound on the start screen (#10).
- Publish on PyPI using trusted publishing when a GitHub release is created.

0.0.4
-----

- Drop Python 2.7 support.
- Remove sounds folder on ``pibooth --reset``.
- Fix looping sounds never stopped.
- Countdown sounds and generic looping sounds for all states.
