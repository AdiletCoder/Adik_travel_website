from django.urls import path

from facility.views import AddFood, add_hotel
from . import views
from .views import *

from country.views import AddLanguage, AddCountry

urlpatterns = [
    # path('', PlaceListView.as_view(), name="destinations"),
    path('places/', PlaceListView.as_view(), name='m-places'),
    path('places/<int:pk>/', PlaceDetailView.as_view(), name='m-place-detail'),
    path('create/destination/', views.add_destination, name='add-place'),
    path('add/language/', AddLanguage.as_view(), name='add-language'),
    path('add/country/', AddCountry.as_view(), name='add-country'),
    path('add/food/', AddFood.as_view(), name='add-food'),
    path('add/hotel/', add_hotel, name='add-hotel'),
    path('places/<int:pk>/delete/', PlaceDeleteView.as_view(), name='m-place-delete'),
    path('places/<int:pk>/edit/', PlaceUpdateView.as_view(), name='m-place-edit'),
    path('guide-requests/', approve_guide, name='m-approve-guide'),
    path('bloggers/', BloggerListView.as_view(), name='m-bloggers'),
    path('bloggers/<int:pk>/', BloggerDeleteView.as_view(), name='m-blogger-delete'),
    path('guides/', GuideListView.as_view(), name='m-guides'),
    path('guides/<int:pk>/', GuideDeleteView.as_view(), name='m-guide-delete'),
]