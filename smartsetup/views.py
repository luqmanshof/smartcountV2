from django.shortcuts import render,redirect,get_object_or_404
from smartsetup.forms import (
    SignUpForm,EditProfileForm,UserProfileForm,ChartCategoryForm,
    ChartSubCategoryForm,ChartNoteItemsForm,SetupInventoryItemsForm,SetupClientsForm,
    SetupVendorsForm,ReceiptMainForm,ReceiptDetailsForm, ExpenseMainForm,
    ExpenseDetailsForm, GJournalMainForm, GJournalDetailsForm
)
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from smartsetup.models import (
    UserProfile,ChartCategory,ChartSubCategory,ChartNoteItems,SetupClients,
    SetupVendors,SetupInventoryCategory,SetupInventoryItems,SetupClients,
    SetupVendors,ReceiptMain,ReceiptDetails, ExpenseMain, ExpenseDetails, 
    GJournalMain, GJournalDetails, GeneralLedger
)
from django.forms.models import model_to_dict
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView
from django.db.models import Max, PositiveIntegerField, Value, Sum
from django.db.models.functions import Cast, Coalesce
from django.utils import timezone
from django.core import serializers
import json as simplejson


@login_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # userprofile_form = UserProfileForm(request.POST)
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            user = form.save()
            # user = userprofile_form.save( instance=request.user.userprofile)

            # login immediately with the created user profile
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('dashboard')
    else:
        form = SignUpForm()
        # userprofile_form = UserProfileForm()
        args = {'form':form}
        return render(request,'smartsetup/signup.html',args)

@login_required
def list_signup(request):
    users = User.objects.all()
    # fields = model_to_dict(user,fields=['username','first_name','last_name','email'])
    fieldCols = ['User Name','First Name','Last Name','E-Mail']
    return render(request, 'smartsetup/list_signup.html',{'fieldCols':fieldCols,'users':users})

