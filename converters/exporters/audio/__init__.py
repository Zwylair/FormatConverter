from typing import Any


class AudioExporter:
    def __init__(self, decoded_audio: Any, export_filepath: str, export_format: str):
        self.decoded_audio = decoded_audio
        self.export_filepath = export_filepath
        self.export_format = export_format

    def export(self):
        ...


class PyDubExport(AudioExporter):
    def export(self):
        self.decoded_audio.export(self.export_filepath, format=self.export_format)
