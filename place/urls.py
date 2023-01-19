from django.urls import path

from .views import *
from facility.views import *

urlpatterns = [
    path('', PlaceListView.as_view(), name="destinations"),
    path('<int:pk>/', PlaceDetailView.as_view(), name="destination"),
    path('<int:pk>/delete', comment_remove, name="destination-delete"),
    path('guide_request/', GuideRequestView.as_view(), name="guide-request"),
    path('search_places', PlaceSearchListView.as_view(), name='search_places'),

]