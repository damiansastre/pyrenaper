from collections import namedtuple
from .exceptions import InvalidImageFormatException
from .settings import STATUS_CODES, SELFIE_TYPE_FORMATS

Environment = namedtuple('Environment', ['base_url', 'domain'])


class Selfie:
    file = None
    image_type = None

    def __init__(self, file: str, image_type: str):
        if image_type not in SELFIE_TYPE_FORMATS:
            raise InvalidImageFormatException
        self.image_type = image_type
        self.file = file

    def __str__(self):
        return "Selfie({})".format(self.image_type)


class RenaperResponse:
    status = None
    code = None
    code_description = None
    message = None
    _error_payload = None
    _response_payload = None

    def __init__(self, data, valid_status):
        if data.get('error'):
            self.status = False
            self.code = data['error'].pop('code')
            description = STATUS_CODES.get(data['error']['code'])
            self.code_description = description if description else 'Unknown'
            self._error_payload = data['error']
        else:
            self.status = True
            code = data.pop('code')
            self.code = code
            self.message = data.pop('message')
            self._response_payload = data

            if STATUS_CODES.get(code):
                if STATUS_CODES[code] in valid_status:
                    self.code_description = STATUS_CODES[code]
                else:
                    self.code_description = 'Returned Code is not in valid_status for this function'
            else:
                self.code_description = 'Returned Code is not configured in env.'

    @property
    def json(self):
        return {attr: getattr(self, attr) for attr in ['status', 'code', 'code_description', 'message', 'request']}

    @property
    def response(self):
        if not self.status:
            return self._error_payload
        return self._response_payload

    def __str__(self):
        return 'RenaperResponse(status={}, code={}, description={}, response={}'.format(str(self.status),
                                                                                        str(self.code),
                                                                                        str(self.message),
                                                                                        self.code_description,
                                                                                        str(self.response))

    def __repr__(self):
        return self.__str__()