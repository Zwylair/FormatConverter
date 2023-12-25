import io
from typing import Any
import pydub


class AudioImporter:
    def __init__(self, target_file: io.BytesIO | str | bytes):
        self.decoded_audio: Any = None


class PyDubImport(AudioImporter):
    def __init__(self, target_file: io.BytesIO | str | bytes):
        super().__init__(target_file)

        if isinstance(target_file, bytes):
            target_file = io.BytesIO(target_file)
        self.decoded_audio = pydub.AudioSegment.from_file(target_file)
