from functools import wraps
from .models import RenaperResponse
import os
import uuid

def api_call_wrapper(valid_status):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = f(*args, **kwargs)
            return RenaperResponse(data, valid_status)
        return wrapper
    return decorator



def package_id(package_id):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, package_id=package_id, **kwargs)
        return wrapper
    return decorator


def clean_files(func):
    def wrapper(self, data, format):
        image_name= str(uuid.uuid4())
        try:
            data = func(self, data, image_name, format)
            return data
        except Exception as e:
            raise e
        finally:
            try:
                os.remove('{}.{}'.format(image_name, format))
            except:
                pass
    return wrapper
