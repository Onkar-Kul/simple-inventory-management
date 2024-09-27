from django.urls import path

from item_management.views import ItemListCreateView, ItemsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ItemListCreateView.as_view(), name='item-list-create'),
    path('<int:pk>/', ItemsRetrieveUpdateDestroyAPIView.as_view(), name='item-retrieve-update-delete'),


]