@login_required
def edit_signup(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        userprofile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        # userprofile_obj = UserProfile.objects.all()

        if form.is_valid() and userprofile_form.is_valid():
            form.save()
            userprofile_form.save()
            # return redirect('home')
            users = User.objects
            return render(request, 'smartsetup/list_signup.html',{'users':users})
    else:
        user = request.user
        form = EditProfileForm(instance=user)
        userprofile_form = UserProfileForm(instance=user.userprofile)
        # form = EditProfileForm(instance=request.user)
        # userprofile_form = UserProfileForm(instance=request.user.userprofile)

        args = {'form':form,'userprofile_form':userprofile_form}
        return render(request,'smartsetup/edit_signup.html',args)

@login_required
@permission_required('smartsetup.can_change_user_profile', raise_exception=True)
def edit_signup_with_pk(request, pk=None):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        userprofile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        # userprofile_obj = UserProfile.objects.all()

        if form.is_valid() and userprofile_form.is_valid():
            form.save()
            userprofile_form.save()
            # return redirect('home')
            users = User.objects
            return render(request, 'smartsetup/list_signup.html',{'users':users})

    else:
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        form = EditProfileForm(instance=user)
        # userprofile_form = UserProfileForm(instance=userprofile)
        userprofile_form = UserProfileForm(instance=user.userprofile)

        args = {'form':form,'userprofile_form':userprofile_form}
        return render(request,'smartsetup/edit_signup.html',args)

#SETUP CHART CATEGORY
@login_required
def chartcategory_list(request, pk=None):
    chartcategories = ChartCategory.objects
    fieldCols = ['Category Code','Category Name']
    args ={'fieldCols':fieldCols,'chartcategories':chartcategories}
    return render(request, 'smartsetup/chartcategory_list.html',args)

@login_required
def chartcategory(request, pk=None):
    if request.method == 'POST':
        if pk:
            chartcategory = ChartCategory.objects.get(pk=pk)
            form = ChartCategoryForm(request.POST, instance=chartcategory)
        else:
            form = ChartCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('chartcategory_list')
    else:
        if (pk != 0):
            chartcategory = ChartCategory.objects.get(pk=pk)
            form = ChartCategoryForm(instance=chartcategory)
        else:
            form = ChartCategoryForm()

        args = {'form':form,'title':'Setup Chart category'}
        return render(request,'smartsetup/form.html',args)

class ChartCategoryDetail(generic.DetailView):
    model = ChartCategory
    template_name = 'smartsetup/chartcategory_detail.html'

class ChartCategoryDelete(generic.DeleteView):
    model = ChartCategory
    template_name = 'smartsetup/chartcategory_delete.html'
    success_url = reverse_lazy('chartcategory_list')

##SETUP CHART SUB-CATEGORY
@login_required
def chartsubcategory_list(request, pk=None):
    chartcategories = ChartSubCategory.objects
    fieldCols = ['Account Code','Account Name','Notes','Category']
    args ={'fieldCols':fieldCols,'chartcategories':chartcategories}
    return render(request, 'smartsetup/chartsubcategory_list.html',args)

@login_required
def chartsubcategory(request, pk=None):
    if request.method == 'POST':
        if pk:
            chartsubcategory = ChartSubCategory.objects.get(pk=pk)
            form = ChartSubCategoryForm(request.POST, instance=chartsubcategory)
        else:
            form = ChartSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chartsubcategory_list')
    else:
        if (pk != 0):
            chartsubcategory = ChartSubCategory.objects.get(pk=pk)
            form = ChartSubCategoryForm(instance=chartsubcategory)
        else:
            form = ChartSubCategoryForm()
    return render(request,'smartsetup/chartsubcategory.html',{'form':form,'title':'Setup Chart category'})

class ChartSubCategoryDetail(generic.DetailView):
    model = ChartSubCategory
    template_name = 'smartsetup/chartsubcategory_detail.html'

class ChartSubCategoryDelete(generic.DeleteView):
    model = ChartSubCategory
    template_name = 'smartsetup/chartsubcategory_delete.html'
    success_url = reverse_lazy('chartsubcategory_list')

##SETUP CHART NOTE-ITEMS
@login_required
def chartnoteitems_list(request, pk=None):
    chartnoteitems = ChartNoteItems.objects.all().order_by('sub_category')
    fieldCols = ['Category','Account Item']
    args ={'fieldCols':fieldCols,'chartnoteitems':chartnoteitems}
    return render(request, 'smartsetup/chartnoteitems_list.html',args)

@login_required
def chartnoteitems(request, pk=None):
    if request.method == 'POST':
        if pk:
            chartnoteitems = ChartNoteItems.objects.get(pk=pk)
            form = ChartNoteItemsForm(request.POST, instance=chartnoteitems)
        else:
            form = ChartNoteItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chartnoteitems_list')
    else:
        if (pk != 0):
            chartnoteitems = ChartNoteItems.objects.get(pk=pk)
            form = ChartNoteItemsForm(instance=chartnoteitems)
        else:
            form = ChartNoteItemsForm()
    return render(request,'smartsetup/form.html',{'form':form,'title':'Setup Account Notes'})

class ChartNoteItemsDelete(generic.DeleteView):
    model = ChartNoteItems
    template_name = 'smartsetup/chartnoteitems_delete.html'
    success_url = reverse_lazy('chartnoteitems_list')


#SETUP INVENTORY CATEGORY
@login_required
def setupinventorycat_list(request, pk=None):
    setupinventorycategory = SetupInventoryCategory.objects
    fieldCols = ['Category Code','Category Name']
    args ={'fieldCols':fieldCols,'setupinventorycategory':setupinventorycategory}
    return render(request, 'smartsetup/setupinvetorycat_list.html',args)

class SetupInventoryCat(generic.CreateView):
    model = SetupInventoryCategory
    fields = ['inventory_category_code','inventory_category_name']
    template_name = 'smartsetup/SetupInventoryCat.html'
    success_url = reverse_lazy('setupinventorycategory_list')

class SetupInventoryCatUpdate(generic.UpdateView):
    model = SetupInventoryCategory
    fields = ['inventory_category_code','inventory_category_name']
    template_name = 'smartsetup/SetupInventoryCat.html'
    success_url = reverse_lazy('setupinventorycategory_list')

class SetupInventoryCatDetail(generic.DetailView):
    model = SetupInventoryCategory
    template_name = 'smartsetup/setupinvetorycat_detail.html'

class SetupInventoryCatDelete(generic.DeleteView):
    model = SetupInventoryCategory
    template_name = 'smartsetup/setupinvetorycat_delete.html'
    success_url = reverse_lazy('setupinventorycategory_list')

#SETUP INVENTORY ITEMS
@login_required
def setupinventoryitems_list(request, pk=None):
    setupinventoryitems = SetupInventoryItems.objects
    fieldCols = ['Inventory Code','Inventory Name','Description','Category']
    args ={'fieldCols':fieldCols,'setupinventoryitems':setupinventoryitems}
    return render(request, 'smartsetup/setupinventoryitems_list.html',args)

@login_required
def setupinventoryitems(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupinventoryitems = SetupInventoryItems.objects.get(pk=pk)
            form = SetupInventoryItemsForm(request.POST, instance=setupinventoryitems)
        else:
            form = SetupInventoryItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('setupinventoryitems_list')
    else:
        if (pk != 0):
            setupinventoryitems = SetupInventoryItems.objects.get(pk=pk)
            form = SetupInventoryItemsForm(instance=setupinventoryitems)
        else:
            form = SetupInventoryItemsForm()
    return render(request,'smartsetup/form.html',{'form':form,'title':'Setup Inventory Items'})

class SetupInventoryItemsDetail(generic.DetailView):
    model = SetupInventoryItems
    template_name = 'smartsetup/setupinventoryitems_detail.html'

class SetupInventoryItemsDelete(generic.DeleteView):
    model = SetupInventoryItems
    template_name = 'smartsetup/setupinventoryitems_delete.html'
    success_url = reverse_lazy('setupinventoryitems_list')


#SETUP CLIENTS
@login_required
def setupclients_list(request, pk=None):
    setupclients = SetupClients.objects
    fieldCols = ['Client Name','Address','Phone','Account Officer']
    args ={'fieldCols':fieldCols,'setupclients':setupclients}
    return render(request, 'smartsetup/setupclients_list.html',args)

@login_required
def setupclients(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupclients = SetupClients.objects.get(pk=pk)
            form = SetupClientsForm(request.POST, instance=setupclients)
        else:
            form = SetupClientsForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('setupclients_list')
    else:
        if (pk != 0):
            setupclients = SetupClients.objects.get(pk=pk)
            form = SetupClientsForm(instance=setupclients)
        else:
            form = SetupClientsForm()

        args = {'form':form,'title':'Setup Client Account'}
        return render(request,'smartsetup/form.html',args)

class SetupClientsDetail(generic.DetailView):
    model = SetupClients
    template_name = 'smartsetup/setupclients_detail.html'

class SetupClientsDelete(generic.DeleteView):
    model = SetupClients
    template_name = 'smartsetup/setupclients_delete.html'
    success_url = reverse_lazy('setupclients_list')



#SETUP VENDORS
@login_required
def setupvendors_list(request, pk=None):
    setupvendors = SetupVendors.objects
    fieldCols = ['Vendor Name','Address','Phone','Website']
    args ={'fieldCols':fieldCols,'setupvendors':setupvendors}
    return render(request, 'smartsetup/setupvendors_list.html',args)

@login_required
def setupvendors(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupvendors = SetupVendors.objects.get(pk=pk)
            form = SetupVendorsForm(request.POST, instance=setupvendors)
        else:
            form = SetupVendorsForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('setupvendors_list')
    else:
        if (pk != 0):
            setupvendors = SetupVendors.objects.get(pk=pk)
            form = SetupVendorsForm(instance=setupvendors)
        else:
            form = SetupVendorsForm()

        args = {'form':form,'title':'Setup Vendor Account'}
        return render(request,'smartsetup/form.html',args)

class SetupVendorsDetail(generic.DetailView):
    model = SetupVendors
    template_name = 'smartsetup/setupvendors_detail.html'

class SetupVendorsDelete(generic.DeleteView):
    model = SetupVendors
    template_name = 'smartsetup/setupvendors_delete.html'
    success_url = reverse_lazy('setupvendors_list')


#RECEIPT TRANSACTION
@login_required
def receipt_list(request, pk=None):
    receipts = ReceiptMain.objects.all()
    fieldCols = ['Receipt No.','Date / Time','Issued To']
    args ={'fieldCols':fieldCols,'receipts':receipts}
    return render(request, 'account/receipt_list.html',args)

class ReceiptClass(ListView):
    # model = ReceiptDetails.objects.filter(id = 0)
    model = ReceiptDetails
    template_name = 'account/receipt.html'
    # context_object_name = 'receiptitems'
           
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_receipt']  = ReceiptMain.objects.aggregate(max_val=Coalesce(Max(Cast('receipt_number', output_field=PositiveIntegerField())), Value(1000)))
        context['client_name'] = SetupClients.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(category_code_id='3')
        context['revenue_acct'] = ChartSubCategory.objects.filter(category_code_id='1')

        return context

class ReceiptEditClass(ListView):
    model = ReceiptDetails
    template_name = 'account/receipt.html'
    # context_object_name = 'receiptitems'

    def get_context_data(self, **kwargs):
        pkMain = self.request.GET.get('RcptId')
        print('MAIN ID: ',pkMain)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['Main_receipt']  = ReceiptMain.objects.get(id=pkMain)
        context['client_name'] = SetupClients.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(category_code_id='3')
        context['revenue_acct'] = ChartSubCategory.objects.filter(category_code_id='1')
        # print(context)

        # return context
        return HttpResponse(simplejson.dumps(context), content_type="application/json")


def receiptedit(request,pk=None):
    # pkMain = request.POST.get('idprov')
    # receiptmain = ReceiptMain.objects.get(id=pkMain)
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_sum = ReceiptDetails.objects.filter(receipt_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        receiptmain = ReceiptMain.objects.get(id=pk)
        receiptitems = ReceiptDetails.objects.filter(receipt_main_id_id=pk)

        # print('RECEIPT MAIN VALUES : ', receiptmain)

        client_name = SetupClients.objects.all()
        cash_acct = ChartSubCategory.objects.filter(category_code_id='3')
        revenue_acct = ChartSubCategory.objects.filter(category_code_id='1')

        args = {'receiptmain':receiptmain,'receiptitems':receiptitems,'client_name':client_name,
        'cash_acct':cash_acct, 'revenue_acct':revenue_acct,'total_sum':total_sum}
        return render(request,'account/receipt.html',args)
    else:
        return render(request,'account/receipt_list.html')


# Create and Read User Django Ajax
class CreateReceipt(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('receipt def AJAX VIEW ')

        receipt_date1 = request.GET.get('receipt_date', None)
        receipt_number1 = request.GET.get('receipt_number', None)
        client_name1 = request.GET.get('client_name', None)
        bill_to1 = request.GET.get('bill_to', None)
        cash_account1 = request.GET.get('cash_account', None)
        Debit_account1 = request.GET.get('Debit_account', None)
        pkMain = request.GET.get('mainID', None)
        description = request.GET.get('description', None)
        revenue_account1 = request.GET.get('revenue_account', None)
        credit_account1 = request.GET.get('credit_account', None)
        amount1 = request.GET.get('amount', None)

        amount2 = float(amount1.replace(',',''))

        ClientID = SetupClients.objects.get(id = client_name1).id
        cashAccount = ChartSubCategory.objects.get(sub_category_code = cash_account1).sub_category_name
        DebitAccount = ChartNoteItems.objects.get(id = Debit_account1).item_name
        revenueAccount = ChartSubCategory.objects.get(sub_category_code = revenue_account1).sub_category_name
        creditAccount = ChartNoteItems.objects.get(id = credit_account1).item_name
        

        if pkMain:
            print('UPDATE EXISTING RECORD ')
            obj = ReceiptMain.objects.get(id=pkMain)
            obj.date = receipt_date1
            obj.receipt_number = receipt_number1
            obj.client = SetupClients.objects.get(id = client_name1)
            obj.bill_to = bill_to1
            obj.cash_account = ChartSubCategory.objects.get(sub_category_code = cash_account1)
            obj.Debit_account = ChartNoteItems.objects.get(id = Debit_account1)

            obj.save()
        
        else:
            # print('CLIENT SELECTED : ',SetupClients.objects.get(id = client_name1))
            # print('BEFORE : ',receipt_date1)
            
            # print('RETRIEVED CLIENT INFO:  ' , ClientID)

            obj = ReceiptMain.objects.create(
                date = receipt_date1,
                receipt_number = receipt_number1,
                client_id = ClientID,
                bill_to = bill_to1,
                cash_account = ChartSubCategory.objects.get(sub_category_code = cash_account1),
                Debit_account = ChartNoteItems.objects.get(id = Debit_account1),
            )
            # print('AFTER RETRIEVED')
            # print('RECEIPT MAIN ID: ', obj.id)

        obj2 = ReceiptDetails.objects.create(
            description = description,
            revenue_account = ChartSubCategory.objects.get(sub_category_code = revenue_account1),
            credit_account = ChartNoteItems.objects.get(id = credit_account1),
            amount = amount2,
            receipt_main_id_id = obj.id,
        )

        total_sum = ReceiptDetails.objects.filter(receipt_main_id_id=obj.id).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        # journal_list = serializers.serialize(
        #         "json", GeneralLedger.objects.filter(ref_number=receipt_number1, journal_type='CRJ'))

        receipt_main = {'Mainid': obj.id, 'date': obj.date, 'receipt_number': obj.receipt_number, 'bill_to': obj.bill_to}

        receipt_sub = {'Subid': obj2.id, 'description': obj2.description,'revenue_account': revenueAccount, 
                'credit_account': creditAccount, 'amount': obj2.amount}

        data = {
            'receipt_main': receipt_main,
            'receipt_sub': receipt_sub
        }
        return JsonResponse(data)

    

#EXPENSE TRANSACTION
@login_required
def expense_list(request, pk=None):
    expenses = ExpenseMain.objects
    fieldCols = ['Date','Expense No.','Description']
    args ={'fieldCols':fieldCols,'expenses':expenses}
    return render(request, 'account/expense_list.html',args)

@login_required
def expense(request,pk=None):
    if request.method == 'POST':
        expensemain_form = ExpenseMainForm(request.POST, instance=request.expensemain)
        expensedetails_form = ExpenseDetailsForm(request.POST, instance=request.expensemain.expensedetails)

        if expensemain_form.is_valid() and expensedetails_form.is_valid():
            expensemain_form.save()
            expensedetails_form.save()
            # return redirect('home')
            expenses = ExpenseMain.objects
            expensedetails = ExpenseMain.ExpenseDetails.objects
            return render(request, 'account/receipt.html',{'expenses':expenses})
    else:
        # receiptmain = request.receiptmain
        expensemain_form = ExpenseMainForm()
        # latest_receiptno = ReceiptMain.objects.latest('receipt_number') + 1
        expensedetails_form = ExpenseDetailsForm()
        expense_acct = ChartSubCategory.objects.filter(category_code_id='2')
        args = {
            'expensemain_form':expensemain_form,'expensedetails_form':expensedetails_form,
            'expense_acct':expense_acct
            }
        return render(request,'account/expense.html',args)



#REPORTS
@login_required
def financialperformance(request):
    revenues = ChartSubCategory.objects.filter(category_code_id=1)
    expenses = ChartSubCategory.objects.filter(category_code_id=2)

    args = {'revenues':revenues,'expenses':expenses}
    return render (request, 'smartsetup/financialperformance.html',args)
# 
# @login_required
# def financialperformanceprint(request):
#     revenues = ChartSubCategory.objects.filter(category_code_id=1)
#     expenses = ChartSubCategory.objects.filter(category_code_id=2)
#
#     args = {'revenues':revenues,'expenses':expenses}
#     return render (request, 'smartsetup/financialperformance_print.html',args)

@login_required
def financialposition(request, pk=None):
    curr_assets = ChartSubCategory.objects.filter(category_code_id=3)
    curr_liabilities = ChartSubCategory.objects.filter(category_code_id=5)
    noncurr_assets = ChartSubCategory.objects.filter(category_code_id=4)
    noncurr_liabilities = ChartSubCategory.objects.filter(category_code_id=6)

    args = {'curr_assets':curr_assets,'curr_liabilities':curr_liabilities,
            'noncurr_assets':noncurr_assets,'noncurr_liabilities':noncurr_liabilities}
    return render (request, 'smartsetup/financialposition.html',args)

@login_required
def financialcashflow(request):
    revenues = ChartSubCategory.objects.filter(category_code_id=1)
    expenses = ChartSubCategory.objects.filter(category_code_id=2)

    args = {'revenues':revenues,'expenses':expenses}
    return render (request, 'smartsetup/financialcashflow.html',args)