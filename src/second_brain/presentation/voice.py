"""Audio capture for voice input — a pure presentation concern.

The core never learns the text came from a microphone: capture → WAV →
Transcriber port → the same handle_turn path as typed input. sounddevice
(and PortAudio underneath) is imported lazily, so keyboard-only usage
never touches audio machinery.

Enter-to-stop rather than hold-to-talk: reliable in every terminal, no
raw key handling, no platform quirks.
"""

from __future__ import annotations

import io
import wave

SAMPLE_RATE = 16_000  # mono 16-bit @ 16 kHz: what Whisper wants, small payloads


def encode_wav(pcm: bytes, sample_rate: int = SAMPLE_RATE) -> bytes:
    """Wrap raw mono 16-bit PCM in a WAV container, stdlib only."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(sample_rate)
        writer.writeframes(pcm)
    return buffer.getvalue()


def record_until_enter(sample_rate: int = SAMPLE_RATE) -> bytes:
    """Record from the default microphone until the user presses Enter;
    return the take as WAV bytes. Blocks by design — it's push-to-talk."""
    import sounddevice as sd  # lazy: PortAudio only when voice is used

    frames: list[bytes] = []

    def _collect(indata: object, _frames: int, _time: object, _status: object) -> None:
        frames.append(bytes(indata))  # type: ignore[arg-type]

    with sd.RawInputStream(
        samplerate=sample_rate, channels=1, dtype="int16", callback=_collect
    ):
        input()
    return encode_wav(b"".join(frames), sample_rate)
