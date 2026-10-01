
=====================
pibooth-sound-effects
=====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-sound-effects`` is a plugin for the `pibooth <https://github.com/pibooth/pibooth>`_
application.

It adds sound effects to the application. By default:

- When entering the layout selection --> click (``choose.wav``)
- When a layout is selected --> click (``chosen.wav``)
- During the countdown --> beep each second (``preview_countdown.wav``)
- When a picture is taken --> shutter (``capture.wav``)
- When entering the "thank you" screen --> applause (``finish.wav``)

Sounds can be customized (see below).

Requirements
------------

- `pibooth`_ 2.x
- Python 3.10 or later
- A working sound output (if no audio device is found, the plugin is disabled
  and a warning is logged)

Install
-------

::

    $ pip3 install pibooth-sound-effects

Configuration
-------------

Here below the new configuration options available in the `pibooth`_ configuration.
**The keys and their default values are automatically added to your configuration
after first** `pibooth`_ **restart.**

.. code-block:: ini

    [SOUNDS]

    # Path to the sounds folder
    sounds_path = ~/.config/pibooth/sounds

    # Delay in seconds before playing the capture sound (to synchronize it with the camera shutter)
    capture_delay = 0.0

.. note:: Edit the configuration by running the command ``pibooth --config``.

Customize sounds
----------------

Sound files shall be ``.wav`` and have the name of the state in which it shall be played (e.g. {state}.wav).
If you want to play the sound in loop, just add "_loop" in the name (e.g. {state}_loop.wav).

Available states are: ``wait``, ``choose``, ``chosen``, ``preview``, ``capture``,
``processing``, ``print`` and ``finish``.

For example at the ``print`` level:

- if it exists, the sound named ``print.wav`` will be played once, when entering the state
- if it exists, the sound named ``print_loop.wav`` will be played in loop until the state is left.

Looping sounds are stopped as soon as the state is left. For instance, a background music
can be played on the start screen with a ``wait_loop.wav`` file: it will stop when the
user presses the button to take a picture.

Custom sounds can be added by adding or replacing existing sound files of the sounds folder
(by default ``~/.config/pibooth/sounds``) with custom ones. Run ``pibooth --reset`` to restore
the default sounds.

Specific features
^^^^^^^^^^^^^^^^^
In addition to the standard ``{state}.wav`` and ``{state_loop}.wav`` states, other sound files are accepted in ``preview`` state:

- if you have a preview sound (``preview.wav`` file), then it will play when entering the state,
- if you want to play the same sound for each time of the countdown, name it as ``preview_countdown.wav``,
- if you want to play different sounds for each time of the countdown, simply add corresponding files in the sound folder (e.g.: ``3.wav``, ``2.wav``, ``1.wav``)

  .. note::  These specific sounds are cut to be 1 second long, and if some are missing, it will be replaced either by ``preview_countdown.wav`` (if it exists) or one second of silence.

Some cameras take a moment to actually shoot the picture once the capture is triggered.
In this case, use the ``capture_delay`` option to delay the ``capture.wav`` sound and
synchronize it with the camera shutter.

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.10+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.10+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-sound-effects.svg
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-sound-effects?color=purple
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi downloads
