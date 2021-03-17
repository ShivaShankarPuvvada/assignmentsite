from .views import WishlistCreate, WishlistUpdateDelete, MovieCreate, MovieUpdateDelete, ContainerCreate, ContainerUpdateDelete
from django.urls import path

app_name = 'port'

urlpatterns = [
path("wishlist/create/", WishlistCreate.as_view(), name = "create_wishlist"),
path("wishlists/<int:wishlist_id>", WishlistUpdateDelete.as_view(), name = "update_delete_wishlist"),

path("movie/create/", MovieCreate.as_view(), name = "create_movie"),
path("movies/<int:movie_id>", MovieUpdateDelete.as_view(), name = "update_delete_movie"),

path("container/create/", ContainerCreate.as_view(), name = "create_container"),
path("containers/<int:container_id>", ContainerUpdateDelete.as_view(), name = "update_delete_container"),

]