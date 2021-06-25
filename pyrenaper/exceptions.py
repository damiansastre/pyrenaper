class BaseRenaperException(Exception):
    default_message = 'An error has ocurred'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(self.default_message, **kwargs)

class IncorrectImageSize(BaseRenaperException):
    default_message = "Provided image has incorrect size."


class InvalidOperation(BaseRenaperException):
    default_message = "Invalid Operation, should be one of: back/front"


class EmptySelfieListException(BaseRenaperException):
    default_message = "Please provide at least 1 selfie"


class MissingSelfieFileException(BaseRenaperException):
    default_message = "No Selfie provided in Selfie Object."


class InvalidImage(BaseRenaperException):
    default_message = "Image format should be one of: JPEG/JPG"


class GeoBlockedRequestException(BaseRenaperException):
    default_message = "Your request hast been GeoBlocked"


class InvalidDomainException(BaseRenaperException):
    default_message = "Incorrect Domain Provided"


class InvalidApiKeyException(BaseRenaperException):
    default_message = "Api key is not valid"


class InvalidApiKeyChannelException(BaseRenaperException):
    default_message = "Api key is not valid"


class BarcodeNotFoundException(BaseRenaperException):
    default_message = "Image contains no barcodes."


class IncorrectBarcodeException(BaseRenaperException):
    default_message = "Barcode does not belong to a valid ID."


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
