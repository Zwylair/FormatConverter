from custom_mimetypes.classes import CustomMimeType

MIMETYPES = {
    'rle2': CustomMimeType(20, 'image/dxt5rle2', b'DXT5RLE2\x00\x04\x00\x08\x0c\x00\x00\x00\x00\x01\x00\x00'),
    'rles': CustomMimeType(20, 'image/dxt5rles', b'DXT5RLES\x00\x04\x00\x08\x0c\x00\x00\x000\x01\x00\x00')
}
AUDIO_MIMETYPES = {}
VIDEO_MIMETYPES = {}
IMAGE_MIMETYPES = {}

READ_LIMIT = 1024

#

_mimetypes_array = {
    'audio': AUDIO_MIMETYPES,
    'video': VIDEO_MIMETYPES,
    'image': IMAGE_MIMETYPES,
}
for k, v in MIMETYPES.items():
    _mimetypes_array[v.mime_str.split('/')[0]][k] = v
