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
                     GJournalDetails, GeneralLedger)


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
        ReceiptDetails.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteRececipt(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        ReceiptMain.objects.get(id=id1).delete()
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

        # print('Selected Category Key is: ', category)

        result_set = []
        selected_items = []

        selected_category = ChartSubCategory.objects.get(
            sub_category_code=category)
        selected_items = selected_category.noteitems.all()
        # print('Selected Note Items are: ', selected_items)

        for item in selected_items:
            # print('Item Name: ', item.item_name)
            # print('Item ID: ', item.id)
            result_set.append({'item': item.item_name, 'itemID': item.id})

        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

    else:
        return redirect('/')
