import uuid
from django.contrib.auth import get_user_model
from django.http.request import QueryDict
from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler,
)

"""
@Author: WSWSCSJ
"""

User = get_user_model()

def argument_check(data, keys):
    result = []
    for key in keys:
        if key not in data.keys():
            result.append(key)
    return result

def SUCCESS_RESPONSE(msg=None):
    if not msg:
        msg = "success"
    return Response(
        data={
            "code": 0,
            "msg": msg,
            "data": []
        }
    )

def EXCEPTION_RESPONSE(exception):
    if not isinstance(exception, str):
        exception = str(exception)
    return Response(
        data={
            "code": 0,
            "msg": exception,
        }
    )

def EXISTS_RESPONSE(value):
    return Response(
        data={
            "code": 1,
            "msg": "{value} exists".format(value=value)
        }
    )

def MISSING_KEY_RESPONSE(keys):
    return Response(
        data={
            "code": 1,
            "msg": "missing key",
            "data": keys,
        }
    )

def EMPTY_RESPONSE():
    return Response(
        data={
            "code": 0,
            "data": [],
        }
    )

def VALUES_RESPONSE(values=None):
    if not values:
        values = []
    return Response(
        data={
            "code": 0,
            "data": values,
            "msg": "success",
        }
    )

def MESSAGE_RESPONSE(code, message):
    return Response(
        data={
            "code": code,
            "msg": message,
            "data": []
        }
    )