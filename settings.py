import os
import pydub
from converters import *

# tabulate settings
FN_LIMIT = 38
FN_LIMIT_HALVED = int(FN_LIMIT / 2)
TABLEFMT = 'plain'

# supported formats
SUPPORTED_AUDIO_IMPORTERS = {
    'audio/mpeg': PyDubImport,
    'audio/wav': PyDubImport,
    'audio/ogg': PyDubImport,
    'audio/opus': PyDubImport,
}
SUPPORTED_AUDIO_EXPORTERS = {
    'mp3': PyDubExport,
    'wav': PyDubExport,
    'ogg': PyDubExport
}

SUPPORTED_VIDEO_OUTPUT = ()
SUPPORTED_IMAGE_OUTPUT = ()
SUPPORTED_AUDIO_OUTPUT = tuple(SUPPORTED_AUDIO_EXPORTERS.keys())

SUPPORTED_VIDEO_IMPORT = ()
SUPPORTED_IMAGE_IMPORT = ()
SUPPORTED_AUDIO_IMPORT = tuple(SUPPORTED_AUDIO_IMPORTERS.keys())

ALL_SUPPORTED_IMPORT = SUPPORTED_VIDEO_IMPORT + SUPPORTED_IMAGE_IMPORT + SUPPORTED_AUDIO_IMPORT

#
LOG_FIELD_DEFAULT = 'Logs'
FFMPEG_PATH = 'bin\\ffmpeg'

os.environ['PATH'] += f';{os.getcwd()}\\{FFMPEG_PATH}'
pydub.AudioSegment.converter = f'{FFMPEG_PATH}/ffmpeg.exe'
pydub.AudioSegment.ffprobe = f'{FFMPEG_PATH}/ffprobe.exe'
