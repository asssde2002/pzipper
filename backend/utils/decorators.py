from rest_framework import status as DRF_status
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from utils.exceptions import UserError, MissingInputError, AlreadyExistError, InternalServerError, GeneralError
from rest_framework.response import Response
from django.core.cache import caches
import re

from functools import wraps

def DRF_response(func):
    @wraps(func)
    def inner(*args, **kwargs):
        response = {"SUCCESS": True}
        status = DRF_status.HTTP_200_OK

        try:
            payload = func(*args, **kwargs)
            if isinstance(payload, tuple):
                payload, status = payload

            response["PAYLOAD"] = payload
        except (UserError, MissingInputError, AlreadyExistError, GeneralError) as e:
            response = {
                "SUCCESS": False,
                "ERR_MSG": e.get_err_msg(),
            }
            status = DRF_status.HTTP_400_BAD_REQUEST

        except ObjectDoesNotExist as e:
            msg = str(e)
            response = {
                "SUCCESS": False,
                "ERR_MSG": f"Object Does Not Exist Error: {msg}",
            }
            status = DRF_status.HTTP_400_BAD_REQUEST

        except PermissionDenied as e:
            msg = str(e)
            response = {
                "SUCCESS": False,
                "ERR_MSG": f"Permission Denied Error: {msg}",
            }
            status = DRF_status.HTTP_403_FORBIDDEN

        except InternalServerError as e:
            response = {
                "SUCCESS": False,
                "ERR_MSG": e.get_err_msg(),
            }
            status = DRF_status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response, status=status)

    return inner


class Sentinel:
    pass


class RedisTTLCache(object):
    def __init__(self, cache_prefix, timeout=60):
        self.cache_prefix = cache_prefix
        self.timeout = timeout

    @property
    def cache_client(self):
        cache_client = caches["default"]
        return cache_client

    def key(self, key):
        return re.sub(r"[\W]", "", f"{self.cache_prefix}-{key}")

    def __getitem__(self, key):
        s = Sentinel()
        res = self.cache_client.get(self.key(key), s)
        if res == s:
            raise KeyError()

        return res

    def __setitem__(self, key, value):
        return self.cache_client.set(self.key(key), value, timeout=self.timeout)

    def __delitem__(self, key):
        return self.cache_client.delete(self.key(key))