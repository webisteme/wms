from rest_framework import status
from rest_framework.test import APITestCase
import json

from .models import Order, OrderLine, SKU, Storage


class OrderTestCase(APITestCase):

    def test_create_order(self):
        """
        Ensure Order can be created via API.
        """
        data = {'customer_name': 'Test Customer 123'}
        response = self.client.post('/api/order/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(
            Order.objects.get().customer_name, 'Test Customer 123')

    def test_read_order(self):
        """
        Ensure Order can be read via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Read the order via API
        response = self.client.get('/api/order/%s/' % order.id, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'id': order.id, 'customer_name': order.customer_name})

    def test_update_order(self):
        """
        Ensure Order can be updated via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Update the order via API
        data = {'customer_name': 'Test Customer 456'}
        response = self.client.put(
            '/api/order/%s/' % order.id, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(
            Order.objects.get().customer_name, 'Test Customer 456')

    def test_delete_order(self):
        """
        Ensure Order can be deleted via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Delete the order via API
        response = self.client.delete(
            '/api/order/%s/' % order.id, format='json')

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class OrderLineTestCase(APITestCase):

    def test_create_order_line(self):
        """
        Ensure OrderLine can be created via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create an order line
        data = {'sku': sku.id, 'quantity': 45, 'order': order.id}
        response = self.client.post('/api/orderline/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderLine.objects.count(), 1)
        self.assertEqual(OrderLine.objects.get().quantity, 45)
        self.assertEqual(OrderLine.objects.get().sku.id, sku.id)
        self.assertEqual(OrderLine.objects.get().order.id, order.id)

    def test_read_order_line(self):
        """
        Ensure OrderLine can be read via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create an order line
        order_line = OrderLine(sku=sku, quantity=11, order=order)
        order_line.save()

        # Read the order line via API
        response = self.client.get(
            '/api/orderline/%s/' % order_line.id, format='json')

        expected_data = {
            'id': order_line.id,
            'sku': sku.id,
            'order': order.id,
            'quantity': 11
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_order_line(self):
        """
        Ensure OrderLine can be updated via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create an order line
        order_line = OrderLine(sku=sku, quantity=45, order=order)
        order_line.save()

        # Create a new order
        new_order = Order(customer_name='Test Customer 123')
        new_order.save()

        # Create a new SKU
        new_sku = SKU(product_name='Test Product 123')
        new_sku.save()

        # Update the order line via API
        data = {'quantity': 30, 'order': new_order.id, 'sku': new_sku.id}
        response = self.client.put(
            '/api/orderline/%s/' % order_line.id, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderLine.objects.count(), 1)
        self.assertEqual(OrderLine.objects.get().quantity, 30)
        self.assertEqual(OrderLine.objects.get().sku.id, new_sku.id)
        self.assertEqual(OrderLine.objects.get().order.id, new_order.id)

    def test_delete_order_line(self):
        """
        Ensure Order can be deleted via API.
        """
        # Create an order
        order = Order(customer_name='Test Customer 123')
        order.save()

        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create an order line
        order_line = OrderLine(sku=sku, quantity=45, order=order)
        order_line.save()

        # Delete the order line via API
        response = self.client.delete(
            '/api/orderline/%s/' % order_line.id, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderLine.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(SKU.objects.count(), 1)


class SKUTestCase(APITestCase):

    def test_create_sku(self):
        """
        Ensure SKU can be created via API.
        """
        data = {'product_name': 'Test SKU 123'}
        response = self.client.post('/api/sku/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SKU.objects.count(), 1)
        self.assertEqual(SKU.objects.get().product_name, 'Test SKU 123')

    def test_read_sku(self):
        """
        Ensure SKU can be read via API.
        """
        # Create an order
        sku = SKU(product_name='Test Customer 123')
        sku.save()

        # Read the order via API
        response = self.client.get('/api/sku/%s/' % sku.id, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'id': sku.id, 'product_name': sku.product_name})

    def test_update_sku(self):
        """
        Ensure SKU can be updated via API.
        """
        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Update the order via API
        data = {'product_name': 'Test Product 456'}
        response = self.client.put(
            '/api/sku/%s/' % sku.id, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SKU.objects.count(), 1)
        self.assertEqual(SKU.objects.get().product_name, 'Test Product 456')

    def test_delete_sku(self):
        """
        Ensure SKU can be deleted via API.
        """
        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Delete the SKU via API
        response = self.client.delete('/api/sku/%s/' % sku.id, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SKU.objects.count(), 0)


class StorageTestCase(APITestCase):

    def test_create_storage(self):
        """
        Ensure Storage can be created via API.
        """
        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create a storage
        data = {'sku': sku.id, 'stock': 127}
        response = self.client.post('/api/storage/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Storage.objects.count(), 1)
        self.assertEqual(Storage.objects.get().stock, 127)
        self.assertEqual(Storage.objects.get().sku.id, sku.id)

    def test_read_storage(self):
        """
        Ensure Storage can be read via API.
        """
        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create a storage
        storage = Storage(sku=sku, stock=88)
        storage.save()

        # Read the order via API
        response = self.client.get(
            '/api/storage/%s/' % storage.id, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'id': storage.id, 'stock': 88, 'sku': sku.id})

    def test_delete_storage(self):
        """
        Ensure Storage can be deleted via API.
        """
        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create a storage
        storage = Storage(sku=sku, stock=17)
        storage.save()

        # Delete the storage via API
        response = self.client.delete(
            '/api/storage/%s/' % storage.id, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Storage.objects.count(), 0)
        self.assertEqual(SKU.objects.count(), 1)

    def test_update_storage(self):
        """
        Ensure Storage can be updated via API.
        """
        # Create an SKU
        sku = SKU(product_name='Test Product 123')
        sku.save()

        # Create a storage
        storage = Storage(sku=sku, stock=70)
        storage.save()

        # Create a new SKU
        new_sku = SKU(product_name='Test Product 123')
        new_sku.save()

        # Update the order line via API
        data = {'stock': 25, 'sku': new_sku.id}
        response = self.client.put(
            '/api/storage/%s/' % storage.id, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Storage.objects.count(), 1)
        self.assertEqual(Storage.objects.get().stock, 25)
        self.assertEqual(Storage.objects.get().sku.id, new_sku.id)


class FulfillmentValidationTestCase(APITestCase):

    def test_only_post_request(self):
        """
        Ensure only POST requests are accepted.
        """
        response = self.client.get('/api/fulfillment/', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['error']['code'], 1)

        response = self.client.put('/api/fulfillment/', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['error']['code'], 1)

        response = self.client.delete('/api/fulfillment/', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['error']['code'], 1)

        response = self.client.post('/api/fulfillment/', {}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 1)

    def test_only_valid_json(self):
        """
        Ensure only valid jason accepted in request body.
        """
        response = self.client.post(
            '/api/fulfillment/', None, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/', {'valid': 'json'}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 2)

    def test_lines_param_required(self):
        """
        Ensure `lines` is a required parameter.
        """
        response = self.client.post(
            '/api/fulfillment/', {'not_lines': []}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/', {'lines': []}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 3)

    def test_lines_not_empty(self):
        """
        Ensure `lines` parameter is not an empty list.
        """
        response = self.client.post(
            '/api/fulfillment/', {'lines': []}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/', {'lines': [{'not': 'empty'}]}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 4)

    def test_lines_is_list(self):
        """
        Ensure `lines` parameter is a list.
        """
        response = self.client.post(
            '/api/fulfillment/', {'lines': 'not a list'}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 5)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/', {'lines': []}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 5)

    def test_line_is_dict(self):
        """
        Ensure every line in `lines` list is dict.
        """
        response = self.client.post(
            '/api/fulfillment/', {'lines': ['not a dict']}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 6)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/', {'lines': [{'a': 'dict'}]}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 6)

    def test_line_keys_required(self):
        """
        Ensure each line dict has required keys.
        """
        response = self.client.post(
            '/api/fulfillment/', {'lines': [{'sku': 'sku'}]}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 7)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': '', 'quantity': ''}]}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 7)

    def test_line_values_integers(self):
        """
        Ensure each line dict value is an integer.
        """
        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': 'str', 'quantity': 'str'}]}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 8)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': 1, 'quantity': -5}]}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 8)

    def test_line_values_positive_integers(self):
        """
        Ensure each line dict value is a positive integer.
        """
        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': -2, 'quantity': -98}]}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 9)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': 1, 'quantity': 5}]}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 9)

    def test_sku_does_not_exist(self):
        """
        Ensure order is not fulfilled if referenced SKUs don't exist.
        """
        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': 1, 'quantity': 2}]}, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['error']['code'], 10)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        sku = SKU(id=1, product_name="Test product 123")
        sku.save()
        response = self.client.post(
            '/api/fulfillment/',
            {'lines': [{'sku': 1, 'quantity': 5}]}, format='json')
        content = json.loads(response.content)
        self.assertNotEqual(content['error']['code'], 10)


