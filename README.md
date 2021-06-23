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


#Validation Flows

---
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
| selfie_list | list of [Selfie](###Selfie)  |  Selfie object   |

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



  
## Dockerfile

---
There is a Dockerfile included for testing.

#Models

---
###Selfie
| Attribute        | Type           |
| ------------- |:-------------:|
| file | base64 image | 
| type | ```enum(['SN', 'SS', 'SCE', 'SBL', 'SBR'])``` | 
