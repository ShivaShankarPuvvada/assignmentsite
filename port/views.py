from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer


from port.models import Movie, Container, Wishlist
from port.serializers import WishlistSerializer, MovieSerializer, ContainerSerializer

import json

# Create your views here.
class WishlistCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'port/wishlist_list.html'

    def post(self,request):
        try:
            wish_lists = Wishlist.objects.all()
            data=request.data
            must_keys=['name',]
            if bool(set(must_keys)-set(data.keys())):
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)
            serializer = WishlistSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                serializer = WishlistSerializer()
                return Response({'serializer': serializer, 'wishlists': wish_lists}, status=status.HTTP_201_CREATED)
            else:
                serializer = WishlistSerializer()
                return Response({'serializer': serializer, 'wishlists': wish_lists})
        except Exception as error:
            return Response(json.dumps({'Message':error}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            wish_lists = Wishlist.objects.all()
            serializer = WishlistSerializer()
            return Response({'serializer': serializer, 'wishlists': wish_lists})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WishlistUpdateDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'port/wishlist_update_delete_get.html'

    def put(self, request, wishlist_id):
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id) 
            data=request.data
            serializer=WishlistSerializer(wishlist, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return redirect('port:create_wishlist')
            else:
                serializer = WishlistSerializer()
                return Response({'serializer': serializer, 'wishlist': wishlist})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, wishlist_id):
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id)
            wishlist.delete()
            return redirect('port:create_wishlist')
        except Exception as error:
            return Response(json.dumps({'Message': error}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, wishlist_id):
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id)
            serializer =WishlistSerializer(wishlist)
            return Response({'serializer': serializer, 'wishlist': wishlist})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MovieCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'port/movie_list.html'

    def post(self,request):
        try:
            movies = Movie.objects.all()
            data=request.data
            must_keys=['wishlist', 'title', 'url', 'released_date'] # folder is an optional field
            if bool(set(must_keys)-set(data.keys())):
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)

            if data["folder"] != '':
                wish_list_id = data['wishlist']
                folder_id = data['folder']
                c = Container.objects.filter(id = folder_id, wishlist__id = wish_list_id)
                if not c.exists():
                    return Response(json.dumps({'Message': 'This given folder is not in the given wishlist'}),status=status.HTTP_400_BAD_REQUEST)

            serializer = MovieSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                serializer = MovieSerializer()
                return Response({'serializer': serializer, 'movies': movies}, status=status.HTTP_201_CREATED)
            else:
                serializer = MovieSerializer()
                return Response({'serializer': serializer, 'movies': movies})
        except Exception as error:
            return Response(json.dumps({'Message':error}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            movies = Movie.objects.all()
            serializer = MovieSerializer()
            return Response({'serializer': serializer, 'movies': movies})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieUpdateDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'port/movie_update_delete_get.html'

    def put(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id) 
            data=request.data
            serializer=MovieSerializer(movie, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return redirect('port:create_movie')
            else:
                serializer = MovieSerializer()
                return Response({'serializer': serializer, 'movie': movie}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return redirect('port:create_movie')
        except Exception as error:
            return Response(json.dumps({'Message': error}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            serializer =MovieSerializer(movie)
            return Response({'serializer': serializer, 'movie': movie})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContainerCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'port/container_list.html'

    def post(self,request):
        try:
            containers = Container.objects.all()
            data=request.data
            must_keys=['wishlist', 'name',]
            if bool(set(must_keys)-set(data.keys())):
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)
            serializer =  ContainerSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                serializer =  ContainerSerializer()
                return Response({'serializer': serializer, 'containers': containers}, status=status.HTTP_201_CREATED)
            else:
                serializer =  ContainerSerializer()
                return Response({'serializer': serializer, 'containers': containers}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':error}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            containers = Container.objects.all()
            serializer = ContainerSerializer()
            return Response({'serializer': serializer, 'containers': containers})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContainerUpdateDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'port/container_update_delete_get.html'

    def put(self, request, container_id):
        try:
            container = Container.objects.get(id=container_id) 
            data=request.data
            serializer= ContainerSerializer(container, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return redirect('port:create_container')
            else:
                serializer = ContainerSerializer()
                return Response({'serializer': serializer, 'container': container}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, container_id):
        try:
            container = Container.objects.get(id=container_id)
            container.delete()
            return redirect('port:create_container')
        except Exception as error:
            return Response(json.dumps({'Message': error}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, container_id):
        try:
            container = Container.objects.get(id=container_id)
            serializer = ContainerSerializer(container)
            return Response({'serializer': serializer, 'container': container})
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

