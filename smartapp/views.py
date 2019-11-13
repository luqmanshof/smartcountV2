from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'smartapp/home.html'

# def home(request):
#     return render(request,'smartapp/home.html')


@login_required
def dashboard(request):
    return render(request, 'smartapp/dashboard.html')
