from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from smartsetup.models import (GeneralLedger)
from django.db.models import Max, PositiveIntegerField, Value, Sum, F, Q


class HomeView(TemplateView):
    template_name = 'smartapp/home.html'

# def home(request):
#     return render(request,'smartapp/home.html')


@login_required
def dashboard(request):

    total_revenue = GeneralLedger.objects.filter(
        category_id=1).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_expense = GeneralLedger.objects.filter(
        category_id=2).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_balance = (total_revenue - total_expense)
    # print('RETURNED REVENUE : ', revenues)
    print('TOTAL REVENUE : ', total_revenue)
    print('TOTAL EXPENSES : ', total_expense)
    args = {'total_revenue': total_revenue,
            'total_expense': total_expense, 'total_balance': total_balance}
    # return render (request, 'smartsetup/financialperformance.html',args)

    return render(request, 'smartapp/dashboard.html', args)
