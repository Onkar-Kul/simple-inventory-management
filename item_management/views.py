import logging
from django.core.cache import cache
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from item_management.models import Item
from item_management.permissions import IsItemAdder
from item_management.serializers import ItemSerializer

# Get the custom logger for item_management
logger = logging.getLogger('item_management')


class CustomAPIViewMixin:
    def create_response(self, data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        response_data = {
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)


# Create your views here.
class ItemListCreateView(CustomAPIViewMixin, generics.ListCreateAPIView):
    """
            API view for Listing, and Creating Item.
            This view handles GET, POST requests for Listing Items or Creating The Item.
            Permission required to access this view.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            logger.info(f'{self.request.user} is trying to list items.')
            # Allow listing to authenticated users only
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            logger.info(f'{self.request.user} is trying to create a new item.')
            # Allow creation to users with IsItemAdder permission
            self.permission_classes = [IsAuthenticated, IsItemAdder]
        return super(ItemListCreateView, self).get_permissions()

    def list(self, request, *args, **kwargs):
        """
                Handle GET requests to list all Items.
        """

        try:
            cache_key = 'item_list'  # Define a unique cache key for the item list

            # Attempt to get the item list from the cache
            cached_items = cache.get(cache_key)
            if cached_items:
                return self.create_response(data=cached_items, message="Items retrieved from cache.")

            # If not in cache, retrieve from database
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            # Store the serialized data in Redis for future requests
            cache.set(cache_key, serializer.data, timeout=3600)  # Cache for 1 hour
            logger.info('Item list retrieved successfully.')
            return self.create_response(data=serializer.data, message="Items retrieved successfully")
        except Exception as e:
            logger.error(f'Error retrieving item list: {str(e)}')
            return Response({'error': 'Failed to retrieve items'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """
                Handle POST request to create Item
            """

        try:
            data = request.data

            # Check if the item already exists
            if Item.objects.filter(name=data['name']).exists():
                logger.warning(f"Item creation failed: {data['name']} already exists.")
                return Response(
                    {"error": "Item already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # Invalidate the cache for the item list
            cache_key = 'item_list'
            cache.delete(cache_key)
            logger.info(f'Item {serializer.data["name"]} created successfully.')
            return self.create_response(data=serializer.data, message="Item created successfully",
                                        status_code=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'Error creating item: {str(e)}')
            return Response({'error': 'Failed to create item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemsRetrieveUpdateDestroyAPIView(CustomAPIViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
        API view for retrieving, updating, or deleting a Item.
        This view handles GET, PUT/PATCH, and DELETE requests for individual Item.
        Permission required to access this view.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsItemAdder]

    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve a specific Item instance.

            Args:
                request (Request): The request object contains request data.

            Returns:
                Response: A Response object contains the item data and a success message.
        """
        item_id = kwargs.get('pk')
        try:
            cache_key = f'item_{item_id}'  # Define a unique cache key

            # Attempt to get the item from the cache
            cached_item = cache.get(cache_key)
            if cached_item:
                return self.create_response(data=cached_item, message="Item retrieved successfully from Cache")

            instance = self.get_object()
            serializer = self.get_serializer(instance)

            # Store the serialized data in Redis for future requests
            cache.set(cache_key, serializer.data, timeout=3600)
            logger.info(f'Item {item_id} retrieved successfully.')
            return self.create_response(data=serializer.data, message="Item retrieved successfully")
        except Http404:
            logger.warning(f'Item {item_id} not found.')
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error retrieving item {item_id}: {str(e)}')
            return Response({'error': 'Failed to retrieve item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
            Update a specific Item instance.

            Args:
                request (Request): The request object contains updated item.

            Returns:
                Response: A DRF Response object contains the serialized updated item data and a success message.
        """
        item_id = kwargs.get('pk')
        try:
            cache_key = f'item_{item_id}'
            cache_key_for_list = 'item_list'
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # Invalidate the cache if Item gets Updated
            cache.delete(cache_key)
            cache.delete(cache_key_for_list)
            logger.info(f'Item {item_id} updated successfully.')
            return self.create_response(data=serializer.data, message="Item updated successfully")
        except Http404:
            logger.warning(f'Item {item_id} not found for update.')
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error updating item {item_id}: {str(e)}')
            return Response({'error': 'Failed to update item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
           Delete a specific Item.

           Args:
               request (Request): The request object.

           Returns:
               Response: A DRF Response object with a success message and an HTTP 204 status code.
        """
        item_id = kwargs.get('pk')
        try:
            cache_key = f'item_{item_id}'
            cache_key_for_list = 'item_list'
            instance = self.get_object()
            self.perform_destroy(instance)
            # Invalidate the cache if Item gets Deleted
            cache.delete(cache_key)
            cache.delete(cache_key_for_list)
            logger.info(f'Item {item_id} deleted successfully.')
            return self.create_response(message="Item deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Http404:
            logger.warning(f'Item {item_id} not found for deletion.')
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error deleting item {item_id}: {str(e)}')
            return Response({'error': 'Failed to delete item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
