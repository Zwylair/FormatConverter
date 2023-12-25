import os
from typing import Type
import pydub  # restricted to remove import
from converters import *

# tabulate settings
FN_LIMIT = 38
FN_LIMIT_HALVED = int(FN_LIMIT / 2)
TABLEFMT = 'plain'

# # # supported formats
SUPPORTED_OPERATION = ('convert', 'merge')

# define supported media formats to import/export
AUDIO_IMPORTERS: dict[str, Type[AudioImporter]] = {
    'audio/mpeg': PyDubImport,
    'audio/x-wav': PyDubImport,
    'audio/ogg': PyDubImport,
    'audio/opus': PyDubImport,
}
AUDIO_EXPORTERS: dict[str, Type[AudioExporter]] = {
    'mp3': PyDubExport,
    'wav': PyDubExport,
    'ogg': PyDubExport
}

IMAGE_IMPORTERS: dict[str, Type[ImageImporter]] = {}
IMAGE_EXPORTERS: dict[str, Type[ImageExporter]] = {}

VIDEO_IMPORTERS: dict[str, Type[VideoImporter]] = {}
VIDEO_EXPORTERS: dict[str, Type[VideoExporter]] = {}

# make shortcut variables
SUPPORTED_AUDIO_IMPORT = tuple(AUDIO_IMPORTERS.keys())
SUPPORTED_IMAGE_IMPORT = tuple(IMAGE_IMPORTERS.keys())
SUPPORTED_VIDEO_IMPORT = tuple(VIDEO_IMPORTERS.keys())
ALL_SUPPORTED_IMPORT = SUPPORTED_VIDEO_IMPORT + SUPPORTED_IMAGE_IMPORT + SUPPORTED_AUDIO_IMPORT

SUPPORTED_AUDIO_OUTPUT = tuple(AUDIO_EXPORTERS.keys())
SUPPORTED_IMAGE_OUTPUT = tuple(IMAGE_EXPORTERS.keys())
SUPPORTED_VIDEO_OUTPUT = tuple(VIDEO_EXPORTERS.keys())

#

LOG_FIELD_DEFAULT = 'Logs'
FFMPEG_PATH = 'bin\\ffmpeg'

os.environ['PATH'] += f';{os.getcwd()}\\{FFMPEG_PATH}'
pydub.AudioSegment.converter = f'{FFMPEG_PATH}/ffmpeg.exe'
pydub.AudioSegment.ffprobe = f'{FFMPEG_PATH}/ffprobe.exe'
