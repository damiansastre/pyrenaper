from pyrenaper.sid import Sid
from pyrenaper.utils import BarcodeReader
import base64
import unittest

PAQUETE1_API_KEY = ''
PAQUETE2_API_KEY = ''
PAQUETE3_API_KEY = ''

TEST_FINGERPRINT = ""
MOCK_URL = 'test_url'

USERNAME = ''
PASSWORD = ''
environment = {"base_url": "https://apirenaper.idear.gov.ar/"}

class SidTest(unittest.TestCase):

    def setUp(self):
        print('asdf')
        self.sid = Sid(environment,
                       username=USERNAME,
                       password=PASSWORD)

    def _test_login(self):
        self.sid.login()

    def _test_basic_user_data(self):
        id_number = ''
        gender = 'M'
        self.sid.login()
        data = self.sid.get_basic_person_data(id_number, gender)
        print(data)
        
    def _test_full_user_data(self):
        id_number = ''
        gender = 'M'
        operation_id = '514030689'
        self.sid.login()
        data = self.sid.get_full_person_data(id_number, gender, operation_id)
        print(data)
        
    def test_barcode(self):
        reader = BarcodeReader()
        with open("mocks/front.jpg", "rb") as image_file:
            encoded_barcode = base64.b64encode(image_file.read())
            data = reader.get_barcode_payload(encoded_barcode)