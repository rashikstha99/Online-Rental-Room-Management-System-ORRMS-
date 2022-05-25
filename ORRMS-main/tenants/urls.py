from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search_result'),
    path('rent_view', views.rent_view, name='rent_view'),
    path('watchlist_delete/<int:id>', views.watchlist_delete, name='watchlist_delete'),
    path('clear_watchlist/<int:id>', views.clear_watchlist, name='clear_watchlist'),
    path('watchlist', views.watchlist, name='watchlist'),
]
