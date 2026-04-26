import wave
import struct
import arcade
import tempfile
import os
from src.core.settings_service import SettingsService


class SoundService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.volume = SettingsService().get('sound_volume', 0.5)
        self.sounds = {}
        self.temp_files = []
        self._generate_all_sounds()

    def _generate_wav_data(self, frequency, duration, volume=0.5, sample_rate=22050):
        num_samples = int(duration * sample_rate)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            import math
            value = int(volume * 32767 * math.sin(2 * math.pi * frequency * t))
            samples.append(struct.pack('<h', value))
        wav_data = b''.join(samples)

        import io
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(wav_data)
        return buffer.getvalue()

    def _generate_all_sounds(self):
        sound_configs = {
            'shoot': (880, 0.05, 0.3),
            'explosion': (220, 0.15, 0.5),
            'hit': (440, 0.1, 0.4),
            'powerup': (1200, 0.1, 0.4),
            'game_over': (330, 0.3, 0.5),
        }
        for name, (freq, dur, vol) in sound_configs.items():
            wav_data = self._generate_wav_data(freq, dur, vol)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.write(wav_data)
            temp_file.close()
            self.temp_files.append(temp_file.name)
            self.sounds[name] = arcade.Sound(temp_file.name)

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(volume=self.volume)

    def set_volume(self, volume):
        self.volume = volume
