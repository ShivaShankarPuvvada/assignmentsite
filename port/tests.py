from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from port.models import Movie, Container, Wishlist
from port.serializers import WishlistSerializer, MovieSerializer, ContainerSerializer


class WishlistCreateTests(APITestCase):

# class: WishlistCreate
# method:Post


    def test_can_create_wishlist(self):
        url = reverse('port:create_wishlist')
        data =  {
                            "name":'my youtube videos',
                        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.filter(name='my youtube videos').exists(), True)
