from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from item_management.models import Item
from django.contrib.auth import get_user_model

User = get_user_model()


class ItemManagementTests(APITestCase):
    def setUp(self):
        # Create a user and get JWT tokens
        self.user = User.objects.create_user(
            email='testuser@yopmail.com',
            name='Test User',
            password='testpass123',
            password2='testpass123',
        )

        # Add the `is_item_adder` permission to the user and save
        self.user.is_item_adder = True
        self.user.save()

        # Get the JWT token for authentication
        self.tokens = self.get_tokens_for_user(self.user)

        self.item_list_url = reverse('item-list-create')
        self.item_detail_url = lambda pk: reverse('item-retrieve-update-delete', args=[pk])

    def get_tokens_for_user(self, user):
        """
        Helper function to get JWT tokens for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def authenticate(self):
        """
        Helper function to add Authorization header with the JWT access token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens["access"]}')

    def test_create_item_success(self):
        # Authenticate before making the request
        self.authenticate()

        data = {
            'name': 'New Item',
            'description': 'A new item for testing.',
            'quantity': 5,
            'price': 10.99
        }
        response = self.client.post(self.item_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Item created successfully')

        # Verify that the item was created in the database
        item = Item.objects.get(name='New Item')
        self.assertIsNotNone(item)

    def test_create_item_failure_existing_item(self):
        # Authenticate before making the request
        self.authenticate()

        # Create an existing item
        Item.objects.create(name='Existing Item', description='An existing item.', quantity=10, price=19.99)
        data = {
            'name': 'Existing Item',
            'description': 'Trying to create an existing item.',
            'quantity': 10,
            'price': 19.99
        }
        response = self.client.post(self.item_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_list_items_success(self):
        # Authenticate before making the request
        self.authenticate()

        # Create multiple items
        Item.objects.create(name='Item 1', description='First item.', quantity=5, price=9.99)
        Item.objects.create(name='Item 2', description='Second item.', quantity=3, price=19.99)

        response = self.client.get(self.item_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Check that we retrieved both items

    def test_retrieve_item_success(self):
        # Authenticate before making the request
        self.authenticate()

        item = Item.objects.create(name='Item to Retrieve', description='This item will be retrieved.', quantity=2,
                                   price=15.99)
        response = self.client.get(self.item_detail_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], item.name)

    def test_retrieve_item_not_found(self):
        # Authenticate before making the request
        self.authenticate()

        response = self.client.get(self.item_detail_url(9999), format='json')  # Non-existing ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item_success(self):
        # Authenticate before making the request
        self.authenticate()

        item = Item.objects.create(name='Item to Update', description='Update me.', quantity=2, price=25.99)
        data = {
            'name': 'Updated Item',
            'description': 'Updated description.',
            'quantity': 3,
            'price': 30.00
        }
        response = self.client.put(self.item_detail_url(item.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Item')

    def test_delete_item_success(self):
        # Authenticate before making the request
        self.authenticate()

        item = Item.objects.create(name='Item to Delete', description='Delete me.', quantity=1, price=5.00)
        response = self.client.delete(self.item_detail_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(Item.DoesNotExist, Item.objects.get, id=item.id)  # Verify the item is deleted

    def test_delete_item_not_found(self):
        # Authenticate before making the request
        self.authenticate()

        response = self.client.delete(self.item_detail_url(542), format='json')  # Non-existing ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
