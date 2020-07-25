import json as simplejson
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import (ChartCategory, ChartSubCategory, ChartNoteItems, SetupClients, SetupVendors,
                     SetupInventoryCategory, SetupInventoryItems, SetupClients, SetupVendors,
                     ReceiptMain, ReceiptDetails, ExpenseMain, ExpenseDetails, GJournalMain,
                     GJournalDetails, GeneralLedger, SetupFixedAssets, SetupBegbalanceDetails,
                     SetupBegBalanceMain, PurchaseMain, PurchaseDetails, BudgetMain, BudgetDetails)
from django.db.models import Max, PositiveIntegerField, Value, Sum


class ChartNoteItem(ListView):
    model = ChartNoteItems
    template_name = 'smartsetup/chartnoteitem.html'
    context_object_name = 'noteitems'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category
        context['sub_category'] = ChartSubCategory.objects.all().order_by(
            'sub_category_name')

        return context


class CreateNoteItem(View):
    def get(self, request):

        name1 = request.GET.get('item_name', None)
        revenue1 = request.GET.get('sub_category', None)

        print(revenue1)

        obj = ChartNoteItems.objects.create(
            item_name=name1,
            sub_category=revenue1
        )

        item = {'id': obj.id, 'item_name': obj.item_name,
                'sub_category': obj.sub_category}

        data = {
            'item': item
        }
        return JsonResponse(data)


# def chartnote_filter(request):
#     notes = request.GET.get('notes', None)
#     print(notes)
#     data = {
#         'is_taken': ChartSubCategory.objects.filter(notes__iexact=notes).exists()
#     }
#     return JsonResponse(data)


def list_filter(request):
    if request.method == "GET" and request.is_ajax():
        category = request.GET.get('category', None)
        # item = ChartNoteItems.objects.get(sub_category=category)
        # item = ChartNoteItems.objects.get(sub_category=category)
        # item_list = serializers.serialize(
        #     "xml", ChartNoteItems.objects.filter(sub_category=category))
        # print(category)
        # print('###')
        # # print(item)
        # print('###')
        # print(item_list)

        try:
            # item_list = serializers.serialize(
            #     "xml", ChartNoteItems.objects.filter(sub_category=category))

            item_list = serializers.serialize(
                "json", ChartNoteItems.objects.filter(sub_category=category))

            data = {
                'List_Record': item_list
            }
            return JsonResponse(data)

        except:
            return JsonResponse({"success": False}, status=400)

    return JsonResponse({"success": False}, status=400)


class UpdateNoteItem(View):
    def get(self, request):
        print('Code executed')

        id1 = request.GET.get('id', None)
        name1 = request.GET.get('item_name', None)
        sub_category1 = request.GET.get('sub_category', None)

        print(id1)
        print(sub_category1)
        print(name1)

        obj = ChartNoteItems.objects.get(id=id1)
        obj.item_name = name1
        obj.sub_category = sub_category1
        obj.save()

        item = {'id': obj.id, 'item_name': obj.item_name,
                'sub_category': obj.sub_category}

        data = {
            'item': item
        }
        return JsonResponse(data)


class DeleteNoteItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        ChartNoteItems.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteRececiptItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        pk = request.GET.get('mainID', None)
        receipt_number = request.GET.get('receipt_number', None)
        description = ReceiptDetails.objects.get(id=id1).description
        amount = ReceiptDetails.objects.get(id=id1).amount

        ReceiptDetails.objects.get(id=id1).delete()
        GeneralLedger.objects.get(credit=amount, description=description,
                                  ref_number=receipt_number, journal_type='CRJ', main_Trans=False).delete()

        # get the sum of the receipt detail values
        total_sum = ReceiptDetails.objects.filter(
            receipt_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00

        # Update Cash receipt journal total credit value
        total_amount = float(total_sum)
        obj3 = GeneralLedger.objects.get(
            ref_number=receipt_number, journal_type='CRJ', main_Trans=True)
        obj3.credit = total_amount
        obj3.save()

        # Get the cash receipt journal items
        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=receipt_number, journal_type='CRJ'))

        journal_list1 = GeneralLedger.objects.filter(
            ref_number=receipt_number, journal_type='CRJ')
        print('JOURNAL LIST RETRIEVED : ', journal_list1)

        data = {
            'deleted': True,
            'total_sum': total_sum,
            'journal_list': journal_list,
        }
        return JsonResponse(data)


