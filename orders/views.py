from decimal import Decimal

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from menu.models import Menu


def _get_cart(request):
    return request.session.setdefault('cart', {})


@require_POST
def add_to_cart(request):
    menu_id = request.POST.get('menu_id')
    quantity = request.POST.get('quantity', '1')

    if not menu_id:
        messages.error(request, 'No menu item selected.')
        return redirect('home')

    try:
        menu_item = Menu.objects.get(pk=menu_id)
    except Menu.DoesNotExist:
        messages.error(request, 'Selected menu item was not found.')
        return redirect('home')

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        messages.error(request, 'Please select a valid quantity.')
        return redirect('home')

    cart = _get_cart(request)
    item_key = str(menu_item.id)

    if item_key in cart:
        cart[item_key]['quantity'] += quantity
    else:
        cart[item_key] = {
            'food_name': menu_item.name,
            'price': str(menu_item.price),
            'quantity': quantity,
        }

    cart[item_key]['subtotal'] = str(
        Decimal(str(cart[item_key]['price'])) * Decimal(cart[item_key]['quantity'])
    )

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, 'Added to cart successfully.')
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for item_id, item in cart.items():
        quantity = int(item.get('quantity', 0))
        price = Decimal(str(item.get('price', '0.00')))
        subtotal = Decimal(str(item.get('subtotal', price * quantity)))

        if quantity <= 0:
            continue

        cart_items.append({
            'id': item_id,
            'food_name': item.get('food_name', 'Menu item'),
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })
