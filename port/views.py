from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from port.models import Movie, Container, Wishlist
from port.serializers import WishlistSerializer, MovieSerializer, ContainerSerializer

import json

# Create your views here.
class WishlistCreate(APIView):

    def post(self,request):
        try:
            data=request.data
            must_keys=['name',]
            if bool(set(must_keys)-set(data.keys())):
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)
            serializer = WishlistSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                resp={
                    'data':serializer.data,
                }
                return Response(resp,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':error}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            wish_lists = Wishlist.objects.all()
            total_data=[]
            resp={}
            for each in wish_lists:
                data =WishlistSerializer(each)
                total_data.append(data.data)
            resp['data']=total_data
            return Response(data=resp,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WishlistUpdateDelete(APIView):

    def put(self, request, wishlist_id):
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id) 
            data=request.data
            serializer=WishlistSerializer(wishlist, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                resp = {
                    'data': serializer.data,
                }
                return Response(resp, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, wishlist_id):
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id)
            wishlist.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response(json.dumps({'Message': error}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, wishlist_id):
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id)
            data =WishlistSerializer(wishlist)
            resp = {}
            resp['data'] = data.data
            return Response(data=resp, status = status.HTTP_200_OK)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MovieCreate(APIView):

    def post(self,request):
        try:
            data=request.data
            must_keys=['wishlist', 'title', 'url', 'released_date'] # folder is an optional field
            if bool(set(must_keys)-set(data.keys())):
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)
            if "folder" in data:
                wish_list_id = data['wishlist']
                folder_id = data['folder']
                c = Container.objects.filter(id = folder_id, wishlist__id = wish_list_id)
                if not c.exists():
                    return Response(json.dumps({'Message': 'This given folder is not in the given wishlist'}),status=status.HTTP_400_BAD_REQUEST)
            serializer = MovieSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                resp={
                    'data':serializer.data,
                }
                return Response(resp,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':error}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            movies = Movie.objects.all()
            total_data=[]
            resp={}
            for each in movies:
                data =MovieSerializer(each)
                total_data.append(data.data)
            resp['data']=total_data
            return Response(data=resp,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieUpdateDelete(APIView):

    def put(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id) 
            data=request.data
            serializer=MovieSerializer(movie, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                resp = {
                    'data': serializer.data,
                }
                return Response(resp, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response(json.dumps({'Message': error}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            data =MovieSerializer(movie)
            resp = {}
            resp['data'] = data.data
            return Response(data=resp, status = status.HTTP_200_OK)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContainerCreate(APIView):

    def post(self,request):
        try:
            data=request.data
            must_keys=['wishlist', 'name',]
            if bool(set(must_keys)-set(data.keys())):
                return Response({'Message':str(set(must_keys)-set(data.keys()))+" missing"},status=status.HTTP_400_BAD_REQUEST)
            serializer =  ContainerSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                resp={
                    'data':serializer.data,
                }
                return Response(resp,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message':error}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            containers = Container.objects.all()
            total_data=[]
            resp={}
            for each in containers:
                data = ContainerSerializer(each)
                total_data.append(data.data)
            resp['data']=total_data
            return Response(data=resp,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContainerUpdateDelete(APIView):

    def put(self, request, container_id):
        try:
            container = Container.objects.get(id=container_id) 
            data=request.data
            serializer= ContainerSerializer(container, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                resp = {
                    'data': serializer.data,
                }
                return Response(resp, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, container_id):
        try:
            container = Container.objects.get(id=container_id)
            container.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response(json.dumps({'Message': error}), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, container_id):
        try:
            container = Container.objects.get(id=container_id)
            data = ContainerSerializer(container)
            resp = {}
            resp['data'] = data.data
            return Response(data=resp, status = status.HTTP_200_OK)
        except Exception as error:
            return Response(json.dumps({'Message': 'Internal Server Error'}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

