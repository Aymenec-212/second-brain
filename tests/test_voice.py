"""Voice tests — offline. Hardware capture is a thin sounddevice loop we
don't test; what we test is ours: the WAV encoding and the adapter's
contract with the Groq client.
"""

import io
import wave
from types import SimpleNamespace
from typing import Any, cast

import pytest
from groq import Groq

from second_brain.infra.voice.groq_whisper import GroqTranscriber, TranscriptionFailure
from second_brain.presentation.voice import SAMPLE_RATE, encode_wav


def test_encode_wav_produces_correct_header_and_length() -> None:
    pcm = b"\x00\x00" * 1600  # 0.1 s of silence, mono 16-bit
    data = encode_wav(pcm)
    with wave.open(io.BytesIO(data), "rb") as reader:
        assert reader.getnchannels() == 1
        assert reader.getsampwidth() == 2
        assert reader.getframerate() == SAMPLE_RATE
        assert reader.getnframes() == 1600


class StubTranscriptions:
    def __init__(self, text: str) -> None:
        self._text = text
        self.requests: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> Any:
        self.requests.append(kwargs)
        return SimpleNamespace(text=self._text)


def stub_client(text: str) -> tuple[Groq, StubTranscriptions]:
    stub = StubTranscriptions(text)
    client = SimpleNamespace(audio=SimpleNamespace(transcriptions=stub))
    return cast(Groq, client), stub


def test_transcriber_sends_wav_and_strips_whitespace() -> None:
    client, stub = stub_client("  Bonjour, je réfléchis à Cairn.  ")
    transcriber = GroqTranscriber(client, model="whisper-large-v3")
    audio = encode_wav(b"\x00\x00" * 160)
    text = transcriber.transcribe(audio)
    assert text == "Bonjour, je réfléchis à Cairn."
    request = stub.requests[0]
    assert request["model"] == "whisper-large-v3"
    filename, payload = request["file"]
    assert filename.endswith(".wav")
    assert payload == audio


def test_empty_transcription_raises_typed_failure() -> None:
    client, _ = stub_client("   ")
    transcriber = GroqTranscriber(client, model="whisper-large-v3")
    with pytest.raises(TranscriptionFailure):
        transcriber.transcribe(encode_wav(b"\x00\x00" * 160))
