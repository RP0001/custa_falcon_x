from django.shortcuts import render
from django.http import HttpResponse


# Index/about/home page.
def about(request):
    return render(request, 'custa/about.html')