class DeleteRececipt(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        ref_number1 = ReceiptMain.objects.get(id=id1).receipt_number
        GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='CRJ').delete()

        ReceiptMain.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteBudget(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        BudgetMain.objects.get(id=id1).delete()

        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteBudgetItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        pk = request.GET.get('mainID', None)
        voucher_number = request.GET.get('voucher_number', None)
        description = BudgetDetails.objects.get(id=id1).description
        amount = BudgetDetails.objects.get(id=id1).amount

        BudgetDetails.objects.get(id=id1).delete()
        total_sum = BudgetDetails.objects.filter(
            budget_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00

        total_amount = float(total_sum)

        data = {
            'deleted': True,
            'total_sum': total_sum,
            # 'journal_list': journal_list,
        }
        return JsonResponse(data)


# For Expense Module
def get_budgetexp(request):

    if request.method == 'GET' and request.is_ajax():
        item_code = request.GET.get('item_code', None)
        print('ITEM CODE IS:', item_code)
        budget_exp = BudgetDetails.objects.get(
            id=item_code).budget_item_id
        print('BUDGET ITEM ACCOUNT IS:', budget_exp)
        acct_exp = ChartNoteItems.objects.filter(id=budget_exp).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        print('Selected Category Items is: ', acct_exp)

        data = dict(values=list(acct_exp))
        print('CONVERTED DATA Items is: ', data)
        return JsonResponse(data)

    else:
        return redirect('/')


class DeleteExpense(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        ref_number1 = ExpenseMain.objects.get(id=id1).voucher_number
        GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='CDJ').delete()

        ExpenseMain.objects.get(id=id1).delete()

        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteExpenseItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        pk = request.GET.get('mainID', None)
        voucher_number = request.GET.get('voucher_number', None)
        description = ExpenseDetails.objects.get(id=id1).description
        amount = ExpenseDetails.objects.get(id=id1).amount

        ExpenseDetails.objects.get(id=id1).delete()
        GeneralLedger.objects.filter(debit=amount, description=description,
                                  ref_number=voucher_number, journal_type='CDJ', main_Trans=False).delete()

        # get the sum of the receipt detail values
        total_sum = ExpenseDetails.objects.filter(
            expense_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00

        # Update Cash receipt journal total credit value
        total_amount = float(total_sum)
        obj3 = GeneralLedger.objects.get(
            ref_number=voucher_number, journal_type='CDJ', main_Trans=True)
        obj3.credit = total_amount
        obj3.save()

        # Get the cash receipt journal items
        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number, journal_type='CDJ'))

        journal_list1 = GeneralLedger.objects.filter(
            ref_number=voucher_number, journal_type='CDJ')
        print('JOURNAL LIST RETRIEVED : ', journal_list1)

        data = {
            'deleted': True,
            'total_sum': total_sum,
            'journal_list': journal_list,
        }
        return JsonResponse(data)


class DeleteGJournal(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        ref_number1 = GJournalMain.objects.get(id=id1).ref_number
        GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='GJ').delete()

        GJournalMain.objects.get(id=id1).delete()

        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteGJournalItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        pk = request.GET.get('mainID', None)
        voucher_number = request.GET.get('voucher_number', None)
        description = GJournalDetails.objects.get(id=id1).description
        debit = GJournalDetails.objects.get(id=id1).debit
        credit = GJournalDetails.objects.get(id=id1).credit

        GJournalDetails.objects.get(id=id1).delete()
        GeneralLedger.objects.get(debit=debit, credit=credit, description=description,
                                  ref_number=voucher_number, journal_type='GJ', main_Trans=False).delete()

        # get the sum of the receipt detail values
        total_debit = GJournalDetails.objects.filter(
            journal_main_id_id=pk).aggregate(Sum('debit'))['debit__sum'] or 0.00
        total_credit = GJournalDetails.objects.filter(
            journal_main_id_id=pk).aggregate(Sum('credit'))['credit__sum'] or 0.00

        # Get the cash receipt journal items
        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number, journal_type='GJ'))

        data = {
            'deleted': True,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'journal_list': journal_list,
        }
        return JsonResponse(data)


class UnpostGJournal(View):
    def get(self, request):
        voucher_number = request.GET.get('voucher_number', None)

        GeneralLedger.objects.filter(
            ref_number=voucher_number, journal_type='GJ').delete()

        # Get the posted journal items
        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number, journal_type='GJ'))

        data = {
            'deleted': True,
            'journal_list': journal_list,
        }
        return JsonResponse(data)


class DeleteBegBalanceItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        pk = request.GET.get('mainID', None)
        period_number = request.GET.get('period_number', None)
        description = SetupBegbalanceDetails.objects.get(id=id1).description
        debit = SetupBegbalanceDetails.objects.get(id=id1).debit
        credit = SetupBegbalanceDetails.objects.get(id=id1).credit

        SetupBegbalanceDetails.objects.get(id=id1).delete()
        # GeneralLedger.objects.get(debit=debit, credit=credit, description=description,
        #                           ref_number=voucher_number, journal_type='BB', main_Trans=False).delete()

        # get the sum of the receipt detail values
        total_debit = SetupBegbalanceDetails.objects.filter(
            mainid_id=pk).aggregate(Sum('debit'))['debit__sum'] or 0.00
        total_credit = SetupBegbalanceDetails.objects.filter(
            mainid_id=pk).aggregate(Sum('credit'))['credit__sum'] or 0.00

        # Get the cash receipt journal items
        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=period_number, journal_type='BB'))

        data = {
            'deleted': True,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'journal_list': journal_list,
        }
        return JsonResponse(data)


class DeleteBegBalance(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        ref_number1 = SetupBegBalanceMain.objects.get(id=id1).periodno
        GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='BB').delete()

        SetupBegBalanceMain.objects.get(id=id1).delete()

        data = {
            'deleted': True
        }
        return JsonResponse(data)


