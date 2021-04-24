import json
import logging

import httpx

# Create your views here.
from django.conf import settings
from httpx import Response as httpx_response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class MovieListAPI(APIView):
    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', '')
        url = self.build_url(page=page)
        api_resp = self._get_movie_api_resource(url)
        api_resp = self._validate_external_api_resp(resp=api_resp)
        return Response(data=api_resp.json(), status=api_resp.status_code)

    def _get_movie_api_resource(self, url):
        api_resp = dict()
        retry = True
        for i in range(2):
            if not retry:
                break
            try:
                api_resp = httpx.get(url, auth=(settings.API_USERNAME, settings.API_PASSWORD))

                if not isinstance(api_resp, httpx_response) or api_resp.status_code != status.HTTP_200_OK:
                    logger.error(
                        "Error occurred while requesting for user {} url {}".format(
                            self.request.user.username, url
                        )
                    )
                    raise httpx.RequestError(message="Error occurred", request=api_resp.request)
                retry = False

            except httpx.RequestError as req_err:
                logger.error(
                    "Error occurred while requesting for user {} url {} error {}".format(
                        self.request.user.username, url, req_err
                    )
                )
            if i != 0:
                logger.warning("Retrying {} times for user {} url {}".format(i, self.request.user.username, url))

        return api_resp

    @staticmethod
    def build_url(page) -> str:
        url = settings.MOVIE_API_URL
        if page:
            url = url + '?' + 'page=' + page
        return url

    @staticmethod
    def _validate_external_api_resp(resp):

        fallback_content = json.dumps({
            "error": {
                "message": "Unexpected exception occurred.",
                "code": "api_service_error"
            }
        }
        )

        return resp or httpx_response(content=fallback_content,
                                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
