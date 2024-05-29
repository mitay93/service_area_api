from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Polygon
from .models import Provider, ServiceArea


class ProviderTests(APITestCase):
    """
    Provider tests
    """

    def setUp(self):
        self.provider = Provider.objects.create(
            name="Test Provider",
            email="test@example.com",
            phone_number="1234567890",
            language="EN",
            currency="USD"
        )

    def test_list_providers(self):
        url = reverse('providers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_provider(self):
        url = reverse('providers-detail', args=[self.provider.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_provider(self):
        url = reverse('providers-list')
        data = {
            "name": "New Provider",
            "email": "new@example.com",
            "phone_number": "0987654321",
            "language": "EN",
            "currency": "USD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_provider(self):
        url = reverse('providers-detail', args=[self.provider.id])
        data = {
            "name": "Updated Provider",
            "email": "updated@example.com",
            "phone_number": "1234567890",
            "language": "EN",
            "currency": "USD"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_provider(self):
        url = reverse('providers-detail', args=[self.provider.id])
        data = {
            "name": "Partially Updated Provider"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_provider(self):
        url = reverse('providers-detail', args=[self.provider.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ServiceAreaTests(APITestCase):
    """
    Service Area Tests
    The test will work for a Postgresql database, in one of two ways:
    - the database user has superuser privileges
    - the test database was created earlier and has PostGIS extension
    """

    def setUp(self):
        self.provider = Provider.objects.create(
            name="Test Provider",
            email="test@example.com",
            phone_number="1234567890",
            language="EN",
            currency="USD"
        )
        self.service_area = ServiceArea.objects.create(
            name="Test Area",
            price="100.00",
            polygon=Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0))),
            provider=self.provider
        )

    def test_list_service_areas(self):
        url = reverse('service-areas-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_service_area(self):
        url = reverse('service-areas-detail', args=[self.service_area.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_service_area(self):
        url = reverse('service-areas-list')
        data = {
            "name": "New Area",
            "price": "200.00",
            "polygon": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, 20], [20, 20], [20, 0], [0, 0]]]
            },
            "provider": self.provider.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_service_area(self):
        url = reverse('service-areas-detail', args=[self.service_area.id])
        data = {
            "name": "Updated Area",
            "price": "300.00",
            "polygon": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, 30], [30, 30], [30, 0], [0, 0]]]
            },
            "provider": self.provider.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_service_area(self):
        url = reverse('service-areas-detail', args=[self.service_area.id])
        data = {
            "name": "Partially Updated Area"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_service_area(self):
        url = reverse('service-areas-detail', args=[self.service_area.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_service_areas(self):
        url = reverse('service-areas-search')
        params = {
            "lat": 5,
            "lng": 5
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
