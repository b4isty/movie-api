import json
import logging

import httpx

# Create your views here.
from django.conf import settings
from django.db.models import Count
from httpx import Response as httpx_response
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from movies.models import Collection, Movie
from movies.serializers import CollectionSerializer, CollectionUpdateSerializer

logger = logging.getLogger(__name__)


class MovieListAPI(APIView):
    """
    MovieListAPI fetch movie data from external api and sends back to user
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', '')
        url = self.build_url(page=page)
        api_resp = self._get_movie_api_resource(url)
        api_resp = self._validate_external_api_resp(resp=api_resp)
        return Response(data=api_resp.json(), status=api_resp.status_code)

    def _get_movie_api_resource(self, url):
        """
        _get_movie_api_resource private method(meant to be private)  to communicate with external api
        this method directly calls Credy movie API using httpx lib, which also
        supports async http call. The main reason to make it a separate
        method is to make it easier to mock.
        It returns httpx response or blank dict
        """
        api_resp = dict()
        retry = True
        for i in range(2):
            if not retry:
                break
            try:
                # actual api call
                api_resp = httpx.get(url, auth=(settings.API_USERNAME, settings.API_PASSWORD))
                # we raise RequestError if there is any issue with the response
                if not isinstance(api_resp, httpx_response) or api_resp.status_code != status.HTTP_200_OK:
                    logger.error(
                        "Error occurred while requesting for user {} url {}".format(
                            self.request.user.username, url
                        )
                    )
                    raise httpx.RequestError(message="Error occurred", request=api_resp.request)
                # if success we don't want any retry
                retry = False

            except httpx.RequestError as req_err:
                logger.error(
                    "Error occurred while requesting for user {} url {} error {}".format(
                        self.request.user.username, url, req_err
                    )
                )
            if i != 0:
                # log the retry cases(may be for metric)
                logger.warning("Retrying {} times for user {} url {}".format(i, self.request.user.username, url))

        return api_resp

    @staticmethod
    def build_url(page) -> str:
        """
        Build and return the url based on page param
        """
        url = settings.MOVIE_API_URL
        if page:
            url = url + '?' + 'page=' + page
        return url

    @staticmethod
    def _validate_external_api_resp(resp) -> httpx_response:
        """
        Checks for the response and if there is no response value
        or blank, it returns a static fallback httpx Response obj
        """

        fallback_content = json.dumps({
            "error": {
                "message": "Unexpected exception occurred.",
                "code": "api_service_error"
            }
        }
        )

        return resp or httpx_response(content=fallback_content,
                                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionListCreateAPIView(ListCreateAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CollectionSerializer

    def get_queryset(self):
        print(self.request.user)
        qs = Collection.objects.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CollectionUpdateDestroyAPIView(DestroyModelMixin, UpdateAPIView):
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = CollectionUpdateSerializer
    lookup_field = 'collection_uuid'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



