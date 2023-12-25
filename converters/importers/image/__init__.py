# import io
#
#
# class ImageConverter:
#     def __init__(self, target_file: io.BytesIO | str | bytes):
#         self.target_file = target_file
#
#     def convert_to_standard(self):
#         """ needs to be replaced with converter logics """
#         pass
#
#
# class RLESConverter(ImageConverter):
#     ...
import io
from typing import Any
import pydub


class ImageImporter:
    def __init__(self, target_file: io.BytesIO | str | bytes):
        self.decoded_media: Any = None


class PILImport(ImageImporter):
    def __init__(self, target_file: io.BytesIO | str | bytes):
        super().__init__(target_file)

        # if isinstance(target_file, bytes):
        #     target_file = io.BytesIO(target_file)
        # self.decoded_audio = pydub.AudioSegment.from_file(target_file)
