from django.test import TestCase
from django.urls import reverse

from menu.models import Menu


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

    def test_menu_page_loads_dynamic_dishes_and_categories(self):
        Menu.objects.create(
            name='Truffle Pasta',
            description='Creamy truffle pasta with parmesan.',
            price='499.00',
            category='Pasta',
            is_available=True,
        )
        Menu.objects.create(
            name='Crispy Tacos',
            description='Fresh tacos with zesty salsa.',
            price='299.00',
            category='Starters',
            is_available=True,
        )
        Menu.objects.create(
            name='Classic Cheesecake',
            description='Velvety cheesecake with berry compote.',
            price='249.00',
            category='Desserts',
            is_available=False,
        )

        response = self.client.get(reverse('menu'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Our Menu')
        self.assertContains(response, 'Explore our delicious selection of freshly prepared dishes, crafted to make every meal memorable.')
        self.assertContains(response, 'Truffle Pasta')
        self.assertContains(response, 'Crispy Tacos')
        self.assertNotContains(response, 'Classic Cheesecake')
        self.assertContains(response, 'All')
        self.assertContains(response, 'Pasta')
        self.assertContains(response, 'Starters')

    def test_menu_search_filters_dishes_by_keyword(self):
        Menu.objects.create(
            name='Truffle Pasta',
            description='Creamy truffle pasta with parmesan.',
            price='499.00',
            category='Pasta',
            is_available=True,
        )
        Menu.objects.create(
            name='Crispy Tacos',
            description='Fresh tacos with zesty salsa.',
            price='299.00',
            category='Starters',
            is_available=True,
        )

        response = self.client.get(reverse('menu'), {'q': 'taco'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search dishes...')
        self.assertContains(response, 'Crispy Tacos')
        self.assertNotContains(response, 'Truffle Pasta')
