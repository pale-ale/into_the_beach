"""Manages playback of audio cues."""

import pygame
import pygame.mixer
from itblib.Log import log

#pylint: disable=invalid-name
class AUDIO_KEYS:
    """'Enum' to store the audio keys."""
    BUTTON = "button_click.wav"
#pylint: enable=invalid-name

AUDIO_PATH = "audio/"

class AudioManager():
    """Manages playback of audio cues."""
    @staticmethod
    def play_audio(filename:str, loop:bool=False):
        """Play audio associated with the provided filename."""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            sound = pygame.mixer.Sound(AUDIO_PATH + filename)
            channel = pygame.mixer.find_channel(False)
            channel.set_volume(.2)
            channel.play(sound, -loop)
        except FileNotFoundError:
            log(f"File '{filename}' not found.", 2)

    @staticmethod
    def stop_audio():
        pygame.mixer.stop()
