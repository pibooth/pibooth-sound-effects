
====================
pibooth-sound-effects
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-sound-effects`` is a plugin for the `pibooth <https://github.com/pibooth/pibooth>`_
application.

It adds sound effects to the application:

Install
-------

::

    $ pip3 install pibooth-sound-effects

Configuration
-------------

This is the extra configuration options that can be added in the ``pibooth``
configuration:

.. code-block:: ini

    [SOUNDS]

    PATH TO THE SOUNDS FOLDER
    sounds_path = ~/.config/pibooth/sounds

.. note:: Edit the configuration by running the command ``pibooth --config``.

.. |PythonVersions| image:: https://img.shields.io/badge/python-2.7+ / 3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 2.7+/3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-sound-effects.svg
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-sound-effects?color=purple
   :target: https://pypi.org/project/pibooth-sound-effects
   :alt: PyPi downloads
