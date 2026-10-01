# -*- coding: utf-8 -*-

import os
import time
import shutil
import os.path as osp
from types import SimpleNamespace

os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame  # noqa: E402
import pytest  # noqa: E402

from pibooth_sound_effects import plugin  # noqa: E402


SOUNDS_DIR = osp.join(osp.dirname(osp.dirname(osp.abspath(__file__))), 'pibooth_sound_effects', 'sounds')


class FakeConfig(object):

    def __init__(self, sounds_path, preview_delay=3, capture_delay=0.0):
        self.values = {('SOUNDS', 'sounds_path'): str(sounds_path),
                       ('SOUNDS', 'capture_delay'): capture_delay,
                       ('WINDOW', 'preview_delay'): preview_delay}

    def getpath(self, section, option):
        return self.values[(section, option)]

    def getint(self, section, option):
        return int(self.values[(section, option)])

    def getfloat(self, section, option):
        return float(self.values[(section, option)])


class FakeSound(object):

    def __init__(self):
        self.played = []
        self.stopped = 0

    def play(self, loops=0):
        self.played.append(loops)

    def stop(self):
        self.stopped += 1


@pytest.fixture
def sounds_path(tmp_path):
    path = tmp_path / 'sounds'
    shutil.copytree(SOUNDS_DIR, path)
    return path


@pytest.fixture
def app():
    application = SimpleNamespace()
    yield application
    plugin.pibooth_cleanup(application)


def bytes_per_second():
    frequency, size, channels = pygame.mixer.get_init()
    return frequency * channels * abs(size) // 8


def test_reset_create_folder(tmp_path):
    cfg = FakeConfig(tmp_path / 'sounds')
    plugin.pibooth_reset(cfg, False)
    assert sorted(os.listdir(tmp_path / 'sounds')) == sorted(os.listdir(SOUNDS_DIR))


def test_reset_hard_restore_folder(sounds_path):
    (sounds_path / 'custom.wav').write_bytes(b'')
    plugin.pibooth_reset(FakeConfig(sounds_path), False)
    assert (sounds_path / 'custom.wav').exists()
    plugin.pibooth_reset(FakeConfig(sounds_path), True)
    assert not (sounds_path / 'custom.wav').exists()


def test_startup_load_sounds(app, sounds_path):
    plugin.pibooth_startup(app, FakeConfig(sounds_path))
    assert set(app.sounds) == {'capture', 'choose', 'chosen', 'finish', 'preview_countdown', 'preview'}


def test_startup_countdown_length(app, sounds_path):
    plugin.pibooth_startup(app, FakeConfig(sounds_path, preview_delay=5))
    assert len(app.sounds['preview'].get_raw()) == 5 * bytes_per_second()


def test_startup_countdown_with_numbered_sounds(app, sounds_path):
    os.remove(sounds_path / 'preview_countdown.wav')
    shutil.copy(sounds_path / 'capture.wav', sounds_path / '2.wav')
    plugin.pibooth_startup(app, FakeConfig(sounds_path, preview_delay=3))

    raw = app.sounds['preview'].get_raw()
    second = bytes_per_second()
    assert len(raw) == 3 * second
    assert not any(raw[:second])  # 3: silence
    sound_2 = app.sounds['2'].get_raw()
    assert raw[second:second + len(sound_2)] == sound_2
    assert not any(raw[second + len(sound_2):2 * second])  # Padding
    assert not any(raw[2 * second:])  # 1: silence


def test_startup_keep_preview_sound(app, sounds_path):
    shutil.copy(sounds_path / 'capture.wav', sounds_path / 'preview.wav')
    plugin.pibooth_startup(app, FakeConfig(sounds_path))
    assert len(app.sounds['preview'].get_raw()) == len(app.sounds['capture'].get_raw())


def test_startup_missing_folder(app, tmp_path):
    plugin.pibooth_startup(app, FakeConfig(tmp_path / 'not_found'))
    assert app.sounds == {}
    plugin.state_wait_enter(app)  # Shall not fail


def test_startup_mixer_error(app, sounds_path, monkeypatch):
    def init():
        raise pygame.error("No available audio device")
    monkeypatch.setattr(pygame.mixer, 'init', init)
    plugin.pibooth_startup(app, FakeConfig(sounds_path))
    assert app.sounds == {}


def test_states_play_sound(app):
    app.sounds = {'finish': FakeSound(), 'wait': FakeSound()}
    plugin.state_finish_enter(app)
    assert app.sounds['finish'].played == [0]
    assert app.sounds['wait'].played == []


def test_loop_sound_stopped_on_next_state(app):
    app.sounds = {'wait_loop': FakeSound(), 'choose': FakeSound()}
    plugin.state_wait_enter(app)
    assert app.sounds['wait_loop'].played == [-1]
    stopped = app.sounds['wait_loop'].stopped
    plugin.state_choose_enter(app)
    assert app.sounds['wait_loop'].stopped == stopped + 1
    assert app.sounds['choose'].played == [0]


def test_capture_delay(app, sounds_path):
    app.sounds = {'capture': FakeSound()}
    plugin.state_capture_enter(app, FakeConfig(sounds_path, capture_delay=0.2))
    assert app.sounds['capture'].played == []
    time.sleep(0.4)
    assert app.sounds['capture'].played == [0]


def test_capture_delay_cancelled_on_next_state(app, sounds_path):
    app.sounds = {'capture': FakeSound()}
    plugin.state_capture_enter(app, FakeConfig(sounds_path, capture_delay=0.2))
    plugin.state_processing_enter(app)
    time.sleep(0.4)
    assert app.sounds['capture'].played == []
