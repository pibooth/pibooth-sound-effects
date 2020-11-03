
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
    sounds_path = sounds

.. note:: Edit the configuration by running the command ``pibooth --config``.

Customize sounds
----------------

Sounds file shall be .wav and have the name of the state in which it shall be played.
Each sound is played once, when entering the corresponding state except:

- the ``wait`` state were the sound is played in loop
- the ``preview`` state were the sound is played once for each number in the countdown

Custom sounds can be added by replacing exiting sound files of the sounds folder
(by default ``~/.config/pibooth/sounds``) with custom ones.

.. |PythonVersions| image:: https://img.shields.io/badge/python-2.7+ / 3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 2.7+/3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-sound-effects.svg
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-sound-effects?color=purple
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi downloads
