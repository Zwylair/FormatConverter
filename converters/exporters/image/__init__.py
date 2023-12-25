from typing import Any


class ImageExporter:
    def __init__(self, decoded_media: Any, export_filepath: str, export_format: str):
        self.decoded_media = decoded_media
        self.export_filepath = export_filepath
        self.export_format = export_format

    def export(self):
        ...
