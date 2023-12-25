from typing import Any


class AudioExporter:
    def __init__(self, decoded_media: Any, export_filepath: str, export_format: str):
        self.decoded_media = decoded_media
        self.export_filepath = export_filepath
        self.export_format = export_format

    def export(self):
        ...


class PyDubExport(AudioExporter):
    def export(self):
        codec = 'libvorbis' if self.export_format == 'ogg' else None
        self.decoded_media.export(self.export_filepath, format=self.export_format, codec=codec)
