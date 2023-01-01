from django.shortcuts import render
from .fetch import do_fetch

def landing_page(request):
    

    return render(request, 'base.html')


def fetch_page(request):
    do_fetch()
    return render(request, 'fetch.html')

