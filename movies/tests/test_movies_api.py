from unittest import mock

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
        self.assertEqual(self.url, '/movies')

    @mock.patch("movies.views.MovieListAPI._get_movie_api_resource", side_effect=mocked_get_movie_api_resource_failed)
    def test_failed_response(self, patched_method):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", resp.json())

    @mock.patch("movies.views.MovieListAPI._get_movie_api_resource", side_effect=mocked_get_movie_api_resource_success)
    def test_success_response(self, patched_method):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('result', resp.json())

