import io
from dataclasses import dataclass, field
from openai import OpenAI
from domain.stt_service import STTService


@dataclass
class WhisperSTTService(STTService):
    client: OpenAI
    model: str = field(default="whisper")

    def transcribe(self, audio_data: bytes) -> str:
        byte_stream = io.BytesIO(audio_data)
        byte_stream.name = "audio.mp3"

        result = self.client.audio.transcriptions.create(
            file=byte_stream,
            model=self.model,
        )

        return result.text
