from rest_framework import status as DRF_status
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from utils.exceptions import UserError, MissingInputError, AlreadyExistError, InternalServerError
from rest_framework.response import Response

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
        except (UserError, MissingInputError, AlreadyExistError) as e:
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