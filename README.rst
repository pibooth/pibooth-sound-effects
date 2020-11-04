
=====================
pibooth-sound-effects
=====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-sound-effects`` is a plugin for the `pibooth <https://github.com/pibooth/pibooth>`_
application.

It adds sound effects to the application:

- When pressing on the first menu --> click
- When selecting a layout --> click
- During the countdown --> countdown
- When entering the "thank you" menu --> applause

Sounds can be customized (see below).

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

.. note:: Edit the configuration by running the command ``pibooth --config``.

Customize sounds
----------------

Sounds file shall be ``.wav`` and have the name of the state in which it shall be played.
For example the sound to play at the ``print`` state will be named ``print.wav``.

Each sound is played once, when entering the corresponding state.

Custom sounds can be added by adding or replacing existing sound files of the sounds folder
(by default ``~/.config/pibooth/sounds``) with custom ones.

Specific features
^^^^^^^^^^^^^^^^^
In addition to the standard states, other sound files are accepted:

- ``wait`` state: if you want to play a sound in loop, name it ``wait_loop.wav``
- ``preview`` state:
 
  - if you have a preview sound (``preview.wav`` file), then it will play when entering the state,
  - if you want to play the same sound for each time of the countdown, name it as ``preview_countdown.wav``,
  - if you want to play different sounds for each time of the countdown, simply add corresponding files in the sound folder (e.g.: ``3.wav``, ``2.wav``, ``1.wav``)

   .. note::  These specific sounds are cutted to be 1 second long, and if some are missing, it will be replaced either by ``preview_countdown.wav`` (if it exists) or one second of silence.

.. |PythonVersions| image:: https://img.shields.io/badge/python-2.7+ / 3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 2.7+/3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-sound-effects.svg
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-sound-effects?color=purple
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi downloads
