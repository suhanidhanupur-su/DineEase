from django.urls import path

from .views import add_to_cart, cart_view, remove_cart_item, update_cart_quantity

urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('update-quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('remove-item/', remove_cart_item, name='remove_cart_item'),
]
