from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path(r'^login/$', views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listings/<str:listing_id>", views.view_listing, name="view"),
    path("userlistings/<str:q_user>", views.view_userlistings, name="userlistings"),
    path("watchlist/<str:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view"),
    path("auction/<str:listing_id>", views.auction, name="auction"),
    path("finish_auction/<str:listing_id>", views.stop_auction, name="stop_auction"),
    path("categories",views.categories, name="categories"),
    path("category/<str:category_type>",views.view_category, name="category"),
    
] 

