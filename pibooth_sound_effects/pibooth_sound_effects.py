# -*- coding: utf-8 -*-

import os
import os.path as osp
import shutil
import pygame
import pibooth


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('SOUNDS', 'sounds_path', "~/.config/pibooth/sounds",
                   "Path to the sounds folder")


@pibooth.hookimpl
def pibooth_reset(cfg, hard):
    """Populate sounds folder if it doesn't exists"""
    sound_path = cfg.getpath('SOUNDS', 'sounds_path')
    if not osp.isdir(sound_path) or hard:
        source_sound_path = osp.join(osp.dirname(osp.abspath(__file__)), 'sounds')
        shutil.copytree(source_sound_path, sound_path)


@pibooth.hookimpl
def pibooth_startup(app, cfg):
    """Init the pygame mixer and load available sounds"""
    pygame.mixer.pre_init(channels=2, buffer=1024)
    pygame.mixer.init()

    one_second_bytes_length = 4 * 44100
    app.sounds = {}
    sounds_file_list = os.listdir(cfg.getpath('SOUNDS', 'sounds_path'))
    for sound in sounds_file_list:
        if sound.endswith(".wav"):
            app.sounds[sound[:-4]] = pygame.mixer.Sound(os.path.join(cfg.getpath('SOUNDS', 'sounds_path'), sound))

    # Generate countdown if files are given and not preview
    if not "preview" in app.sounds:
        preview_delay = int(cfg.getint("WINDOW", "preview_delay"))
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

        # preview_sound_raw = app.sounds["preview_countdown"].get_raw()
        if preview_sound_raw:
            app.sounds["preview"] = pygame.mixer.Sound(preview_sound_raw)


@pibooth.hookimpl
def pibooth_cleanup():
    """Quit the mixer
    """
    pygame.mixer.quit()

#--- Wait State ---------------------------------------------------------------
@pibooth.hookimpl
def state_wait_enter(app):
    """Actions performed when application enter in Wait state.
    """
    if "wait_loop" in app.sounds:
        app.sounds["wait_loop"].play(loops=-1)
    if "wait" in app.sounds:
        app.sounds["wait"].play()

#--- Choose State -------------------------------------------------------------
@pibooth.hookimpl
def state_choose_enter(app):
    """Actions performed when application enter in Choose state.
    """
    if "wait_loop" in app.sounds:
        app.sounds["wait_loop"].stop()
    if "choose" in app.sounds:
        app.sounds["choose"].play()

#--- Chosen State -------------------------------------------------------------
@pibooth.hookimpl
def state_chosen_enter(app):
    """Actions performed when application enter in Chosen state.
    """
    if "chosen" in app.sounds:
        app.sounds["chosen"].play()

#--- Preview State ------------------------------------------------------------
@pibooth.hookimpl
def state_preview_enter(app):
    """Actions performed when application enter in Preview state.
    """
    if "preview" in app.sounds:
        app.sounds["preview"].play()

#--- Capture State ------------------------------------------------------------
@pibooth.hookimpl
def state_capture_enter(app):
    """Actions performed when application enter in Capture state.
    """
    if "capture" in app.sounds:
        app.sounds["capture"].play()

#--- Processing State ---------------------------------------------------------
@pibooth.hookimpl
def state_processing_enter(app):
    """Actions performed when application enter in Processing state.
    """
    if "processing" in app.sounds:
        app.sounds["processing"].play()

#--- PrintView State ----------------------------------------------------------
@pibooth.hookimpl
def state_print_enter(app):
    """Actions performed when application enter in Print state.
    """
    if "print" in app.sounds:
        app.sounds["print"].play()

#--- Finish State -------------------------------------------------------------
@pibooth.hookimpl
def state_finish_enter(app):
    """Actions performed when application enter in Finish state.
    """
    if "finish" in app.sounds:
        app.sounds["finish"].play()
