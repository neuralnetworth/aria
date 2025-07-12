import time
import pyaudio
import numpy as np
import soundfile as sf
import scipy.signal as signal


class Ap:
    def __init__(self, params=None, ui=None):
        self.params = params or {}
        self.audio_device = self.params.get("audio_device", None)
        self.samplerate = self.params.get("samplerate", None)
        self.buffer_size = self.params.get("buffer_size", None)
        self.channels = self.params.get("channels", None)
        self.listening_sound_path = self.params.get("assets", None).get(
            "listening_sound", None
        )
        self.transition_sound_path = self.params.get("assets", None).get(
            "transition_sound", None
        )
        self.sample_format = pyaudio.paInt16

        if self.audio_device == "default":
            self.audio_device = None

        self.ui = ui
        self.update_ui = False
        self.load_visual_once = True
        self.audio_buffer = None

        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.samplerate,
            frames_per_buffer=self.buffer_size,
            output=True,
            output_device_index=self.audio_device,
            stream_callback=self._callback,
        )

        self.listening_sound, self.listening_sound_sr = sf.read(
            self.listening_sound_path
        )
        self.transition_sound, self.transition_sound_sr = sf.read(
            self.transition_sound_path
        )
        
        # Resample sounds to match the configured sample rate if needed
        if self.listening_sound_sr != self.samplerate:
            num_samples = int(len(self.listening_sound) * self.samplerate / self.listening_sound_sr)
            self.listening_sound = signal.resample(self.listening_sound, num_samples)
            self.listening_sound_sr = self.samplerate
            
        if self.transition_sound_sr != self.samplerate:
            num_samples = int(len(self.transition_sound) * self.samplerate / self.transition_sound_sr)
            self.transition_sound = signal.resample(self.transition_sound, num_samples)
            self.transition_sound_sr = self.samplerate

    def _callback(self, in_data, frame_count, time_info, status):
        if self.audio_buffer is None:
            data = np.zeros(frame_count, dtype=np.int16)
        elif len(self.audio_buffer) >= frame_count:
            data = self.audio_buffer[:frame_count]
            self.audio_buffer = self.audio_buffer[frame_count:]
        else:
            shortfall = frame_count - len(self.audio_buffer)
            data = np.concatenate(
                (self.audio_buffer, np.zeros(shortfall, dtype=np.int16))
            )
            self.audio_buffer = None
        if self.update_ui:
            self.ui.update_visual("Aria", data.astype(np.float32, order="C") / 32768.0)
        return (data.tobytes(), pyaudio.paContinue)

    def check_audio_finished(self):
        if self.audio_buffer is not None:
            time.sleep(len(self.audio_buffer) / self.samplerate)
        self.update_ui = False
        self.load_visual_once = True

    def stream_sound(self, chunk, update_ui=False):
        if update_ui and self.load_visual_once:
            self.ui.load_visual("Aria")
            self.load_visual_once = False
        self.update_ui = update_ui
        if self.audio_buffer is None:
            self.audio_buffer = chunk
        else:
            self.audio_buffer = np.concatenate((self.audio_buffer, chunk))

    def play_sound(self, sound):
        # Convert stereo to mono if needed
        if len(sound.shape) > 1 and sound.shape[1] > 1:
            sound = np.mean(sound, axis=1)
        
        for chunk_index in range(0, len(sound), self.buffer_size):
            chunk = sound[chunk_index : chunk_index + self.buffer_size]
            self.stream_sound(np.int16(chunk * 32768))
        self.check_audio_finished()
