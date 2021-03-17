from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from port.models import Movie, Container, Wishlist
from port.serializers import WishlistSerializer, MovieSerializer, ContainerSerializer


class WishlistCreateTests(APITestCase):

# class: WishlistCreate
# method:Post


    def test_can_create_wishlist(self):
        url = reverse('create_wishlist')
        data =  {
                            "name":'my youtube videos',
                        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.filter(name='my youtube videos').exists(), True)

    def test_cannot_create_wishlist_if_required_fields_missed(self):
        url = reverse('create_wishlist')
        data =  {
                            "id":'name field must exist in order to save the wishlist',
                        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Wishlist.objects.filter(name='my youtube videos').exists(), False)


    def test_cannot_create_wishlist_if_data_type_is_wrong(self):
        url = reverse('create_wishlist')
        data =  {
                            "name": 1,
                        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Wishlist.objects.filter(name='my youtube videos').exists(), True)