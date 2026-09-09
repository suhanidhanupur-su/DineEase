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


@require_POST
def update_cart_quantity(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity', '1')

    if not product_id:
        return redirect('cart')

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    cart = _get_cart(request)
    item_key = str(product_id)

    if item_key in cart:
        if quantity <= 0:
            cart.pop(item_key, None)
        else:
            cart[item_key]['quantity'] = quantity
            cart[item_key]['subtotal'] = str(
                Decimal(str(cart[item_key]['price'])) * Decimal(quantity)
            )

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


@require_POST
def remove_cart_item(request):
    product_id = request.POST.get('product_id')

    if not product_id:
        return redirect('cart')

    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
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

        menu_item = Menu.objects.filter(pk=item_id).first()
        image_url = menu_item.image.url if menu_item and menu_item.image else ''
        description = menu_item.description if menu_item else item.get('description', '')

        cart_items.append({
            'id': item_id,
            'food_name': item.get('food_name', 'Menu item'),
            'description': description,
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
            'image_url': image_url,
        })
        total += subtotal

    delivery_fee = Decimal('49.00') if total > 0 else Decimal('0.00')
    grand_total = total + delivery_fee

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
    })
