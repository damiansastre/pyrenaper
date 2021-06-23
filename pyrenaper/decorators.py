from functools import wraps
from settings import STATUS_CODES
import os


def api_call_wrapper(valid_status):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = f(*args, **kwargs)
            if data.get('code'):
                if STATUS_CODES.get(data['code']):
                    if STATUS_CODES[data['code']] in valid_status:
                        message = data.pop('message')
                        code = data.pop('code')
                        return {"status": True,
                                "message": message,
                                'code': code,
                                'code_description': STATUS_CODES[code],
                                "response": data}

            if data.get('error'):
                code = data['error'].pop('code')
                description = STATUS_CODES.get(data['error']['code'])
                code_description = description if description else 'Unknown'
                return {"status": False,
                        'code': code,
                        'code_description': code_description,
                        "error": data['error']}

            return {"status": False,
                    "data": data}
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
    def wrapper(self, operation_id, data):
        try:
            data = func(self, operation_id, data)
            return data
        except Exception as e:
            raise e
        finally:
            try:
                os.remove('{}.jpg'.format(operation_id))
            except:
                pass
    return wrapper