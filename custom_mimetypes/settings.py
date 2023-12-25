from custom_mimetypes.classes import CustomMimeType

MIMETYPES = {
    'rle2': CustomMimeType(20, 'image/rle2', b'DXT5RLE2\x00\x04\x00\x08\x0c\x00\x00\x00\x00\x01\x00\x00'),
    'rles': CustomMimeType(20, 'image/rles', b'DXT5RLES\x00\x04\x00\x08\x0c\x00\x00\x000\x01\x00\x00')
}
AUDIO_MIMETYPES = {}
VIDEO_MIMETYPES = {}
IMAGE_MIMETYPES = {}

READ_LIMIT = 1024

#

for k, v in MIMETYPES.items():
    match v.mime_str.split('/')[0]:
        case 'audio':
            AUDIO_MIMETYPES[k] = v
        case 'video':
            VIDEO_MIMETYPES[k] = v
        case 'image':
            IMAGE_MIMETYPES[k] = v
