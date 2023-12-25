import io
from custom_mimetypes.settings import *
from custom_mimetypes import classes


def define_mimetype(file_entry: io.BytesIO | str | bytes) -> CustomMimeType | None:
    entry: bytes | None = None
    if isinstance(file_entry, str):
        with open(file_entry, 'rb') as file:
            entry = file.read(READ_LIMIT)
    elif isinstance(file_entry, bytes):
        entry = file_entry[:READ_LIMIT]
    elif isinstance(file_entry, io.BytesIO):
        file_entry.seek(0)
        entry = file_entry.read(READ_LIMIT)
        file_entry.seek(0)

    for key, info in MIMETYPES.items():
        read_limit, mime, header = info.generator()

        if entry[:read_limit] == header:
            return MIMETYPES[key]
    return None  # mimetype hasn't been defined
