from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.property_list, name='property_list'),
]