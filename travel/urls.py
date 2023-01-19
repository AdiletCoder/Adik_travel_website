from django.urls import path
from travel.views import home_page, create_trip, MyTripDeleteView, trip_service, trip_guide, GroupListView, TripUpdateView

urlpatterns = [
    path('', home_page, name='home'),
    path('trips/<int:pk>/create', create_trip, name='trip-create'),
    path('trips/<int:pk>/update', TripUpdateView.as_view(), name='trip-update'),
    path('trips/<int:pk>/', MyTripDeleteView.as_view(), name='trip-delete'),
    path('trips/<int:pk>/services', trip_service, name='trip-service'),
    path('trips/<int:pk>/guide', trip_guide, name='trip-guide'),
    path('groups/', GroupListView.as_view(), name='groups'),
]
