from pyrenaper.renaper import Renaper
from pyrenaper.mocks.response import MockResponse
from environments import ONBOARDING
from exceptions import GeoBlockedRequestException, ApiKeyForPackageNotFoundException, InvalidImage
import base64
import unittest

PAQUETE1_API_KEY = ''
PAQUETE2_API_KEY = ''
PAQUETE3_API_KEY = ''

TEST_FINGERPRINT = ""
MOCK_URL = 'test_url'

class RenaperTest(unittest.TestCase):

    def setUp(self):
        self.environment = ONBOARDING
        self.renaper = Renaper(self.environment,
                               package1_apikey=PAQUETE1_API_KEY,
                               package2_apikey=PAQUETE2_API_KEY,
                               package3_apikey=PAQUETE3_API_KEY)

    def test_get_error_code_500(self):
        response = MockResponse(status_code=500, json_data={})
        with self.assertRaises(Exception) as context:
            self.renaper._get_error_code(response)
        self.assertEqual('500 status code returned', context.exception.__str__())

    def test_get_error_code_renaper(self):
        response = MockResponse(status_code=444, json_data={})
        with self.assertRaises(GeoBlockedRequestException) as context:
            self.renaper._get_error_code(response)

    def test_get_error_code_bad_request(self):
        response = MockResponse(status_code=400, json_data={})
        data = self.renaper._get_error_code(response)
        self.assertIn('error', data)

    def test_get_requests_headers_invalid_package_id(self):
        package_id = 4
        with self.assertRaises(ApiKeyForPackageNotFoundException) as context:
            self.renaper._get_request_headers(MOCK_URL, package_id)

    def test_get_requests_headers_valid(self):
        package_id = 1
        data = self.renaper._get_request_headers(MOCK_URL, package_id)
        self.assertIn('apiKey', data)
        self.assertIn('url', data)

    def test_validate_image_format_nonimage(self):
        image = 'NOTABASE64IMAGE'
        with self.assertRaises(InvalidImage) as context:
            self.renaper._validate_image(image, {})

    def atest_person_data(self):
        number = ""
        gender = ""
        order = ""
        data = self.renaper.person_data(number, gender, order)
        self.assertTrue(data['status'])
        self.assertEqual(data['message'], 'Exito')

    def atest_invalid_person_data(self):
        number = ""
        gender = ""
        order = ""
        data = self.renaper.person_data(number, gender, order)
        self.assertFalse(data['status'])
        self.assertIn('error', data)

    def test_package1(self):
        number = ""
        gender = ""
        ip = ''
        data = self.renaper.new_operation(number, gender, ip, TEST_FINGERPRINT)
        self.assertTrue(data['status'])
        self.assertIn('operationId', data['response'])
        self.assertEqual(data['code_description'], 'NEW_OPERATION_OK')
        operation_id = data['response']['operationId']
        with open("mocks/front.jpg", "rb") as image_file:
            encoded_front = base64.b64encode(image_file.read())
        data = self.renaper.add_front(operation_id, number, gender, encoded_front)
        self.assertTrue(data['status'])
        self.assertEqual(data['code_description'], 'ADD_FRONT_OK')
        with open("mocks/back.jpg", "rb") as image_file:
            encoded_back = base64.b64encode(image_file.read())
        data = self.renaper.add_back(operation_id, number, gender, encoded_back)
        self.assertTrue(data['status'])
        self.assertEqual(data['code_description'], 'ADD_BACK_OK')
        with open("mocks/front.jpg", "rb") as image_file:
            encoded_barcode = base64.b64encode(image_file.read())
        data = self.renaper.add_barcode(operation_id, number, gender, encoded_barcode)
        self.assertTrue(data['status'])
        self.assertEqual(data['code_description'], 'ADD_BARCODE_OK')
        with open("mocks/selfie.jpg", "rb") as image_file:
            encoded_selfie = base64.b64encode(image_file.read())
        selfie_list = {"file": encoded_selfie, "type": "SN"}
        data = self.renaper.register(operation_id, gender, number, [selfie_list])
        self.assertTrue(data['status'])
        self.assertEqual(data['code_description'], 'ADD_SELFIES_OK')
        data = self.renaper.end_operation(operation_id, number, gender)
        self.assertTrue(data['status'])
        self.assertEqual(data['code_description'], 'END_OPERATION_OK')

    def atest_package2(self):
        with open("mocks/selfie.jpg", "rb") as image_file:
            encoded_selfie = base64.b64encode(image_file.read())
        selfie_list = {"file": encoded_selfie, "type": "SN"}
        number = ""
        gender = ""
        data = self.renaper.face_login(number, gender, [selfie_list], TEST_FINGERPRINT)
        self.assertTrue(data['status'])

    def test_package3(self):
        number = ""
        gender = ""
        order = ''
        data = self.renaper.person_data(number, gender, order)
        self.assertTrue(data['status'])
        self.assertEqual(data['code_description'], 'RENAPER_OK_EXITO')
