from collections import defaultdict
from typing import Optional, Dict, List
from .decorators import api_call_wrapper, package_id, clean_files
from .exceptions import *
from .settings import *
from PIL import Image
from io import BytesIO
import base64
import requests
import zxing

Response = requests.models.Response

class Renaper:
    """Renaper API implementation.

    This class provides methods to access Argentina's Government ID validation Methods.
    Api keys should be obtained in RENAPER's panel: Administration -> API Key.
    """
    _env = None
    _api_keys = defaultdict(None)
    _headers = {"Content-Type": "application/json"}

    def __init__(self,
                 environment: str,
                 package1_apikey: Optional[str] = None,
                 package2_apikey: Optional[str] = None,
                 package3_apikey: Optional[str] = None) -> None:
        self._env = environment
        self._set_api_keys(package1_apikey, package2_apikey, package3_apikey)

    def _set_api_keys(self, *args):
        for i in range(1, len(args)+1):
            self._api_keys[i] = args[i-1]

    def _get_error_code(self, request: Response) -> Dict:
        if request.status_code in RENAPER_EXCEPTION_CODES:
            raise RENAPER_EXCEPTION_CODES[request.status_code]
        else:
            if request.status_code == 400:
                return {"error": request.json()}
            raise Exception("{} status code returned".format(str(request.status_code)))

    def _get_request_headers(self, url: str, p_id: int) -> Dict:
        if not self._api_keys.get(p_id):
            raise ApiKeyForPackageNotFoundException(p_id)
        headers = self._headers.copy()
        headers['url'] = self._build_url(url)
        headers['apiKey'] = self._api_keys[p_id]
        return headers

    def _make_request(self, url: str, payload: dict, p_id: int) -> Dict:
        headers = self._get_request_headers(url, p_id)
        try:
            request = requests.post(self._env.domain,
                                    json=payload,
                                    headers=headers)
        except Exception as e:
            raise e
        else:
            if request.status_code != 200:
                try:
                    error_payload = self._get_error_code(request)
                    return error_payload
                except Exception as e:
                    raise e
        return request.json()

    def _build_url(self, uri: str) -> str:
        """
        Builds URL based on ENV base_url and method url
        :(str) uri: method_url
        :(str) return: formated url
        """
        return ''.join((self._env.base_url, uri))

    def _validate_image(self, image: str, settings: Dict):
        """
        Checks validity of image to uplaod.
        :(image) image: Pillow Image object to validate
        :(dict) settings: Image format settings.
        """
        try:
            image = Image.open(BytesIO(base64.b64decode(image)))
        except Exception as e:
            raise InvalidImage('Not able to parse provided image')
        else:
            if image.format.lower() not in settings['formats']:
                raise InvalidImageFormatException(image.format.lower(), settings['formats'])
            if not (settings['min_length'] <= image.width <= settings['max_length']):
                raise InvalidLengthException(image.width, settings['min_length'], settings['max_length'])
            if 'height' in settings.keys():
                if not (settings['min_height'] <= image.height <= settings['max_height']):
                    raise InvalidHeightException(image.width, settings['min_height'], settings['max_height'])

    def _decode_image(self, image):
        return image.decode() if type(image) == bytes else image

    def _parse_barcode(self, barcode: str) -> Dict:
        """
        Parses Document data from ID PDF417 QR code.
        :(base64 img) barcode: Front/Back or simple image of Document ID Barcode.
        :return: Parsed payload
        """
        barcode_data = barcode.split('@')
        if 8 <= len(barcode_data) <= 9:
            data = {"order": barcode_data[0],
                    "lastNames": barcode_data[1],
                    "names": barcode_data[2],
                    "gender": barcode_data[3],
                    "number": barcode_data[4],
                    "birthdate": barcode_data[6]}
        elif 16 <= len(barcode_data) <= 17:
            data = {"order": barcode_data[0],
                    "lastNames": barcode_data[4],
                    "names": barcode_data[5],
                    "gender": barcode_data[8],
                    "number": barcode_data[1],
                    "birthdate": barcode_data[7]}
        else:
            raise IncorrectBarcodeException
        return data

    @clean_files
    def _get_barcode_payload(self, operation_id: int, image: str) -> Dict:
        """
        Extracts information from Argentina's PDF417 Qr Code.
        :(base64 img) image: Image containing Argentina's Government PDF417 QR Code.
        :return:
        """
        filename = '{}.jpg'.format(str(operation_id))
        np_img = Image.open(BytesIO(base64.b64decode(image)))
        np_img.save(filename)
        reader = zxing.BarCodeReader()
        barcode = reader.decode(filename)
        if not barcode:
            raise BarcodeNotFoundException
        return self._parse_barcode(barcode.parsed)

    def _add_document_image(self,
                            operation_type: str,
                            operation_id: int,
                            number: int,
                            gender: str,
                            file: str,
                            analyze_anomalies: Optional[bool] = False,
                            analyze_ocr: Optional[bool] = False,
                            **kwargs) -> Dict:
        """
        Adds document images to operation.
        :(str) operation_type: type of image being uploaded, front or back of document
        :(int) operation_id: operation_id retrieved from new_operation_method
        :(int) number: government ID number
        :(str) gender: gender must be M / F
        :(base64 image) file: image file base64 encoded, sizes must match settings for document image.
        :(boolean) analyze_anomalies: Check veracity by area. Result will be provided by end_operation
        :(boolean) analyze_ocr: Checks document with OCR capabilities. Result will be provided by end_operation
        :(dict) return:
        """
        if operation_type not in ['front', 'back']:
            raise InvalidOperation("Operations are either front or back.")

        self._validate_image(file, DOCUMENT_FORMAT_SETTINGS)

        data = {"operationId": operation_id,
                "number": number,
                "gender": gender,
                "analyzeAnomalies": analyze_anomalies,
                "analyzeOcr": analyze_ocr,
                "file": self._decode_image(file)}
        return self._make_request("onboarding/add{}".format(operation_type.title()), data, kwargs.get('package_id'))

    def _check_selfie_format(self, selfie_list: List) -> Dict:
        """
        Validates selfies with settings provided in SELFIE_FORMAT_SETTINGS
        :(list) selfie_list: List of selfie_dictionaries with format: {"file": file, "type": type}
        :(list) returns: List of selfies parsed for api usage.
        """
        selfies = []
        if not len(selfie_list):
            raise EmptySelfieListException

        for i in range(len(selfie_list)):
            self._validate_image(selfie_list[i].file, SELFIE_FORMAT_SETTINGS)
            selfies.append(dict(file=self._decode_image(selfie_list[i].file), imageType=selfie_list[i].image_type))

        return selfies

    def _local_scan_response(self, data):
        data['code'] = 5001
        data['message'] = 'Local Scan'
        return data

    @package_id(1)
    @api_call_wrapper(['NEW_OPERATION_OK'])
    def new_operation(self,
                      number: int,
                      gender: str,
                      ip: str,
                      browser_fingerprint: str,
                      **kwargs) -> Dict:
        """
        Initial step of Argentine Government ID Validation.
        :(int) number: Government ID Number
        :(str) gender:  Must be M or F
        :(str) ip: Ip address of client performing API request
        :(str) browser_fingerprint: Fingerprint provided by Renaper's JS library.
        :(int) return: Operation ID used by following methods of validation.
        """
        data = {"number": number,
                "gender": gender,
                "ipAddress": ip,
                "applicationVersion": APPLICATION_VERSION,
                "browserFingerprintData": browser_fingerprint}

        return self._make_request('onboarding/newOperation', data, kwargs.get('package_id'))

    @package_id(1)
    @api_call_wrapper(['ADD_BACK_OK', 'ANALYZE_DOCUMENT_OK'])
    def add_back(self, *args, **kwargs) -> Dict:
        """
        Wrapper function for add_document_image with BACK param
        """
        return self._add_document_image('back', *args, **kwargs)

    @package_id(1)
    @api_call_wrapper(['ADD_FRONT_OK', 'ANALYZE_DOCUMENT_OK'])
    def add_front(self, *args, **kwargs) -> Dict:
        """
        Wrapper function for add_document_image with FRONT param
        """
        return self._add_document_image('front', *args, **kwargs)

    @package_id(1)
    @api_call_wrapper(['ADD_SELFIES_OK'])
    def register(self,
                 operation_id: int,
                 gender: str,
                 number: int,
                 selfie_list: List,
                 **kwargs) -> Dict:
        """
        Registers user selfies.
        :(int) operation_id: Operation id provided by new_operation method
        :(str) gender: Must be M / F
        :(int) number: Government ID number
        :(list) selfie_list: List of selfie_dictionaries with format: {"file": file, "type": type}
        :(str) return:
        """
        selfie_list = self._check_selfie_format(selfie_list)
        data = {"operationId": operation_id,
                "number": number,
                "gender": gender,
                "selfieList": selfie_list}
        return self._make_request('onboarding/register', data, kwargs.get('package_id'))

    @package_id(2)
    @api_call_wrapper(['FACE_COMPARE_OK'])
    def face_login(self,
                   number: int,
                   gender: str,
                   selfie_list: List,
                   browser_fingerprint: str,
                   **kwargs) -> Dict:
        """
        Compares a face selfie to current Renaper record of person.
        :(str) gender: Must be M / F
        :(int) number: Government ID number
        :(list) selfie_list: List of selfie_dictionaries with format: {"file": file, "type": type}
        :(str) browser_fingerprint: Fingerprint provided by Renaper's JS library.
        :(str) return:
        """
        selfie_list = self._check_selfie_format(selfie_list)
        data = {"number": number,
                "gender": gender,
                "selfieList": selfie_list,
                "browserFingerprintData": browser_fingerprint}
        return self._make_request('face/login', data, kwargs.get('package_id'))

    @package_id(1)
    @api_call_wrapper(['END_OPERATION_OK', 'SCORE_SUCCESS', 'ANALYZE_DOCUMENT_OK'])
    def end_operation(self,
                      operation_id: int,
                      number: int,
                      gender: str,
                      **kwargs) -> Dict:
        """
        Ends Government ID Validation
        :(int) operation_id: Operation ID provided by new_operation method
        :(str) gender: Must be M / F
        :(int) number: Government ID number
        :return:
        """
        data = {"operationId": operation_id,
                "number": number,
                "gender": gender}
        return self._make_request('onboarding/endOperation', data, kwargs.get('package_id'))

    @package_id(1)
    @api_call_wrapper(['BARCODE_SCAN_OK'])
    def scan_barcode(self, image_file: str, local: Optional[bool] = False, **kwargs) -> Dict:
        """
        :(base64 imaeg)  image_file: 417 Barcode image.
        :(boolean) local: Attempts to decode the barcode locally.
        :return:
        """
        self._validate_image(image_file, PDF417_FORMAT_SETTINGS if not local else DOCUMENT_FORMAT_SETTINGS)
        if local:
            return self._local_scan_response(self._get_barcode_payload(image_file))
        return self._make_request('onboarding/scanBarcode', {"file": image_file}, kwargs.get('package_id'))

    @package_id(1)
    @api_call_wrapper(['ADD_BARCODE_OK'])
    def add_barcode(self,
                    operation_id: int,
                    number: int,
                    gender: str,
                    image_file: str,
                    **kwargs) -> Dict:
        """
        :(base64 imaeg)  image_file: 417 Barcode image.
        :return:
        """
        self._validate_image(image_file, DOCUMENT_FORMAT_SETTINGS)
        document_data = self._get_barcode_payload(operation_id, image_file)
        data = {"operationId": operation_id,
                "gender": gender,
                "number": number,
                "document": document_data}
        return self._make_request('onboarding/addBarcode', data, kwargs.get('package_id'))

    @package_id(3)
    @api_call_wrapper(['RENAPER_OK_EXITO'])
    def person_data(self,
                    number: int,
                    gender: str,
                    order: int,
                    **kwargs) -> Dict:
        """
        Checks Person data.
        :(str) gender: Must be M / F
        :(int) number: Government ID number
        :(int) order: Goverment ID order number.
        :(dict) returns: Dictionary of person data.
        """
        data = {"number": number,
                "gender": gender,
                "order": order}
        return self._make_request('information/personData', data, kwargs.get('package_id'))

    def status(self):
        """
        Checks service status
        """
        return self._make_request('status', {})
