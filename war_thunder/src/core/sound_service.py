import wave
import struct
import arcade
import tempfile
import os
import math
import io
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
        self.music_volume = SettingsService().get('music_volume', 0.3)
        self.sounds = {}
        self.temp_files = []
        self._generate_all_sounds()
        self._generate_background_music()
        self._music_player = None
        self._music_looping = True

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

    def _generate_melody_data(self, frequencies, duration, volume=0.5, sample_rate=22050):
        """生成旋律音轨"""
        num_samples = int(duration * sample_rate)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            note_index = int(t / duration * len(frequencies))
            note_index = min(note_index, len(frequencies) - 1)
            freq = frequencies[note_index]
            value = int(volume * 32767 * math.sin(2 * math.pi * freq * t))
            samples.append(struct.pack('<h', value))
        return b''.join(samples)

    def _generate_background_music(self):
        """生成程序化背景音乐 - 简单循环旋律"""
        # 简单的战斗风格旋律频率 (C大调分解和弦进行)
        melody_freqs = [
            262, 330, 392, 523,  # C E G C
            392, 330, 262, 196,  # G E C G
            294, 370, 440, 587,  # D F# A D
            523, 440, 370, 294,  # C A F# D
        ]
        # 贝斯低音
        bass_freqs = [
            131, 131, 165, 165,
            147, 147, 196, 196,
            175, 175, 220, 220,
            196, 196, 147, 147,
        ]

        note_duration = 0.25  # 每个音符0.25秒
        total_notes = len(melody_freqs)
        total_duration = total_notes * note_duration

        # 生成旋律
        melody_samples = []
        for i in range(total_notes):
            freq = melody_freqs[i]
            t = i * note_duration
            for j in range(int(note_duration * 22050)):
                time = t + j / 22050
                env = 0.7 + 0.3 * math.sin(math.pi * j / (note_duration * 22050))
                value = int(0.3 * 32767 * env * math.sin(2 * math.pi * freq * time))
                melody_samples.append(struct.pack('<h', value))

        # 生成低音
        bass_samples = []
        for i in range(total_notes):
            freq = bass_freqs[i]
            t = i * note_duration
            for j in range(int(note_duration * 22050)):
                time = t + j / 22050
                env = 0.6 + 0.4 * math.sin(math.pi * j / (note_duration * 22050))
                value = int(0.2 * 32767 * env * math.sin(2 * math.pi * freq * time))
                bass_samples.append(struct.pack('<h', value))

        # 合并旋律和低音
        combined = []
        for m, b in zip(melody_samples, bass_samples):
            melody_val = struct.unpack('<h', m)[0]
            bass_val = struct.unpack('<h', b)[0]
            combined_val = max(-32767, min(32767, melody_val + bass_val))
            combined.append(struct.pack('<h', combined_val))

        # 创建WAV
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22050)
            wav_file.writeframes(b''.join(combined))
        self.music_data = buffer.getvalue()

    def _create_music_stream(self):
        """创建可循环的背景音乐流"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.write(self.music_data)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        return arcade.Sound(temp_file.name)

    def play_music(self, looping=True):
        """播放背景音乐"""
        self._music_looping = looping
        if self._music_player is not None and hasattr(self._music_player, 'stop'):
            try:
                self._music_player.stop()
            except:
                pass
        music_stream = self._create_music_stream()
        self._music_player = music_stream.play(volume=self.music_volume, loop=looping)

    def stop_music(self):
        """停止背景音乐"""
        if self._music_player is not None and hasattr(self._music_player, 'stop'):
            try:
                self._music_player.stop()
            except:
                pass
            self._music_player = None

    def pause_music(self):
        """暂停背景音乐"""
        if self._music_player is not None and hasattr(self._music_player, 'pause'):
            try:
                self._music_player.pause()
            except:
                pass

    def resume_music(self):
        """恢复背景音乐"""
        if self._music_player is not None:
            try:
                self._music_player.play()
            except:
                pass

    def set_music_volume(self, volume):
        """设置背景音乐音量"""
        self.music_volume = volume
        if self._music_player is not None and hasattr(self._music_player, 'volume'):
            try:
                self._music_player.volume = volume
            except:
                pass

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(volume=self.volume)

    def set_volume(self, volume):
        self.volume = volume