# VALIDATIONS


def ValidateNoteNo(request):
    notes = request.GET.get('notes', None)
    # print(notes)
    data = {
        'is_taken': ChartSubCategory.objects.filter(notes__iexact=notes).exists()
    }
    return JsonResponse(data)


def populate_noteitems(request):
    if request.method == 'GET' and request.is_ajax():
        category = request.GET.get('sub_category', None)

        result_set = []
        selected_items = []

        if category:
            selected_category = ChartSubCategory.objects.get(
                id=category)
            selected_items = selected_category.noteitems.all()
            print('Selected Note Items are: ', selected_items)
        else:
            selected_items = ChartNoteItems.objects.all().order_by('-item_name')
            print('Selected ALL Note Items')

        for item in selected_items:
            # print('Item Name: ', item.item_name)
            # print('Item ID: ', item.id)
            result_set.append({'item': item.item_name, 'itemID': item.id})

        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

    else:
        return redirect('/')


def get_acctcat(request):
    if request.method == 'GET' and request.is_ajax():
        item_code = request.GET.get('item_code', None)

        selected_category = ChartNoteItems.objects.get(
            id=item_code).sub_category_id
        print('Selected Category Items is: ', selected_category)

        data = {
            'selected_category': selected_category
        }
        return JsonResponse(data)

    else:
        return redirect('/')


def populate_purchaseitems(request):
    if request.method == 'GET' and request.is_ajax():
        print('AM HERE!!!: ')
        option_type = request.GET.get('type', None)

        result_set = []
        selected_items = []
        selected_accounts = []

        if option_type == 'inventory':
            # selected_items = SetupInventoryItems.objects.all().order_by('-inventory_name')
            selected_items = SetupInventoryItems.objects.all()
            print('Selected Inventory Items are: ', selected_items)

            for item in selected_items:
                result_set.append(
                    {'item': item.inventory_name, 'itemID': item.id})

            # ids = ChartSubCategory.objects.filter(id='24').values_list('id', flat=True)
            # note_acct_inventory = ChartNoteItems.objects.filter(sub_category__in=ids)
        else:
            selected_items = SetupFixedAssets.objects.all().order_by('-description')
            print('Selected Fixed Asset are: ', selected_items)

            for item in selected_items:
                result_set.append(
                    {'item': item.description, 'itemID': item.id})

        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

    else:
        return redirect('/')


class DeletePurchase(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        ref_number1 = PurchaseMain.objects.get(id=id1).voucher_number
        GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='PJ').delete()

        PurchaseMain.objects.get(id=id1).delete()

        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeletePurchaseItem(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        pk = request.GET.get('mainID', None)
        voucher_number = request.GET.get('voucher_number', None)
        description = PurchaseDetails.objects.get(id=id1).description
        amount = PurchaseDetails.objects.get(id=id1).amount

        PurchaseDetails.objects.get(id=id1).delete()
        GeneralLedger.objects.get(debit=amount, description=description,
                                  ref_number=voucher_number, journal_type='PJ', main_Trans=False).delete()

        # get the sum of the receipt detail values
        total_sum = PurchaseDetails.objects.filter(
            expense_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00

        # Update Cash receipt journal total credit value
        total_amount = float(total_sum)
        obj3 = GeneralLedger.objects.get(
            ref_number=voucher_number, journal_type='PJ', main_Trans=True)
        obj3.credit = total_amount
        obj3.save()

        # Get the cash receipt journal items
        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number, journal_type='PJ'))

        journal_list1 = GeneralLedger.objects.filter(
            ref_number=voucher_number, journal_type='PJ')
        print('JOURNAL LIST RETRIEVED : ', journal_list1)

        data = {
            'deleted': True,
            'total_sum': total_sum,
            'journal_list': journal_list,
        }
        return JsonResponse(data)


def get_assetaccts(request):
    if request.method == 'GET' and request.is_ajax():
        item_code = request.GET.get('item_code', None)

        asset_account = SetupFixedAssets.objects.get(
            id=item_code).asset_account_id
        expense_account = SetupFixedAssets.objects.get(
            id=item_code).expense_account_id
        accumulated_account = SetupFixedAssets.objects.get(
            id=item_code).accumulated_account_id
        asset_category = ChartNoteItems.objects.get(
            id=asset_account).sub_category_id

        print('Selected Asset Account Items is: ', asset_account)
        print('Selected Category Items is: ', asset_category)

        data = {
            'asset_account': asset_account,
            'expense_account': expense_account,
            'accumulated_account': accumulated_account,
            'asset_category': asset_category,
        }
        return JsonResponse(data)

    else:
        return redirect('/')


def get_date_value(request):
    if request.method == 'GET' and request.is_ajax():
        main_ID = request.GET.get('main_ID', None)

        selected_date = SetupBegBalanceMain.objects.get(
            id=main_ID).entrydate
        print('Selected DATE Items is: ', selected_date)

        data = {
            'selected_date': selected_date
        }
        return JsonResponse(data)

    else:
        return redirect('/')
