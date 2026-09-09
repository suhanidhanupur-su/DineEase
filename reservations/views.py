from django.shortcuts import render


def reservations_view(request):
    return render(request, 'reservations.html')
