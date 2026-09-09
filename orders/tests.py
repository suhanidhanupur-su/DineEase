from django.test import TestCase
from django.urls import reverse

from menu.models import Menu


class CartSessionTests(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            name='Butter Chicken',
            description='Creamy and rich.',
            price='299.00',
            category='Main Course',
            is_available=True,
        )

    def test_add_to_cart_updates_session(self):
        response = self.client.post(
            reverse('add_to_cart'),
            {'menu_id': self.menu_item.id, 'quantity': 2},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        cart = self.client.session.get('cart', {})
        self.assertIn(str(self.menu_item.id), cart)
        self.assertEqual(cart[str(self.menu_item.id)]['quantity'], 2)
        self.assertEqual(str(cart[str(self.menu_item.id)]['price']), '299.00')

    def test_cart_view_shows_selected_item(self):
        session = self.client.session
        session['cart'] = {
            str(self.menu_item.id): {
                'food_name': self.menu_item.name,
                'price': str(self.menu_item.price),
                'quantity': 1,
                'subtotal': '299.00',
            }
        }
        session.save()

        response = self.client.get(reverse('cart'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Butter Chicken')
        self.assertContains(response, '299.00')
        self.assertContains(response, 'Your Cart')
        self.assertContains(response, 'Order Summary')

    def test_cart_quantity_and_remove_routes_exist(self):
        self.assertEqual(reverse('update_cart_quantity'), '/orders/update-quantity/')
        self.assertEqual(reverse('remove_cart_item'), '/orders/remove-item/')
