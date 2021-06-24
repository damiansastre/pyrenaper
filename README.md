# PYRENAPER

---
Argentina's RENAPER (Registro nacional de las personas) python API implementation.

This library provides python shortcuts for RENAPER's API.


## Libraries

---

* [Xzing](https://github.com/zxing/zxing) Required to decode PDF417 Barcode information from ID Images.
* [Java8](https://openjdk.java.net/install/) or higher required by xzing. 
* Python >= 3.9

##Installation

---

```
pip install git+https://github.com/tagercito/pyrenaper
```


# Usage

---

This library implements all of RENAPER packages: 
* **PAQUETE 1**
* **PAQUETE 2**
* **PAQUETE 3**

```
from renaper import Renaper
from renaper.environments import ONBOARDING

renaper = Renaper(ONBOARDING
                  package_1=PACKAGE_1_APIKEY,
                  package_2=PACKAGE_2_APIKEY,
                  package_3=PACKAGE_3_API_KEY)
```
## NOTE:
Packages can be used independently, if only package1 is being used there is no need to provide the rest.

#Package 1

---

This flow implements a full validation of an ID: 
* Front-Back of government ID picture.
* Selfie validation (AKA Proof of live).
* ID's PDF417 Barcode verification. 

##Methods

---


### new_operation
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| ip | str      |  IPV4 or IPV6   |
| browser_fingerprint | str      |  Browser fingerprint returned by REPAPER's JS fingerprint library.   |

```
renaper.new_operation(number, gender, ip, browser_fingerprint)
```


### add_back
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| operation_id      | int | ID provided by [new_operation](###new_operation) |
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| file | base64 encoded image  |  Image of back of ID   |
| analyze_anomalies | boolean (default=False)     |  Whether to analyze anomalize or not  |
| analyze_ocr | boolean(default=False)      | Whether to analyze anomalize or not   |

```
renaper.add_back(operation_id, number, gender, file)
```

### add_front
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| operation_id      | int | ID provided by [new_operation](###new_operation) |
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| file | base64 encoded image  |  Image of back of ID   |
| analyze_anomalies | boolean (default=False)     |  Whether to analyze anomalize or not  |
| analyze_ocr | boolean(default=False)      | Whether to analyze anomalize or not   |

```
renaper.add_front(operation_id, number, gender, file)
```

### register
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| operation_id      | int | ID provided by [new_operation](###new_operation) |
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| selfie_list | list of [Selfie](###Selfie)  |  ```[Selfie(image=BASE_64, type='SN')]```   |

```
renaper.register(operation_id, number, gender, selfie_list)
```

### add_barcode
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| operation_id      | int | ID provided by [new_operation](###new_operation) |
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| image_file | (base64 image)  |  Image of front of ID.   |

```
renaper.add_barcode(operation_id, number, gender, image_file)
```

### end_operation

| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| operation_id      | int | ID provided by [new_operation](###new_operation) |
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |

```
renaper.end_operation(operation_id, number, gender)
```

### Recommended flow

---

 1. new_operation
2. add_back
3. add_front
4. register
5. add_barcode
6. end_operation

#Package 2

---

This flow implements Proof of life.

##Methods

---


### face_login
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| selfie_list | list of [Selfie](###Selfie)  |  ```[Selfie(image=BASE_64, type='SN')]```  |
| browser_fingerprint | str      |  Browser fingerprint returned by REPAPER's JS fingerprint library.   |

```
renaper.face_login(number, gender, selfie_list, browser_fingerprint)
```

#Package 3

---

This flow only validates plain document data and retrieves extra information about it.

##Methods

---


### person_data
| Parameter        | Type           |  Value  |
| ------------- |:-------------:| -----:|
| number      | int | 12392994 |
| gender      | str      |   Must be M or F |
| order | int  |  Order number (tramite) from front of ID |

```
renaper.person_data(number, gender, order)
```


###Responses

All responses follow RENAPER's structure but add methods to check whether the response is valid or not

```
{"status": True / False,
 "message": Original Message returned by RENAPER,
 "code": Renaper status code,
 "code_description": Description to Renaper's status code,
 "response": Original Response.
}
```
TODO: Turn response dictionary into response object.

##Exceptions

---
| Exception        | Description           |
| ------------- |:-------------:|
| **IncorrectImageSize** | File does not meet valid sizes for method ( check documentation ) | 
| **InvalidOperation** | Operation must be *front* or *back* | 
| **EmptySelfieListException**| No selfie provided in list |
| **MissingSelfieFileException**| Selfie object was not instantiated properly |
| **InvalidImage**| Could not decode image file|
| **GeoBlockedRequestException**| Request rejected by Repaper for GEO Reasons|
| **InvalidDomainException**| Domain provided in settings is invalid | 
| **InvalidApiKeyException**| API Key not valid for current request|
| **BarcodeNotFoundException**| Barcode was not found in provided image |
| **IncorrectBarcodeException**| Barcode does not provide ID information |
| **ApiKeyForPackageNotFoundException**| No API_KEY provided for current packages method |
| **InvalidImageFormatException**| Image format should be in accepted list (JPG, JPEG) |
| **InvalidLengthException**| Image length does not fit current requirements | 
| **InvalidHeightException**| Image width does not fit current requirements.| 


## Known Status Codes

---

| Code       | Description           |
| ------------- |:-------------:|
| **901** | NEW_OPERATION_OK |
| **903** | END_OPERATION_OK |
| **904** | END_OPERATION_FAIL |
| **905** | END_OPERATION_EMPTY_FAIL |
| **1905** | OPERATION_END_BARCODE_DOESNT_BELONG |
| **1906** | OPERATION_END_OCR_DOESNT_BELONG |
| **1907** | OPERATION_END_FRONT_BACK_NOT_BELONG |
| **906** | CANCEL_OPERATION_OK |
| **908** | STATUS_OPERATION_OK |
| **909** | ADD_FRONT_OK |
| **911** | FRONT_ALREADY_EXIST |
| **912** | ADD_BACK_OK |
| **914** | BACK_ALREADY_EXIST |
| **915** | ADD_OCR_OK |
| **916** | ADD_OCR_FAIL |
| **920** | ADD_BARCODE_OK |
| **921** | ADD_BARCODE_FAIL |
| **925** | ADD_ANOMALIES_OK |
| **926** | ADD_ANOMALIES_FAIL |
| **932** | ADD_SELFIES_OK |
| **935** | SCORE_EMPTY_FRONT |
| **936** | SCORE_EMPTY_SELFIE |
| **937** | SCORE_SUCCESS |
| **952** | OPERATION_NOT_EXIST |
| **953** | OPERATION_DOESNT_BELONG |
| **954** | OPERATION_DISABLED |
| **960** | IMAGE_NOT_VALID |
| **963** | ANALYZE_DOCUMENT_OK |
| **964** | ANALYZE_DOCUMENT_FAIL |
| **965** | QRCODE_OK |
| **966** | QRCODE_FAILED |
| **967** | END_OPERATION_BARCODE_ORDER_EMPTY |
| **970** | OPERATION_ENDPOINT_CREATE_OBJECT_FAILED |
| **971** | OPERATION_ENDPOINT_BUSINESS_POST_FAILED |
| **972** | FACE_ENDPOINT_CREATE_OBJECT_FAILED |
| **973** | FACE_ENDPOINT_BUSINESS_POST_FAILED |
| **981** | APIKEY_REST_FAILED |
| **990** | END_OPERATION_PERSON_PARSE_FAIL |
| **1000** | INCORRECT_PARAMETERS |
| **1003** | LOGIN_FAIL |
| **1006** | LOGIN_FAIL_CROSSCHECK |
| **1010** | SAVE_IMAGE_TO_STORAGE_FAIL |
| **1011** | LOAD_IMAGE_FROM_STORAGE_FAIL |
| **1013** | ENCRYPTION_FAIL |
| **2001** | FACE_NOT_FOUND |
| **2003** | FACE_COMPARE_OK |
| **2005** | FACE_COMPARE_FAIL |
| **2006** | FACE_SERVICE_FAIL |
| **2023** | FACE_IMAGE_BACKGROUND_ICAO_FAIL |
| **2024** | FACE_IMAGE_ANTISPOOFING_FAIL |
| **2025** | FACE_IMAGE_MONOCHROMATIC_BALANCE_FAIL |
| **2027** | FACE_IMAGE_BACKGROUND_CROSSCHECK_FAIL |
| **2028** | FACE_IMAGE_SCREEN_PLOT_FAIL |
| **2029** | FACE_IMAGE_SCREEN_SWEEP_FAIL |
| **2030** | FACE_IMAGE_FLASHLIGHT_SPOT_FAIL |
| **2031** | FACE_IMAGE_LINES_DETECTION_FAIL |
| **3002** | REGISTER_FAIL |
| **3003** | REGISTER_FAIL_CROSSCHECK |
| **5001** | BARCODE_SCAN_OK |
| **5002** | BARCODE_SCAN_NOT_DETECTED |
| **9100** | IMAGE_SANITIZATION_FAILURE |
| **9200** | BUSINESS_CONFIGURATION_EMPTY |
| **9202** | BUSINESS_CONFIGURATION_SCORE_ONBOARDING_EMPTY |
| **9204** | BUSINESS_CONFIGURATION_SCORE_FACE_EMPTY |
| **9206** | BUSINESS_CONFIGURATION_URL_ENDPOINT_PACKAGE_ONE_EMPTY |
| **9207** | BUSINESS_CONFIGURATION_URL_ENDPOINT_PACKAGE_TWO_EMPTY |
| **9209** | BUSINESS_CONFIGURATION_APIKEY_ENDPOINT_PACKAGE_ONE_EMPTY |
| **9210** | BUSINESS_CONFIGURATION_APIKEY_ENDPOINT_PACKAGE_TWO_EMPTY |
| **9212** | BUSINESS_CONFIGURATION_ENDPOINT_PACKAGE_ONE_OK |
| **9213** | BUSINESS_CONFIGURATION_ENDPOINT_PACKAGE_TWO_OK |
| **9220** | INFORMATION_RENAPER_FAILED |
| **9221** | INFORMATION_RENAPER_SAVE_FAIL |
| **10001** | RENAPER_OK_EXITO |

## Dockerfile

---
There is a Dockerfile included for testing.

```
docker build -t renaper .
docker run -it renaper tests.py
```
#Models

---
###Selfie
| Attribute        | Type           |
| ------------- |:-------------:|
| file | base64 image | 
| type | ```enum(['SN', 'SS', 'SCE', 'SBL', 'SBR'])``` | 


#TODO's

* Increase coverage
* Create response models
* Improve exception handling.