class FulfillmentTestCase(APITestCase):

    def test_fulfill_order(self):
        """
        Ensure fulfillment endpoint returns expected picks.
        """
        order_lines = [
            {'sku': 1, 'quantity': 12},
            {'sku': 2, 'quantity': 2}
        ]

        storages = [
            {'sku': 1, 'stock': 5},
            {'sku': 1, 'stock': 100},
            {'sku': 2, 'stock': 100}
        ]

        expected_picks = [
            {'id': 1, 'quantity': 5},
            {'id': 2, 'quantity': 7},
            {'id': 3, 'quantity': 2}
        ]

        # Create order lines, storage, skus
        for s in storages:
            sku, created = SKU.objects.get_or_create(
                id=s['sku'], product_name=s['sku'])
            sku.save()
            storage = Storage(
                id=storages.index(s)+1, sku=sku, stock=s['stock'])
            storage.save()

        # Attempt to fulfill order
        data = {'lines': order_lines}
        response = self.client.post('/api/fulfillment/', data, format='json')

        # Test response
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(content['success'])
        self.assertEqual(content['picks'], expected_picks)

    def test_not_enough_stock(self):
        """
        Ensure fulfillment fails if stock is insufficient.
        """
        order_lines = [
            {'sku': 1, 'quantity': 120},
            {'sku': 2, 'quantity': 2}
        ]

        storages = [
            {'sku': 1, 'stock': 5},
            {'sku': 1, 'stock': 100},
            {'sku': 2, 'stock': 100}
        ]

        # Create order lines, storage, skus
        for s in storages:
            sku, created = SKU.objects.get_or_create(
                id=s['sku'], product_name=s['sku'])
            sku.save()
            storage = Storage(
                id=storages.index(s)+1, sku=sku, stock=s['stock'])
            storage.save()

        # Attempt to fulfill order
        data = {'lines': order_lines}
        response = self.client.post(
            '/api/fulfillment/', data, format='json')

        # Test response
        content = json.loads(response.content)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['error']['code'], 11)

    def test_out_of_stock(self):
        """
        Ensure fulfillment fails if stock is depleted.
        """
        order_lines = [
            {'sku': 1, 'quantity': 120},
            {'sku': 2, 'quantity': 2}
        ]

        storages = [
            {'sku': 1, 'stock': 0},
            {'sku': 1, 'stock': 0},
            {'sku': 2, 'stock': 0}
        ]

        # Create order lines, storage, skus
        for s in storages:
            sku, created = SKU.objects.get_or_create(
                id=s['sku'], product_name=s['sku'])
            sku.save()
            storage = Storage(
                id=storages.index(s)+1, sku=sku, stock=s['stock'])
            storage.save()

        # Attempt to fulfill order
        data = {'lines': order_lines}
        response = self.client.post('/api/fulfillment/', data, format='json')

        # Test response
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['error']['code'], 11)

    def test_no_storages(self):
        """
        Ensure fulfillment fails if no storage exists.
        """
        order_lines = [
            {'sku': 1, 'quantity': 120},
            {'sku': 2, 'quantity': 2}
        ]

        # Create skus
        for s in order_lines:
            sku, created = SKU.objects.get_or_create(
                id=s['sku'], product_name=s['sku'])
            sku.save()

        # Attempt to fulfill order
        data = {'lines': order_lines}
        response = self.client.post('/api/fulfillment/', data, format='json')

        # Test response
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content['error']['code'], 11)


