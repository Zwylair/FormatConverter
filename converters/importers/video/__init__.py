import io
from typing import Any


class VideoImporter:
    def __init__(self, target_file: io.BytesIO | str | bytes):
        self.decoded_media: Any = None


# class PILImport(ImageImporter):
#     def __init__(self, target_file: io.BytesIO | str | bytes):
#         super().__init__(target_file)
#
#         # if isinstance(target_file, bytes):
#         #     target_file = io.BytesIO(target_file)
#         # self.decoded_audio = pydub.AudioSegment.from_file(target_file)
