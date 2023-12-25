class CustomMimeType:
    def __init__(self, read_limit: int, mime_str: str, header: bytes):
        self.read_limit = read_limit
        self.header = header
        self.mime_str = mime_str

    def __str__(self):
        return self.mime_str

    def generator(self) -> tuple[int, str, bytes]:
        """ return its parameters in tuple for easy use through a for loop """
        return self.read_limit, self.mime_str, self.header