class SearchTestCase(APITestCase):

    def test_search_no_orders(self):
        """
        Ensure search returns no results when if no orders exist.
        """
        response = self.client.get('/api/order/?q=test', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 0)

    def test_search_match(self):
        """
        Ensure search returns matching results.
        """
        order = Order(customer_name="Test customer 123")
        order.save()
        response = self.client.get('/api/order/?q=123', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 1)
        self.assertEqual(
            content['results'][0],
            {'id': 1, 'customer_name': 'Test customer 123'})

    def test_search_no_match(self):
        """
        Ensure search does not return non-matching results.
        """
        order = Order(customer_name="Test customer 123")
        order.save()
        response = self.client.get('/api/order/?q=456', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 0)

    def test_search_not_case_sensitive(self):
        """
        Ensure search is not case-sensitive.
        """
        order = Order(customer_name="Test customer 123")
        order.save()
        response = self.client.get(
            '/api/order/?q=TEST%20CUSTOMER%20123', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 1)
        self.assertEqual(
            content['results'][0],
            {'id': 1, 'customer_name': 'Test customer 123'})

    def test_search_no_accent_match(self):
        """
        Ensure search term without accent matches `customer_name` with accent.
        """
        order = Order(customer_name="Thomas Müller")
        order.save()
        response = self.client.get('/api/order/?q=muller', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 1)
        self.assertEqual(
            content['results'][0],
            {'id': 1, 'customer_name': 'Thomas Müller'})

    def test_search_with_accent_match(self):
        """
        Ensure search term with accent matches `customer_name` with accent.
        """
        order = Order(customer_name="Thomas Müller")
        order.save()
        response = self.client.get('/api/order/?q=müller', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 1)
        self.assertEqual(
            content['results'][0], {'id': 1, 'customer_name': 'Thomas Müller'})

    def test_search_with_accent_no_match(self):
        """
        Ensure search term with accent matches does not match
        `customer_name` without accent.
        """
        order = Order(customer_name="Tom Jones")
        order.save()
        response = self.client.get('/api/order/?q=jönes', {}, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['count'], 0)
