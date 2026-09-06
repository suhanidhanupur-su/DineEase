from django.shortcuts import render
from .models import Menu


def home(request):
	popular_dishes = Menu.objects.filter(is_available=True)[:6]
	return render(request, 'home.html', {'popular_dishes': popular_dishes})
