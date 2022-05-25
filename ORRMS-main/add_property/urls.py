from django.urls import path
from . import views

urlpatterns = [
    path('flat/', views.add_property_flat, name='flat_insert'),
    path('room/', views.add_property_room, name='room_insert'),
    path('flat/<int:id>/', views.add_property_flat, name='flat_update'),
    path('room/<int:id>/', views.add_property_room, name='room_update'),
    path('Flat_delete/<int:id>', views.flat_delete, name='flat_delete'),
    path('Room_delete/<int:id>', views.room_delete, name='room_delete'),
    path('Flat_details/<int:id>/', views.flat_details, name='property_details'),
    path('Room_details/<int:id>/', views.room_details, name='room_details'),
    path('location_flat', views.location_flat, name='locationDataFlat'),
    path('location_room', views.location_room, name='locationDataRoom'),
    path('loc/<int:id>/', views.location_single_flat, name='locationSingleFlat'),
    path('loc_room/<int:id>/', views.location_single_room, name='locationSingleRoom'),

]
