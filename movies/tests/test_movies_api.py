from unittest import mock

from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from faker import Factory

from movies.tests.mocked_methods import mocked_get_movie_api_resource_success, mocked_get_movie_api_resource_failed

MOVIES_URL = reverse('movies:movie_list')

faker = Factory.create()


class MoviesAPITestCase(APITestCase):
    """
    Test MoviesAPI
    endpoint '/movies'
    endpoint alias - 'movies'
    """

    @classmethod
    def setUpClass(cls):
        cls.faker = Factory.create()
        cls.url = MOVIES_URL
        super(MoviesAPITestCase, cls).setUpClass()

    def setUp(self) -> None:
        self.client = APIClient()

    def test_url_is_being_resolved(self):
        """
        Test url resolve
        """
        self.assertEqual(self.url, '/movies/')

    def test_unauthenticated_req_gets_401(self):
        """
        Test It generates correct response code for unauthenticated req
        """
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("movies.views.MovieListAPI._get_movie_api_resource", side_effect=mocked_get_movie_api_resource_failed)
    def test_failed_response_from_external_api(self, patched_method):
        """
        Test mocked scenario if external api somehow fails
        """
        user = baker.make('account.CustomUser')
        self.client.force_authenticate(user=user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", resp.json())

    @mock.patch("movies.views.MovieListAPI._get_movie_api_resource", side_effect=mocked_get_movie_api_resource_success)
    def test_success_response_for_authenticated_request(self, patched_method):
        user = baker.make('account.CustomUser')

        self.client.force_authenticate(user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
