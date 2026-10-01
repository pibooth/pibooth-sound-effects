# -*- coding: utf-8 -*-

import os
import os.path as osp
import shutil
import threading
import pygame
import pibooth
from pibooth.utils import LOGGER


def stop_delayed_sound(app):
    """Cancel the sound waiting to be played (if any).
    """
    timer = getattr(app, 'sounds_timer', None)
    if timer:
        timer.cancel()
        app.sounds_timer = None


def handle_sounds(app, state, delay=0):
    """Actions performed when application enter the defined state.
    """
    sounds = getattr(app, 'sounds', {})

    # stop delayed and looping sounds of the previous state
    stop_delayed_sound(app)
    for sound_key in sounds:
        if sound_key.endswith("_loop"):
            sounds[sound_key].stop()

    # play sound
    if state in sounds:
        if delay > 0:
            app.sounds_timer = threading.Timer(delay, sounds[state].play)
            app.sounds_timer.daemon = True
            app.sounds_timer.start()
        else:
            sounds[state].play()

    # play loop sound
    if f"{state}_loop" in sounds:
        sounds[f"{state}_loop"].play(loops=-1)


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('SOUNDS', 'sounds_path', "~/.config/pibooth/sounds",
                   "Path to the sounds folder")
    cfg.add_option('SOUNDS', 'capture_delay', 0.0,
                   "Delay in seconds before playing the capture sound (to synchronize it with the camera shutter)",
                   "Capture sound delay", [str(i / 10) for i in range(0, 21)])


@pibooth.hookimpl
def pibooth_reset(cfg, hard):
    """Populate sounds folder if it doesn't exists"""
    sound_path = cfg.getpath('SOUNDS', 'sounds_path')
    if hard and osp.isdir(sound_path):
        shutil.rmtree(sound_path, ignore_errors=True)
    if not osp.isdir(sound_path):
        source_sound_path = osp.join(osp.dirname(osp.abspath(__file__)), 'sounds')
        LOGGER.info("Generate sounds directory in '%s'", sound_path)
        shutil.copytree(source_sound_path, sound_path)


@pibooth.hookimpl
def pibooth_startup(app, cfg):
    """Init the pygame mixer and load available sounds"""
    app.sounds = {}
    app.sounds_timer = None

    sounds_path = cfg.getpath('SOUNDS', 'sounds_path')
    if not osp.isdir(sounds_path):
        LOGGER.warning("Sounds directory '%s' not found, sound effects are disabled", sounds_path)
        return

    try:
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
    except pygame.error as ex:
        LOGGER.warning("Can not initialize audio mixer (%s), sound effects are disabled", ex)
        return

    for sound in os.listdir(sounds_path):
        if sound.endswith(".wav"):
            try:
                app.sounds[sound[:-4]] = pygame.mixer.Sound(osp.join(sounds_path, sound))
            except pygame.error as ex:
                LOGGER.warning("Can not load sound '%s': %s", sound, ex)

    # Generate countdown if files are given and not preview
    if "preview" not in app.sounds:
        frequency, size, channels = pygame.mixer.get_init()
        one_second_bytes_length = frequency * channels * abs(size) // 8
        preview_delay = cfg.getint("WINDOW", "preview_delay")
        preview_sound_raw = bytes(0)
        for i in range(preview_delay, 0, -1):
            if str(i) in app.sounds:
                raw_sound = app.sounds[str(i)].get_raw()
            elif "preview_countdown" in app.sounds:
                raw_sound = app.sounds["preview_countdown"].get_raw()
            else:
                # add one second of silence in the raw signal
                raw_sound = bytes(one_second_bytes_length)

            if len(raw_sound) > one_second_bytes_length:
                # Sound too long
                raw_sound = raw_sound[:one_second_bytes_length]
            elif len(raw_sound) < one_second_bytes_length:
                # Sound too short
                raw_sound += bytes(one_second_bytes_length - len(raw_sound))
            preview_sound_raw += raw_sound

        if preview_sound_raw:
            app.sounds["preview"] = pygame.mixer.Sound(buffer=preview_sound_raw)


@pibooth.hookimpl
def pibooth_cleanup(app):
    """Quit the mixer
    """
    stop_delayed_sound(app)
    pygame.mixer.quit()

# --- Wait State ---------------------------------------------------------------


@pibooth.hookimpl
def state_wait_enter(app):
    """Actions performed when application enter in Wait state.
    """
    handle_sounds(app, "wait")

# --- Choose State -------------------------------------------------------------


@pibooth.hookimpl
def state_choose_enter(app):
    """Actions performed when application enter in Choose state.
    """
    handle_sounds(app, "choose")

# --- Chosen State -------------------------------------------------------------


@pibooth.hookimpl
def state_chosen_enter(app):
    """Actions performed when application enter in Chosen state.
    """
    handle_sounds(app, "chosen")

# --- Preview State ------------------------------------------------------------


@pibooth.hookimpl
def state_preview_enter(app):
    """Actions performed when application enter in Preview state.
    """
    handle_sounds(app, "preview")

# --- Capture State ------------------------------------------------------------


@pibooth.hookimpl
def state_capture_enter(app, cfg):
    """Actions performed when application enter in Capture state.
    """
    handle_sounds(app, "capture", cfg.getfloat('SOUNDS', 'capture_delay'))

# --- Processing State ---------------------------------------------------------


@pibooth.hookimpl
def state_processing_enter(app):
    """Actions performed when application enter in Processing state.
    """
    handle_sounds(app, "processing")

# --- PrintView State ----------------------------------------------------------


@pibooth.hookimpl
def state_print_enter(app):
    """Actions performed when application enter in Print state.
    """
    handle_sounds(app, "print")

# --- Finish State -------------------------------------------------------------


@pibooth.hookimpl
def state_finish_enter(app):
    """Actions performed when application enter in Finish state.
    """
    handle_sounds(app, "finish")
