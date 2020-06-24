# -*- coding: utf-8 -*-

"""Pibooth plugin for sound effects"""

import os
import os.path as osp
import shutil
import pygame
import pibooth


__version__ = "0.0.2"



@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('SOUNDS', 'sounds_path', "~/.config/pibooth/sounds",
                   "Path to the sounds")

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
    app.sounds = {}
    notefile_list = os.listdir(cfg.getpath('SOUNDS', 'sounds_path'))
    for sound in notefile_list:
        if sound.endswith(".wav"):
            app.sounds[sound[:-4]] = pygame.mixer.Sound(os.path.join(cfg.getpath('SOUNDS', 'sounds_path'), sound))


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
    if "wait" in app.sounds:
        app.sounds["wait"].play(loops=-1)

#--- Choose State -------------------------------------------------------------
@pibooth.hookimpl
def state_choose_enter(app):
    """Actions performed when application enter in Choose state.
    """
    if "wait" in app.sounds:
        app.sounds["wait"].stop()
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
def state_preview_enter(app, cfg):
    """Actions performed when application enter in Preview state.
    """
    if "preview" in app.sounds:
        app.sounds["preview"].play(loops=cfg.getint("WINDOW","preview_delay")-1)

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
