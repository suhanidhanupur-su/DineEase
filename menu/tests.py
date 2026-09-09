from django.test import TestCase
from django.urls import reverse


class HomeHeroAndRouteTests(TestCase):
    def test_home_page_has_premium_hero_content(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'GOOD FOOD, GOOD MOOD')
        self.assertContains(response, 'Delicious Food,')
        self.assertContains(response, 'Beautiful Moments')
        self.assertContains(response, 'EXPLORE OUR MENU')
        self.assertContains(response, 'BOOK A TABLE')
        self.assertContains(response, '15+ Signature Dishes')
        self.assertContains(response, '500+ Happy Customers')
        self.assertContains(response, '4.8 Customer Rating')

    def test_menu_and_reservations_routes_exist(self):
        self.assertEqual(reverse('menu'), '/menu/')
        self.assertEqual(reverse('reservations'), '/reservations/')
        self.assertEqual(self.client.get(reverse('menu')).status_code, 200)
        self.assertEqual(self.client.get(reverse('reservations')).status_code, 200)
