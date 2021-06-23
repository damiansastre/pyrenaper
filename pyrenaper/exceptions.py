class IncorrectImageSize(Exception):
    pass


class InvalidOperation(Exception):
    pass


class EmptySelfieListException(Exception):
    pass


class MissingSelfieFileException(Exception):
    pass


class InvalidImage(Exception):
    pass


class GeoBlockedRequestException(Exception):
    pass


class InvalidDomainException(Exception):
    pass


class InvalidApiKeyException(Exception):
    pass


class InvalidApiKeyChannelException(Exception):
    pass


class BarcodeNotFoundException(Exception):
    pass


class IncorrectBarcodeException(Exception):
    pass


class ApiKeyForPackageNotFoundException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__('Please provide an api key for Package {}'.format(str(message)))

class InvalidImageFormatException(Exception):
    def __init__(self, format, formats, *args, **kwargs):
        super().__init__('Invalid format [{}] please use one of :{}'.format(str(format),
                                                                            str([f for f in formats])))


class InvalidLengthException(Exception):
    def __init__(self, size, min_l, max_l, *args, **kwargs):
        super().__init__('Invalid image length [{}] not in range {} - {} '.format(str(size), min_l, max_l))


class InvalidHeightException(Exception):
    def __init__(self, size, min_l, max_l, *args, **kwargs):
        super().__init__('Invalid image length [{}] not in range {} - {} '.format(str(size), min_l, max_l))


RENAPER_EXCEPTION_CODES = {444: GeoBlockedRequestException,
                           501: InvalidDomainException,
                           511: InvalidApiKeyException,
                           555: InvalidApiKeyChannelException}
