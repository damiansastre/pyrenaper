from pyrenaper.exceptions import IncorrectBarcodeException, BarcodeNotFoundException
from pyrenaper.decorators import clean_files
from typing import Optional, Dict, List
from PIL import Image
from io import BytesIO
import base64
import zxing

class BarcodeReader:

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
    def get_barcode_payload(self, image: str, image_name: str) -> Dict:
        """
        DEPRECATED
        Extracts information from Argentina's PDF417 Qr Code.
        :(base64 img) image: Image containing Argentina's Government PDF417 QR Code.
        :return:
        """
        filename = '{}.jpg'.format(image_name)
        np_img = Image.open(BytesIO(base64.b64decode(image)))
        np_img.save(filename)
        reader = zxing.BarCodeReader()
        barcode = reader.decode(filename)
        if not barcode:
            raise BarcodeNotFoundException
        return self._parse_barcode(barcode.parsed)