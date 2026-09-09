from django.shortcuts import render

from .models import Menu


def home(request):
    popular_dishes = Menu.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'popular_dishes': popular_dishes})


def menu_view(request):
    dishes = Menu.objects.filter(is_available=True)
    return render(request, 'menu.html', {'dishes': dishes})
