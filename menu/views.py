from django.shortcuts import render

from .models import Menu


def home(request):
    popular_dishes = Menu.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'popular_dishes': popular_dishes})


def menu_view(request):
    selected_category = request.GET.get('category', '').strip()
    dishes = Menu.objects.filter(is_available=True)

    if selected_category:
        dishes = dishes.filter(category__iexact=selected_category)

    categories = (
        Menu.objects.filter(is_available=True)
        .exclude(category='')
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )

    return render(request, 'menu.html', {
        'dishes': dishes,
        'categories': categories,
        'selected_category': selected_category,
    })
