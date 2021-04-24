import json

from httpx import Response as httpx_response
from rest_framework import status

from movies.tests.dummy_data import MOVIE_API_DUMMY_RESP


def mocked_get_movie_api_resource_failed(url=''):
    return {}


def mocked_get_movie_api_resource_success(url=''):
    return httpx_response(content=json.dumps(MOVIE_API_DUMMY_RESP),
                          status_code=status.HTTP_200_OK)
