from django.db.models import Q
from django.shortcuts import render

from .models import Menu


def home(request):
    popular_dishes = Menu.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'popular_dishes': popular_dishes})


def menu_view(request):
    selected_category = request.GET.get('category', '').strip()
    search_query = request.GET.get('q', '').strip()

    dishes = Menu.objects.filter(is_available=True)

    if search_query:
        dishes = dishes.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if selected_category:
        dishes = dishes.filter(category__iexact=selected_category)

    categories_queryset = Menu.objects.filter(is_available=True).exclude(category='')
    if search_query:
        categories_queryset = categories_queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    categories = (
        categories_queryset
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )

    return render(request, 'menu.html', {
        'dishes': dishes,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    })
