"""Groq Whisper transcriber: speech → text behind the Transcriber port.

Whisper large v3 auto-detects English, French, and the code-switching
between them — no language hint on purpose, since forcing one would break
exactly the bilingual sessions this store is built for.
"""

from __future__ import annotations

from groq import Groq


class TranscriptionFailure(RuntimeError):
    """Nothing usable came back — likely silence."""


class GroqTranscriber:
    """Implements the Transcriber port over Groq's audio API."""

    def __init__(self, client: Groq, model: str) -> None:
        self._client = client
        self._model = model

    def transcribe(self, audio_wav: bytes) -> str:
        result = self._client.audio.transcriptions.create(
            file=("speech.wav", audio_wav),
            model=self._model,
        )
        text = (result.text or "").strip()
        if not text:
            raise TranscriptionFailure("empty transcription — was there any speech?")
        return text
