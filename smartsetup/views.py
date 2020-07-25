from django.shortcuts import render, redirect, get_object_or_404
from smartsetup.forms import (
    SignUpForm, EditProfileForm, UserProfileForm, ChartCategoryForm,
    ChartSubCategoryForm, ChartNoteItemsForm, SetupInventoryItemsForm,
    SetupClientsForm, SetupVendorsForm, ReceiptMainForm, ReceiptDetailsForm,
    ExpenseMainForm, ExpenseDetailsForm, GJournalMainForm, GJournalDetailsForm,
    EmployeeProfileForm, SetupFixedAssetsForm, SetupDivisionForm, SetupDepartmentForm,
    CompanyRegistrationForm, SetupUnitForm, BudgetDepartmentForm
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from smartsetup.models import (
    UserProfile, ChartCategory, ChartSubCategory, ChartNoteItems, SetupClients,
    SetupVendors, SetupInventoryCategory, SetupInventoryItems, SetupClients,
    SetupVendors, ReceiptMain, ReceiptDetails, ExpenseMain, ExpenseDetails,
    GJournalMain, GJournalDetails, GeneralLedger, EmployeeProfile, PurchaseMain,
    PurchaseDetails, SetupFixedAssets, SetupDivision, SetupDepartment, CompanyRegistration,
    SetupBegBalanceMain, SetupBegbalanceDetails, SetupUnit, BudgetDepartment,
    BudgetMain, BudgetDetails, BudgetDepartment
)
from django.forms.models import model_to_dict
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView
from django.db.models import Max, PositiveIntegerField, Value, Sum, F, Q
from django.db.models.functions import Cast, Coalesce
from django.utils import timezone
from django.core import serializers
import json as simplejson
import datetime


@login_required
def signup(request):
    if request.method == 'POST':
        print("AM HERE!!!")
        form = SignUpForm(request.POST)
        # userprofile_form = UserProfileForm(request.POST)
        print("FIRST HERE!!!")
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            print("SECOND HERE!!!")
            user = form.save()
            # user = userprofile_form.save( instance=request.user.userprofile)
            print("AM ALSO HERE!!!")

            # login immediately with the created user profile
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('dashboard')
    else:
        form = SignUpForm()
        # userprofile_form = UserProfileForm()
        args = {'form': form}
        return render(request, 'smartsetup/signup.html', args)


@login_required
def list_signup(request):
    users = User.objects.all()
    # fields = model_to_dict(user,fields=['username','first_name','last_name','email'])
    fieldCols = ['User Name', 'First Name', 'Last Name', 'E-Mail']
    return render(request, 'smartsetup/list_signup.html', {'fieldCols': fieldCols, 'users': users})


@login_required
def edit_signup(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        userprofile_form = UserProfileForm(
            request.POST, instance=request.user.userprofile)
        # userprofile_obj = UserProfile.objects.all()

        if form.is_valid() and userprofile_form.is_valid():
            form.save()
            userprofile_form.save()
            # return redirect('home')
            users = User.objects
            return render(request, 'smartsetup/list_signup.html', {'users': users})
    else:
        user = request.user
        form = EditProfileForm(instance=user)
        userprofile_form = UserProfileForm(instance=user.userprofile)
        # form = EditProfileForm(instance=request.user)
        # userprofile_form = UserProfileForm(instance=request.user.userprofile)

        args = {'form': form, 'userprofile_form': userprofile_form}
        return render(request, 'smartsetup/edit_signup.html', args)


@login_required
@permission_required('smartsetup.can_change_user_profile', raise_exception=True)
def edit_signup_with_pk(request, pk=None):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        userprofile_form = UserProfileForm(
            request.POST, instance=request.user.userprofile)
        # userprofile_obj = UserProfile.objects.all()

        if form.is_valid() and userprofile_form.is_valid():
            form.save()
            userprofile_form.save()
            # return redirect('home')
            users = User.objects
            return render(request, 'smartsetup/list_signup.html', {'users': users})

    else:
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        form = EditProfileForm(instance=user)
        # userprofile_form = UserProfileForm(instance=userprofile)
        userprofile_form = UserProfileForm(instance=user.userprofile)

        args = {'form': form, 'userprofile_form': userprofile_form}
        return render(request, 'smartsetup/edit_signup.html', args)

# SETUP COMPANY INFO


@login_required
def setupcompanyreg(request, pk=None):
    print('AM HERE NOW!!!')
    if request.method == 'POST':
        if pk:
            companyregistration = CompanyRegistration.objects.get(pk=pk)
            form = CompanyRegistrationForm(
                request.POST, instance=companyregistration)
        else:
            form = CompanyRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            # return redirect('home')
            return render(request, 'smartapp/dashboard.html')
    else:
        if (pk != 0):
            companyregistration = CompanyRegistration.objects.get(pk=pk)
            form = CompanyRegistrationForm(instance=companyregistration)
        else:
            form = CompanyRegistrationForm()

        args = {'form': form, 'title': 'Company Registration'}
        return render(request, 'smartsetup/form.html', args)


# SETUP DEPARTMENT
@login_required
def setupdepartment_list(request, pk=None):
    setupdepartment = SetupDepartment.objects
    fieldCols = ['Department Name', 'Division']
    args = {'fieldCols': fieldCols, 'setupdepartment': setupdepartment}
    return render(request, 'smartsetup/setupdepartment_list.html', args)


@login_required
def setupdepartment(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupdepartment = SetupDepartment.objects.get(pk=pk)
            form = SetupDepartmentForm(request.POST, instance=setupdepartment)
        else:
            form = SetupDepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('setupdepartment_list')
    else:
        if (pk != 0):
            setupdepartment = SetupDepartment.objects.get(pk=pk)
            form = SetupDepartmentForm(instance=setupdepartment)
        else:
            form = SetupDepartmentForm()

        args = {'form': form, 'title': 'Setup Department'}
        return render(request, 'smartsetup/form.html', args)


class SetupDepartmentDetail(generic.DetailView):
    model = SetupDepartment
    template_name = 'smartsetup/setupdepartment_detail.html'


class SetupDepartmentDelete(generic.DeleteView):
    model = SetupDepartment
    template_name = 'smartsetup/setupdepartment_delete.html'
    success_url = reverse_lazy('setupdepartment_list')


# SETUP DIVISION
@login_required
def setupdivision_list(request, pk=None):
    setupdivision = SetupDivision.objects
    fieldCols = ['Section', 'Department', 'Description']
    args = {'fieldCols': fieldCols, 'setupdivision': setupdivision}
    return render(request, 'smartsetup/setupdivision_list.html', args)


@login_required
def setupdivision(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupdivision = SetupDivision.objects.get(pk=pk)
            form = SetupDivisionForm(request.POST, instance=setupdivision)
        else:
            form = SetupDivisionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('setupdivision_list')
    else:
        if (pk != 0):
            setupdivision = SetupDivision.objects.get(pk=pk)
            form = SetupDivisionForm(instance=setupdivision)
        else:
            form = SetupDivisionForm()

        args = {'form': form, 'title': 'Setup Section'}
        return render(request, 'smartsetup/form.html', args)


class SetupDivisionDetail(generic.DetailView):
    model = SetupDivision
    template_name = 'smartsetup/setupdivision_detail.html'


class SetupDivisionDelete(generic.DeleteView):
    model = SetupDivision
    template_name = 'smartsetup/setupdivision_delete.html'
    success_url = reverse_lazy('setupdivision_list')


# SETUP UNIT
@login_required
def setupunit_list(request, pk=None):
    setupunit = SetupUnit.objects
    fieldCols = ['Unit Name', 'Section', 'Description']
    args = {'fieldCols': fieldCols, 'setupunit': setupunit}
    return render(request, 'smartsetup/setupunit_list.html', args)


@login_required
def setupunit(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupunit = SetupUnit.objects.get(pk=pk)
            form = SetupUnitForm(request.POST, instance=setupunit)
        else:
            form = SetupUnitForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('setupunit_list')
    else:
        if (pk != 0):
            setupunit = SetupUnit.objects.get(pk=pk)
            form = SetupUnitForm(instance=setupunit)
        else:
            form = SetupUnitForm()

        args = {'form': form, 'title': 'Setup Unit'}
        return render(request, 'smartsetup/form.html', args)


class SetupUnitDetail(generic.DetailView):
    model = SetupUnit
    template_name = 'smartsetup/setupunit_detail.html'


class SetupUnitDelete(generic.DeleteView):
    model = SetupUnit
    template_name = 'smartsetup/setupunit_delete.html'
    success_url = reverse_lazy('setupunit_list')


# SETUP CHART CATEGORY
@login_required
def chartcategory_list(request, pk=None):
    chartcategories = ChartCategory.objects
    fieldCols = ['Category Code', 'Category Name']
    args = {'fieldCols': fieldCols, 'chartcategories': chartcategories}
    return render(request, 'smartsetup/chartcategory_list.html', args)


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

        args = {'form': form, 'title': 'Setup Chart category'}
        return render(request, 'smartsetup/form.html', args)


class ChartCategoryDetail(generic.DetailView):
    model = ChartCategory
    template_name = 'smartsetup/chartcategory_detail.html'


class ChartCategoryDelete(generic.DeleteView):
    model = ChartCategory
    template_name = 'smartsetup/chartcategory_delete.html'
    success_url = reverse_lazy('chartcategory_list')

# SETUP CHART SUB-CATEGORY
@login_required
def chartsubcategory_list(request, pk=None):
    chartcategories = ChartSubCategory.objects
    fieldCols = ['Account Code', 'Account Name', 'Notes', 'Category']
    args = {'fieldCols': fieldCols, 'chartcategories': chartcategories}
    return render(request, 'smartsetup/chartsubcategory_list.html', args)


@login_required
def chartsubcategory(request, pk=None):
    if request.method == 'POST':
        if pk:
            chartsubcategory = ChartSubCategory.objects.get(pk=pk)
            form = ChartSubCategoryForm(
                request.POST, instance=chartsubcategory)
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
    return render(request, 'smartsetup/chartsubcategory.html', {'form': form, 'title': 'Setup Chart category'})


class ChartSubCategoryDetail(generic.DetailView):
    model = ChartSubCategory
    template_name = 'smartsetup/chartsubcategory_detail.html'


class ChartSubCategoryDelete(generic.DeleteView):
    model = ChartSubCategory
    template_name = 'smartsetup/chartsubcategory_delete.html'
    success_url = reverse_lazy('chartsubcategory_list')

# SETUP CHART NOTE-ITEMS
@login_required
def chartnoteitems_list(request, pk=None):
    chartnoteitems = ChartNoteItems.objects.all().order_by('sub_category')
    fieldCols = ['Category', 'Account Item']
    args = {'fieldCols': fieldCols, 'chartnoteitems': chartnoteitems}
    return render(request, 'smartsetup/chartnoteitems_list.html', args)


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
    return render(request, 'smartsetup/form.html', {'form': form, 'title': 'Setup Account Notes'})


class ChartNoteItemsDelete(generic.DeleteView):
    model = ChartNoteItems
    template_name = 'smartsetup/chartnoteitems_delete.html'
    success_url = reverse_lazy('chartnoteitems_list')


# SETUP INVENTORY CATEGORY
@login_required
def setupinventorycat_list(request, pk=None):
    setupinventorycategory = SetupInventoryCategory.objects
    fieldCols = ['Category Code', 'Category Name']
    args = {'fieldCols': fieldCols,
            'setupinventorycategory': setupinventorycategory}
    return render(request, 'smartsetup/setupinvetorycat_list.html', args)


class SetupInventoryCat(generic.CreateView):
    model = SetupInventoryCategory
    fields = ['inventory_category_code', 'inventory_category_name']
    template_name = 'smartsetup/SetupInventoryCat.html'
    success_url = reverse_lazy('setupinventorycategory_list')


class SetupInventoryCatUpdate(generic.UpdateView):
    model = SetupInventoryCategory
    fields = ['inventory_category_code', 'inventory_category_name']
    template_name = 'smartsetup/SetupInventoryCat.html'
    success_url = reverse_lazy('setupinventorycategory_list')


class SetupInventoryCatDetail(generic.DetailView):
    model = SetupInventoryCategory
    template_name = 'smartsetup/setupinvetorycat_detail.html'


class SetupInventoryCatDelete(generic.DeleteView):
    model = SetupInventoryCategory
    template_name = 'smartsetup/setupinvetorycat_delete.html'
    success_url = reverse_lazy('setupinventorycategory_list')

# SETUP INVENTORY ITEMS
@login_required
def setupinventoryitems_list(request, pk=None):
    setupinventoryitems = SetupInventoryItems.objects
    fieldCols = ['Inventory Code', 'Inventory Name', 'Description', 'Category']
    args = {'fieldCols': fieldCols, 'setupinventoryitems': setupinventoryitems}
    return render(request, 'smartsetup/setupinventoryitems_list.html', args)


@login_required
def setupinventoryitems(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupinventoryitems = SetupInventoryItems.objects.get(pk=pk)
            form = SetupInventoryItemsForm(
                request.POST, instance=setupinventoryitems)
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
    return render(request, 'smartsetup/form.html', {'form': form, 'title': 'Setup Inventory Items'})


class SetupInventoryItemsDetail(generic.DetailView):
    model = SetupInventoryItems
    template_name = 'smartsetup/setupinventoryitems_detail.html'


class SetupInventoryItemsDelete(generic.DeleteView):
    model = SetupInventoryItems
    template_name = 'smartsetup/setupinventoryitems_delete.html'
    success_url = reverse_lazy('setupinventoryitems_list')


# SETUP FIXED ASSET
@login_required
def setupfixedasset_list(request, pk=None):
    setupfixedassets = SetupFixedAssets.objects
    # fieldCols = ['Asset ID', 'Serial No', 'Asset Description', 'Asset Category',
    #              'Purchase Date', 'Purchase Cost', 'Depr. Method', 'Useful Life',
    #              'Salvage Value', 'Department'
    #              ]
    fieldCols = ['Asset ID', 'Asset Description', 'Asset Category', 'Depr. Method',
                 'Purchase Date', 'Purchase Cost', 'Useful Life', 'Salvage Value'
                 ]
    args = {'fieldCols': fieldCols, 'setupfixedassets': setupfixedassets}
    return render(request, 'smartsetup/setupfixedasset_list.html', args)


class FixedAsset(ListView):
    model = SetupFixedAssets
    template_name = 'smartsetup/setupfixedasset.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        # context['max_expense']  = ExpenseMain.objects.aggregate(max_val=Coalesce(Max(Cast('voucher_number', output_field=PositiveIntegerField())), Value(1000)))
        context['dept_name'] = SetupDepartment.objects.all()
        context['asset_acct'] = ChartNoteItems.objects.filter(
            sub_category_id='26')
        context['expense_acct'] = ChartNoteItems.objects.filter(
            sub_category_id='15')
        context['depreciation_acct'] = ChartNoteItems.objects.filter(
            sub_category_id='46')

        return context


def fixedassetedit(request, pk=None):
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        # total_sum = ExpenseDetails.objects.filter(expense_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00
        # print('TOTAL SUM GENERATED CREATED : ', total_sum)

        fixedasset_main = SetupFixedAssets.objects.get(id=pk)
        # expense_number1 = SetupFixedAssets.objects.get(id=pk).voucher_number
        # print('EXPENSE NO. RETRIEVED : ', expense_number1)

        # expenseitems = ExpenseDetails.objects.filter(expense_main_id_id=pk)

        dept_name = SetupDepartment.objects.all()
        asset_acct = ChartNoteItems.objects.filter(sub_category_id='26')
        expense_acct = ChartNoteItems.objects.filter(sub_category_id='15')
        depreciation_acct = ChartNoteItems.objects.filter(sub_category_id='46')

        staff_name = EmployeeProfile.objects.all()
        cash_acct = ChartSubCategory.objects.filter(category_code_id='3')
        expense_acct = ChartSubCategory.objects.filter(category_code_id='2')
        note_acct = ChartNoteItems.objects.all()
        # journal_list = GeneralLedger.objects.filter(ref_number=expense_number1, journal_type='CDJ')
        # print('EXPENSE JORNAL ITEMS : ', journal_list)

        args = {'fixedasset_main': fixedasset_main, 'dept_name': dept_name,
                'asset_acct': asset_acct, 'expense_acct': expense_acct,
                'depreciation_acct': depreciation_acct,
                }
        return render(request, 'smartsetup/setupfixedasset.html', args)
    else:
        return render(request, 'smartsetup/setupfixedasset_list.html')


@login_required
def setupfixedasset(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupfixedassets = SetupFixedAssets.objects.get(pk=pk)
            form = SetupFixedAssetsForm(
                request.POST, instance=setupfixedassets)
        else:
            form = SetupFixedAssetsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('setupfixedasset_list')
    else:
        if (pk != 0):
            setupfixedassets = SetupFixedAssets.objects.get(pk=pk)
            form = SetupFixedAssetsForm(instance=setupfixedassets)
        else:
            form = SetupFixedAssetsForm()
    return render(request, 'smartsetup/form.html', {'form': form, 'title': 'Setup Fixed Assets'})


class SetupFixedAssetDetail(generic.DetailView):
    model = SetupFixedAssets
    template_name = 'smartsetup/setupfixedasset_detail.html'


class SetupFixedAssetDelete(generic.DeleteView):
    model = SetupFixedAssets
    template_name = 'smartsetup/setupfixedasset_delete.html'
    success_url = reverse_lazy('setupfixedasset_list')


class CreateFixedAsset(View):
    # print('receipt AJAX VIEW ')

    def get(self, request):
        print('FixedAsset AJAX CREATE ')

        # ClientID = EmployeeProfile.objects.get(id = client_name1).id
        # cashAccount = ChartSubCategory.objects.get(id = cash_account1).sub_category_name
        # cashCategoryID = ChartSubCategory.objects.get(id = cash_account1).category_code_id
        # creditAccount = ChartNoteItems.objects.get(id = credit_account1).item_name
        # expenseAccount = ChartSubCategory.objects.get(id = expense_account1).sub_category_name
        # expenseCategoryID = ChartSubCategory.objects.get(id = expense_account1).category_code_id
        # DebitAccount = ChartNoteItems.objects.get(id = Debit_account1).item_name

        trans_date1 = request.GET.get('trans_date', None)
        asset_id1 = request.GET.get('asset_id', None)
        description = request.GET.get('description', None)
        depart_name = request.GET.get('depart_name', None)
        asset_account = request.GET.get('asset_account', None)
        expense_account = request.GET.get('expense_account', None)
        depr_account = request.GET.get('depr_account', None)
        depr_method = request.GET.get('depr_method', None)
        pkMain = request.GET.get('mainID', None)

        print('ASSET ACCOUNT : ', asset_account)

        if pkMain:
            print('UPDATE EXISTING RECORD ')
            obj = SetupFixedAssets.objects.get(id=pkMain)
            obj.acquisition_date = trans_date1
            obj.asset_id = asset_id1
            obj.description = description
            obj.department = SetupDepartment.objects.get(id=depart_name)
            obj.asset_account = ChartNoteItems.objects.get(id=asset_account)
            obj.expense_account = ChartNoteItems.objects.get(
                id=expense_account)
            obj.accumulated_account = ChartNoteItems.objects.get(
                id=depr_account)
            obj.depreciation_method = depr_method
            obj.save()

        else:
            print('ENTERED NEW ASSET RECORD ')

            obj = SetupFixedAssets.objects.create(
                acquisition_date=trans_date1,
                asset_id=asset_id1,
                description=description,
                department=SetupDepartment.objects.get(id=depart_name),
                asset_account=ChartNoteItems.objects.get(id=asset_account),
                expense_account=ChartNoteItems.objects.get(id=expense_account),
                accumulated_account=ChartNoteItems.objects.get(
                    id=depr_account),
                depreciation_method=depr_method
            )

        fixedasset_main = {'Mainid': obj.id, 'date': obj.acquisition_date,
                           'asset_id': obj.asset_id, 'description': obj.description}

        data = {'fixedasset_main': fixedasset_main}
        return JsonResponse(data)


# SETUP EMPLOYEES
@login_required
def employees_list(request, pk=None):
    employees = EmployeeProfile.objects
    fieldCols = ['First Name', 'Last Name', 'Address', 'Phone']
    args = {'fieldCols': fieldCols, 'employees': employees}
    return render(request, 'smartsetup/employees_list.html', args)


@login_required
def employees(request, pk=None):
    if request.method == 'POST':
        if pk:
            employees = EmployeeProfile.objects.get(pk=pk)
            form = EmployeeProfileForm(request.POST, instance=setupclients)
        else:
            form = EmployeeProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        if (pk != 0):
            employees = EmployeeProfile.objects.get(pk=pk)
            form = EmployeeProfileForm(instance=employees)
        else:
            form = EmployeeProfileForm()

        args = {'form': form, 'title': 'Setup Client Account'}
        return render(request, 'smartsetup/form.html', args)


class EmployeesDetail(generic.DetailView):
    model = EmployeeProfile
    template_name = 'smartsetup/employees_detail.html'


class EmployeesDelete(generic.DeleteView):
    model = EmployeeProfile
    template_name = 'smartsetup/employees_delete.html'
    success_url = reverse_lazy('employees_list')


# SETUP CLIENTS
@login_required
def setupclients_list(request, pk=None):
    setupclients = SetupClients.objects
    fieldCols = ['Client Name', 'Address', 'Phone', 'Account Officer']
    args = {'fieldCols': fieldCols, 'setupclients': setupclients}
    return render(request, 'smartsetup/setupclients_list.html', args)


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

        args = {'form': form, 'title': 'Setup Client Account'}
        return render(request, 'smartsetup/form.html', args)


class SetupClientsDetail(generic.DetailView):
    model = SetupClients
    template_name = 'smartsetup/setupclients_detail.html'


class SetupClientsDelete(generic.DeleteView):
    model = SetupClients
    template_name = 'smartsetup/setupclients_delete.html'
    success_url = reverse_lazy('setupclients_list')


# SETUP VENDORS
@login_required
def setupvendors_list(request, pk=None):
    setupvendors = SetupVendors.objects
    fieldCols = ['Vendor Name', 'Address', 'Phone', 'Website']
    args = {'fieldCols': fieldCols, 'setupvendors': setupvendors}
    return render(request, 'smartsetup/setupvendors_list.html', args)


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

        args = {'form': form, 'title': 'Setup Vendor Account'}
        return render(request, 'smartsetup/setupvendor.html', args)


class SetupVendorsDetail(generic.DetailView):
    model = SetupVendors
    template_name = 'smartsetup/setupvendors_detail.html'


class SetupVendorsDelete(generic.DeleteView):
    model = SetupVendors
    template_name = 'smartsetup/setupvendors_delete.html'
    success_url = reverse_lazy('setupvendors_list')


# RECEIPT TRANSACTION
@login_required
def receipt_list(request, pk=None):
    receipts = ReceiptMain.objects.all()
    fieldCols = ['Receipt No.', 'Date', 'Issued To']
    args = {'fieldCols': fieldCols, 'receipts': receipts}
    return render(request, 'account/receipt_list.html', args)


class ReceiptClass(ListView):
    # model = ReceiptDetails.objects.filter(id = 0)
    model = ReceiptDetails
    template_name = 'account/receipt.html'
    # context_object_name = 'receiptitems'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_receipt'] = ReceiptMain.objects.aggregate(max_val=Coalesce(
            Max(Cast('receipt_number', output_field=PositiveIntegerField())), Value(1000)))
        context['client_name'] = SetupClients.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(
            category_code_id='3')
        context['revenue_acct'] = ChartSubCategory.objects.filter(
            category_code_id='1')
        # context['note_acct'] = ChartNoteItems.objects.all()
        ids = ChartSubCategory.objects.filter(
            category_code_id='3').values_list('id', flat=True)
        context['note_acct_cash'] = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        ids = ChartSubCategory.objects.filter(
            category_code_id='1').values_list('id', flat=True)
        context['note_acct'] = ChartNoteItems.objects.filter(
            sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        # context['note_acct'] = ChartNoteItems.objects.all().values(
        #     'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        return context


def receiptedit(request, pk=None):
    # pkMain = request.POST.get('idprov')
    # receiptmain = ReceiptMain.objects.get(id=pkMain)
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_sum = ReceiptDetails.objects.filter(
            receipt_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        receiptmain = ReceiptMain.objects.get(id=pk)
        receipt_number1 = ReceiptMain.objects.get(id=pk).receipt_number
        print('RECEIPT NO. RETRIEVED : ', receipt_number1)
        # cash_id = ReceiptMain.objects.get(id=pk).cash_account_id
        # debit_id = ReceiptMain.objects.get(id=pk).id

        receiptitems = ReceiptDetails.objects.filter(receipt_main_id_id=pk)

        # print('RECEIPT MAIN VALUES : ', receiptmain)

        client_name = SetupClients.objects.all()
        cash_acct = ChartSubCategory.objects.filter(category_code_id='3')
        revenue_acct = ChartSubCategory.objects.filter(category_code_id='1')
        ids = ChartSubCategory.objects.filter(
            category_code_id='3').values_list('id', flat=True)
        note_acct_cash = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        ids = ChartSubCategory.objects.filter(
            category_code_id='1').values_list('id', flat=True)
        note_acct = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        # note_acct = ChartNoteItems.objects.all()
        journal_list = GeneralLedger.objects.filter(
            ref_number=receipt_number1, journal_type='CRJ')
        print('RECEIPT JORNAL ITEMS : ', journal_list)
        trans_date = receiptmain.date.strftime("%Y-%m-%d")

        args = {'receiptmain': receiptmain, 'receiptitems': receiptitems, 'client_name': client_name,
                'cash_acct': cash_acct, 'revenue_acct': revenue_acct, 'note_acct_cash': note_acct_cash, 'note_acct': note_acct,
                'total_sum': total_sum, 'journal_list': journal_list, 'trans_date': trans_date}
        return render(request, 'account/receipt.html', args)
    else:
        return render(request, 'account/receipt_list.html')


class CreateReceipt(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('receipt def AJAX VIEW ')
        ClientID = ""
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
        total_amount = float(request.GET.get('total_amount', 0))

        amount2 = float(amount1.replace(',', ''))
        print('RECEIPT CASH ACCOUNT ID: ', cash_account1)
        print('RECEIPT CLIENT ID: ', client_name1)

        if client_name1:
            ClientID = SetupClients.objects.get(id=client_name1).id
        else:
            pass

        cashAccount = ChartSubCategory.objects.get(
            id=cash_account1).sub_category_name
        cashCategoryID = ChartSubCategory.objects.get(
            id=cash_account1).category_code_id
        DebitAccount = ChartNoteItems.objects.get(id=Debit_account1).item_name
        revenueAccount = ChartSubCategory.objects.get(
            id=revenue_account1).sub_category_name
        revenueCategoryID = ChartSubCategory.objects.get(
            id=revenue_account1).category_code_id
        creditAccount = ChartNoteItems.objects.get(
            id=credit_account1).item_name

        if pkMain:
            print('UPDATE EXISTING RECORD ')
            obj = ReceiptMain.objects.get(id=pkMain)
            obj.date = receipt_date1
            obj.receipt_number = receipt_number1
            obj.client = SetupClients.objects.get(id=client_name1)
            obj.bill_to = bill_to1
            obj.cash_account = ChartSubCategory.objects.get(id=cash_account1)
            obj.Debit_account = ChartNoteItems.objects.get(id=Debit_account1)
            obj.save()

            obj3 = GeneralLedger.objects.get(
                ref_number=receipt_number1, journal_type='CRJ', main_Trans=True)
            obj3.date = receipt_date1
            obj3.ref_number = receipt_number1
            obj3.journal_type = 'CRJ'
            obj3.account_id = ChartNoteItems.objects.get(id=Debit_account1)
            obj3.sub_category = ChartSubCategory.objects.get(id=cash_account1)
            obj3.category = ChartCategory.objects.get(id=cashCategoryID)
            obj3.description = bill_to1
            obj3.debit = total_amount + amount2
            obj3.save()

        else:
            # print('CLIENT SELECTED : ',SetupClients.objects.get(id = client_name1))
            # print('BEFORE : ',receipt_date1)

            # print('RETRIEVED CLIENT INFO:  ' , ClientID)
            if ClientID:
                obj = ReceiptMain.objects.create(
                    date=receipt_date1,
                    receipt_number=receipt_number1,
                    client_id=ClientID,
                    bill_to=bill_to1,
                    cash_account=ChartSubCategory.objects.get(
                        id=cash_account1),
                    Debit_account=ChartNoteItems.objects.get(
                        id=Debit_account1),
                )
            else:
                obj = ReceiptMain.objects.create(
                    date=receipt_date1,
                    receipt_number=receipt_number1,
                    bill_to=bill_to1,
                    cash_account=ChartSubCategory.objects.get(
                        id=cash_account1),
                    Debit_account=ChartNoteItems.objects.get(
                        id=Debit_account1),
                )

            # print('AFTER RETRIEVED')
            obj3 = GeneralLedger.objects.create(
                date=receipt_date1,
                ref_number=receipt_number1,
                journal_type='CRJ',
                account_id=ChartNoteItems.objects.get(id=Debit_account1),
                sub_category=ChartSubCategory.objects.get(id=cash_account1),
                category=ChartCategory.objects.get(id=cashCategoryID),
                description=bill_to1,
                debit=total_amount + amount2,
                main_Trans=True
            )

        obj2 = ReceiptDetails.objects.create(
            description=description,
            revenue_account=ChartSubCategory.objects.get(id=revenue_account1),
            credit_account=ChartNoteItems.objects.get(id=credit_account1),
            amount=amount2,
            receipt_main_id_id=obj.id,
        )

        obj4 = GeneralLedger.objects.create(
            date=receipt_date1,
            ref_number=receipt_number1,
            journal_type='CRJ',
            account_id=ChartNoteItems.objects.get(id=credit_account1),
            sub_category=ChartSubCategory.objects.get(id=revenue_account1),
            category=ChartCategory.objects.get(id=revenueCategoryID),
            description=description,
            credit=amount2,
        )

        # GeneralLedger.objects.filter(ref_number=obj.receipt_number, journal_type='CRJ').delete()

        total_sum = ReceiptDetails.objects.filter(
            receipt_main_id_id=obj.id).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=receipt_number1, journal_type='CRJ'))

        receipt_main = {'Mainid': obj.id, 'date': obj.date,
                        'receipt_number': obj.receipt_number, 'bill_to': obj.bill_to}

        receipt_sub = {'Subid': obj2.id, 'description': obj2.description, 'revenue_account': revenueAccount,
                       'credit_account': creditAccount, 'amount': obj2.amount}

        data = {
            'receipt_main': receipt_main,
            'receipt_sub': receipt_sub,
            'total_sum': total_sum,
            'journal_list': journal_list
        }
        return JsonResponse(data)


class GetAcctIDs(View):
    def get(self, request):
        print('GET ACCOUNT IDs AJAX VIEW ')
        creditAcct = request.GET.get('creditAcct', None)
        departAcct = request.GET.get('departAcct', None)
        budgetDepart = request.GET.get('budgetDepart', None)

        print('THE NOTE NAME IS : ', creditAcct)
        print('THE DEPARTMENT NAME IS : ', departAcct)
        # print('THE BUDGET DEPARTMENT NAME IS : ', budgetDepart)

        if departAcct:
            departAcct_id = BudgetDepartment.objects.get(department_name=departAcct).id
        else:
            departAcct_id = "0"

        # if budgetDepart:
        #     budgetDepart_id = BudgetDetails.objects.get(budget_item=budgetDepart).id
        # else:
        #     budgetDepart_id = "0"

        note_id = ChartNoteItems.objects.get(item_name=creditAcct).id
        cat_id = ChartNoteItems.objects.get(
            item_name=creditAcct).sub_category_id
            
        # print('THE DEPARTMENT ID IS : ', departAcct_id)
        print('THE NOTE ID IS : ', note_id)
        print('THE SUB-CATEGORY ID IS : ', cat_id)

        data = {
            'note_id': note_id,
            'cat_id': cat_id,
            'dept_id': departAcct_id,
            # 'receipt_sub': receipt_sub
        }
        return JsonResponse(data)


# EXPENSE TRANSACTION
@login_required
def expense_list(request, pk=None):
    expenses = ExpenseMain.objects
    fieldCols = ['Date', 'Expense No.', 'Description']
    args = {'fieldCols': fieldCols, 'expenses': expenses}
    return render(request, 'account/expense_list.html', args)


class ExpenseClass(ListView):
    model = ExpenseDetails
    template_name = 'account/expense.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_expense'] = ExpenseMain.objects.aggregate(max_val=Coalesce(
            Max(Cast('voucher_number', output_field=PositiveIntegerField())), Value(1000)))
        context['staff_name'] = EmployeeProfile.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(
            category_code_id='3')
        context['expense_acct'] = ChartSubCategory.objects.filter(
            category_code_id='2')
        ids = ChartSubCategory.objects.filter(
            category_code_id='2').values_list('id', flat=True)
        print('AM HERE NOW!!! :', ids)
        context['note_acct_exp'] = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        ids = ChartSubCategory.objects.filter(
            category_code_id='3').values_list('id', flat=True)
        context['note_acct_cash'] = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        context['department'] = BudgetDetails.objects.all()
        # context['department'] = BudgetDepartment.objects.all()

        return context


def expenseedit(request, pk=None):
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_sum = ExpenseDetails.objects.filter(
            expense_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        expensemain = ExpenseMain.objects.get(id=pk)
        expense_number1 = ExpenseMain.objects.get(id=pk).voucher_number
        # acct_cash = ExpenseMain.objects.get(id=pk).voucher_number
        print('EXPENSE NO. RETRIEVED : ', expense_number1)

        expenseitems = ExpenseDetails.objects.filter(
            expense_main_id_id=pk).values('budget_dept__budget_dept__department_name',
                                          'description', 'expense_account__sub_category_name', 
                                          'Debit_account__item_name', 'amount', 'id', 'budget_dept__id')

        staff_name = EmployeeProfile.objects.all()
        cash_acct = ChartSubCategory.objects.filter(category_code_id='3')
        expense_acct = ChartSubCategory.objects.filter(category_code_id='2')
        note_acct = ChartNoteItems.objects.all()
        ids = ChartSubCategory.objects.filter(
            category_code_id='3').values_list('id', flat=True)
        note_acct_cash = ChartNoteItems.objects.filter(
            sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        ids = ChartSubCategory.objects.filter(
            category_code_id='2').values_list('id', flat=True)
        note_acct_exp = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        # department = BudgetDepartment.objects.all()
        department = BudgetDetails.objects.all()

        journal_list = GeneralLedger.objects.filter(
            ref_number=expense_number1, journal_type='CDJ')
        print('EXPENSE JORNAL ITEMS : ', journal_list)
        trans_date = expensemain.date.strftime("%Y-%m-%d")

        args = {'expensemain': expensemain, 'expenseitems': expenseitems, 'staff_name': staff_name,
                'cash_acct': cash_acct, 'expense_acct': expense_acct, 'note_acct': note_acct,
                'note_acct_cash': note_acct_cash, 'department': department, 'total_sum': total_sum,
                'journal_list': journal_list, 'note_acct_exp': note_acct_exp, 'trans_date': trans_date}
        return render(request, 'account/expense.html', args)
    else:
        return render(request, 'account/expense_list.html')


class CreateExpense(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('receipt def AJAX VIEW ')

        expense_date1 = request.GET.get('trans_date', None)
        voucher_number1 = request.GET.get('voucher_number', None)
        client_name1 = request.GET.get('client_name', None)
        bill_to1 = request.GET.get('bill_to', None)
        cash_account1 = request.GET.get('cash_account', None)
        Debit_account1 = request.GET.get('credit_account', None)
        pkMain = request.GET.get('mainID', None)
        description = request.GET.get('description', None)
        expense_account1 = request.GET.get('expense_account', None)
        credit_account1 = request.GET.get('Debit_account', None)
        amount1 = request.GET.get('amount', 0)
        total_amount1 = request.GET.get('total_amount', 0)
        budget_dept2 = request.GET.get('budget_dept', None)
        pkSub = request.GET.get('subID', None)

        amount2 = float(amount1.replace(',', ''))
        total_amount = float(total_amount1.replace(',', ''))
        print('EXPENSE CASH ACCOUNT ID: ', cash_account1)
        print('EXPENSE BUDGET ID: ', budget_dept2)

        # ClientID = EmployeeProfile.objects.get(id=client_name1).id
        cashAccount = ChartSubCategory.objects.get(
            id=cash_account1).sub_category_name
        cashCategoryID = ChartSubCategory.objects.get(
            id=cash_account1).category_code_id
        creditAccount = ChartNoteItems.objects.get(
            id=credit_account1).item_name
        expenseAccount = ChartSubCategory.objects.get(
            id=expense_account1).sub_category_name
        expenseCategoryID = ChartSubCategory.objects.get(
            id=expense_account1).category_code_id
        DebitAccount = ChartNoteItems.objects.get(id=Debit_account1).item_name
        departmentId = BudgetDetails.objects.get(
            id=budget_dept2).budget_dept_id
        departmentName = BudgetDepartment.objects.get(
            id=departmentId).department_name
        budgetId = BudgetDetails.objects.get(
            id=budget_dept2).id

        if pkMain:
            print('VOUCHER NUMBER', voucher_number1)
            print('UPDATE EXISTING RECORD ')
            obj = ExpenseMain.objects.get(id=pkMain)
            obj.date = expense_date1
            obj.voucher_number = voucher_number1
            # obj.payee = EmployeeProfile.objects.get(id=client_name1)
            obj.description = bill_to1
            obj.cash_account = ChartSubCategory.objects.get(id=cash_account1)
            obj.credit_account = ChartNoteItems.objects.get(id=credit_account1)
            obj.save()

            obj3 = GeneralLedger.objects.get(
                ref_number=voucher_number1, journal_type='CDJ', main_Trans=True)
            obj3.date = expense_date1
            obj3.ref_number = voucher_number1
            obj3.journal_type = 'CDJ'
            obj3.account_id = ChartNoteItems.objects.get(id=credit_account1)
            obj3.sub_category = ChartSubCategory.objects.get(id=cash_account1)
            obj3.category = ChartCategory.objects.get(id=cashCategoryID)
            obj3.description = bill_to1
            obj3.credit = total_amount + amount2
            obj3.save()

        else:
            print('ENTER NEW EXPENSE RECORD ')

            obj = ExpenseMain.objects.create(
                date=expense_date1,
                voucher_number=voucher_number1,
                # payee_id=ClientID,
                description=bill_to1,
                cash_account=ChartSubCategory.objects.get(id=cash_account1),
                credit_account=ChartNoteItems.objects.get(id=Debit_account1),
            )
            # print('AFTER RETRIEVED')
            obj3 = GeneralLedger.objects.create(
                date=expense_date1,
                ref_number=voucher_number1,
                journal_type='CDJ',
                account_id=ChartNoteItems.objects.get(id=credit_account1),
                sub_category=ChartSubCategory.objects.get(id=cash_account1),
                category=ChartCategory.objects.get(id=cashCategoryID),
                description=bill_to1,
                credit=total_amount + amount2,
                main_Trans=True
            )

        if pkSub:
            print('EDIT EXPENSE DETAILS RECORD')
            obj2 = ExpenseDetails.objects.get(id=pkSub)
            obj2.description = description
            obj2.expense_account = ChartSubCategory.objects.get(id=expense_account1)
            obj2.Debit_account = ChartNoteItems.objects.get(id=Debit_account1)
            obj2.amount = amount2
            obj2.budget_dept = BudgetDetails.objects.get(id=budget_dept2)
            obj2.save()

        else:
            print('ADD EXPENSE DETAILS RECORD ')
            obj2 = ExpenseDetails.objects.create(
                description=description,
                expense_account=ChartSubCategory.objects.get(id=expense_account1),
                Debit_account=ChartNoteItems.objects.get(id=Debit_account1),
                amount=amount2,
                budget_dept=BudgetDetails.objects.get(id=budget_dept2),
                expense_main_id_id=obj.id,
            )

        obj4 = GeneralLedger.objects.create(
            date=expense_date1,
            ref_number=voucher_number1,
            journal_type='CDJ',
            account_id=ChartNoteItems.objects.get(id=Debit_account1),
            sub_category=ChartSubCategory.objects.get(id=expense_account1),
            category=ChartCategory.objects.get(id=expenseCategoryID),
            description=description,
            debit=amount2,
        )

        total_sum = ExpenseDetails.objects.filter(
            expense_main_id_id=obj.id).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number1, journal_type='CDJ'))

        expense_main = {'Mainid': obj.id, 'date': obj.date,
                        'voucher_number': obj.voucher_number, 'bill_to': obj.description}

        expense_sub = {'Subid': obj2.id, 'description': obj2.description, 'expense_account': expenseAccount,
                       'debit_account': DebitAccount, 'amount': obj2.amount, 'budget_dept': departmentName, 'budget_id': budgetId}

        data = {
            'expense_main': expense_main,
            'expense_sub': expense_sub,
            'total_sum': total_sum,
            'journal_list': journal_list
        }
        return JsonResponse(data)


# BUDGET TRANSACTION
@login_required
def budget_list(request, pk=None):
    budget = BudgetMain.objects
    fieldCols = ['Period Start', 'Period End', 'Description']
    args = {'fieldCols': fieldCols, 'budget': budget}
    return render(request, 'account/budget_list.html', args)


class BudgetClass(ListView):
    model = BudgetDetails
    template_name = 'account/budget.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_budget'] = BudgetMain.objects.aggregate(max_val=Coalesce(
            Max(Cast('budget_no', output_field=PositiveIntegerField())), Value(1000)))
        context['department'] = BudgetDepartment.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(
            category_code_id='3')

        context['expense_acct'] = ChartSubCategory.objects.all()
        # context['expense_acct'] = ChartSubCategory.objects.filter(
        #     category_code_id='2')
            
        ids = ChartSubCategory.objects.filter(
            Q(category_code_id='1') | Q(category_code_id='2') | Q(category_code_id='3') | Q(category_code_id='4')).values_list('id', flat=True)
        context['note_acct_exp'] = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        context['revenue_acct'] = ChartSubCategory.objects.filter(
            category_code_id='1')
        ids = ChartSubCategory.objects.filter(
            category_code_id='1').values_list('id', flat=True)
        context['note_acct_rev'] = ChartNoteItems.objects.filter(
            sub_category__in=ids)

        # print('AM HERE NOW!!! :', ids)

        return context


class BudgetSaveMain(View):
    # print('BUDGET SAVE MAIN')

    def get(self, request):
        # print('BUDGET SAVE MAIN VIEW ')

        period_start = request.GET.get('period_start', None)
        period_end = request.GET.get('period_end', None)
        voucher_number1 = request.GET.get('voucher_number', None)
        pkMain = request.GET.get('mainID', None)
        description = request.GET.get('description', None)

        if pkMain:
            print('UPDATE EXISTING RECORD ')
            obj = BudgetMain.objects.get(id=pkMain)
            obj.period_start = period_start
            obj.period_end = period_end
            obj.budget_no = voucher_number1
            obj.description = description
            obj.save()

        else:
            print('ENTER NEW BUDGET RECORD ')

            obj = BudgetMain.objects.create(
                period_start=period_start,
                period_end=period_end,
                budget_no=voucher_number1,
                description=description,
            )

        budget_main = {'Mainid': obj.id, 'period_start': obj.period_start,
                       'period_end': obj.period_end, 'voucher_number': obj.budget_no,
                       'description': obj.description}

        total_sum = BudgetDetails.objects.filter(
            budget_main_id_id=obj.id).aggregate(Sum('amount'))['amount__sum'] or 0.00

        data = {
            'budget_main': budget_main,
            'total_sum': total_sum,
        }
        return JsonResponse(data)


class CreateBudget(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('BUDGET def AJAX VIEW ')

        period_start = request.GET.get('period_start', None)
        period_end = request.GET.get('period_end', None)
        voucher_number1 = request.GET.get('voucher_number', None)
        department_name = request.GET.get('department_name', None)
        # bill_to1 = request.GET.get('bill_to', None)
        # cash_account1 = request.GET.get('cash_account', None)
        Debit_account1 = request.GET.get('credit_account', None)
        pkMain = request.GET.get('mainID', None)
        description = request.GET.get('description', None)
        expense_account1 = request.GET.get('expense_account', None)
        budget_type = request.GET.get('budget_type', None)
        amount1 = request.GET.get('amount', None)
        total_amount = float(request.GET.get('total_amount', 0))
        pkSub = request.GET.get('subID', None)

        amount2 = float(amount1.replace(',', ''))
        print('EXPENSE DEPARTMENT ID: ', department_name)

        department = BudgetDepartment.objects.get(
            id=department_name).department_name
        # cashAccount = ChartSubCategory.objects.get(
        #     id=cash_account1).sub_category_name
        # cashCategoryID = ChartSubCategory.objects.get(
        #     id=cash_account1).category_code_id
        # creditAccount = ChartNoteItems.objects.get(
        #     id=credit_account1).item_name
        expenseAccount = ChartSubCategory.objects.get(
            id=expense_account1).sub_category_name
        expenseCategoryID = ChartSubCategory.objects.get(
            id=expense_account1).category_code_id
        DebitAccount = ChartNoteItems.objects.get(id=Debit_account1).item_name

        if pkMain:
            print('UPDATE EXISTING RECORD ')
            obj = BudgetMain.objects.get(id=pkMain)
            obj.period_start = period_start
            obj.period_end = period_end
            obj.budget_no = voucher_number1
            obj.description = description
            obj.save()

        else:
            print('ENTER NEW BUDGET RECORD ')

            obj = BudgetMain.objects.create(
                period_start=period_start,
                period_end=period_end,
                budget_no=voucher_number1,
                description=description,
            )

        if pkSub:
            print('edit details')
            obj2 = BudgetDetails.objects.get(id=pkSub)
            obj2.budget_type = budget_type
            obj2.budget_cat = ChartSubCategory.objects.get(
                id=expense_account1)
            obj2.budget_item = ChartNoteItems.objects.get(id=Debit_account1)
            obj2.amount = amount2
            obj2.save()

        else:
            obj2 = BudgetDetails.objects.create(
                budget_type=budget_type,
                budget_dept=BudgetDepartment.objects.get(id=department_name),
                budget_cat=ChartSubCategory.objects.get(id=expense_account1),
                budget_item=ChartNoteItems.objects.get(id=Debit_account1),
                amount=amount2,
                budget_main_id_id=obj.id,
            )

        total_sum = BudgetDetails.objects.filter(
            budget_main_id_id=obj.id).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        budget_main = {'Mainid': obj.id, 'period_start': obj.period_start,
                       'period_end': obj.period_end, 'voucher_number': obj.budget_no,
                       'description': obj.description, 'budget_type': budget_type}

        budget_sub = {'Subid': obj2.id, 'department': department,
                      'debit_account': DebitAccount, 'amount': obj2.amount}

        # print('TOTAL DATA GENERATED : ')

        data = {
            'budget_main': budget_main,
            'budget_sub': budget_sub,
            'total_sum': total_sum,
        }
        return JsonResponse(data)


def budgetedit(request, pk=None):
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_sum = BudgetDetails.objects.filter(
            budget_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        budgetmain = BudgetMain.objects.get(id=pk)
        print('TOTAL SUM ')
        budget_number1 = BudgetMain.objects.get(id=pk).budget_no
        print('budget NO. RETRIEVED : ', budget_number1)

        budgetitems = BudgetDetails.objects.filter(
            budget_main_id_id=pk).order_by('budget_item')

        # staff_name = EmployeeProfile.objects.all()
        department = BudgetDepartment.objects.all()

        revenue_acct = ChartSubCategory.objects.filter(category_code_id='1')
        ids = ChartSubCategory.objects.filter(
            category_code_id='1').values_list('id', flat=True)
        note_acct_rev = ChartNoteItems.objects.filter(sub_category__in=ids)

        cash_acct = ChartSubCategory.objects.filter(category_code_id='3')
        expense_acct = ChartSubCategory.objects.all()
        # expense_acct = ChartSubCategory.objects.filter(category_code_id='2')

        ids = ChartSubCategory.objects.filter(
            Q(category_code_id='1') | Q(category_code_id='2') | Q(category_code_id='3') | Q(category_code_id='4')).values_list('id', flat=True)
        note_acct_exp = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        # note_acct = ChartNoteItems.objects.all()
        # journal_list = GeneralLedger.objects.filter(
        #     ref_number=expense_number1, journal_type='CDJ')
        # print('EXPENSE JORNAL ITEMS : ', journal_list)
        period_start = budgetmain.period_start.strftime("%Y-%m-%d")
        period_end = budgetmain.period_end.strftime("%Y-%m-%d")
        # period_end = budgetmain.period_end.strftime("%Y-%m-%dT%H:%M:%S")

        fieldCols = ['Department', 'Budget Account', 'Amount']

        args = {'budgetmain': budgetmain, 'budgetitems': budgetitems, 'department': department,
                'cash_acct': cash_acct, 'expense_acct': expense_acct, 'note_acct_exp': note_acct_exp,
                'revenue_acct': revenue_acct, 'note_acct_rev': note_acct_rev, 'total_sum': total_sum,
                'period_start': period_start, 'period_end': period_end, 'fieldCols': fieldCols}
        return render(request, 'account/budget.html', args)

        # budget = BudgetMain.objects
        # args = {'fieldCols': fieldCols,
        #         'budget': budget, 'budgetitems': budgetitems}
        # return render(request, 'account/budgetB.html', args)

    else:
        return render(request, 'account/budget_list.html')


# SETUP BUDGET DEPARTMENT
@login_required
def budgetdept_list(request, pk=None):
    budgetdept = BudgetDepartment.objects
    fieldCols = ['Department Code', 'Department Name', 'Description']
    args = {'fieldCols': fieldCols, 'budgetdept': budgetdept}
    return render(request, 'smartsetup/budgetdept_list.html', args)


@login_required
def budgetdept(request, pk=None):
    if request.method == 'POST':
        if pk:
            setupunit = BudgetDepartment.objects.get(pk=pk)
            form = BudgetDepartmentForm(request.POST, instance=setupunit)
        else:
            form = BudgetDepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('budgetdept_list')
    else:
        if (pk != 0):
            setupunit = BudgetDepartment.objects.get(pk=pk)
            form = BudgetDepartmentForm(instance=setupunit)
        else:
            form = BudgetDepartmentForm()

        args = {'form': form, 'title': 'Setup Department'}
        return render(request, 'smartsetup/form.html', args)


class BudgetDeptDetail(generic.DetailView):
    model = BudgetDepartment
    template_name = 'smartsetup/budgetdept_detail.html'


class BudgetDeptDelete(generic.DeleteView):
    model = BudgetDepartment
    template_name = 'smartsetup/budgetdept_delete.html'
    success_url = reverse_lazy('budgetdept_list')


# SETUP OPENING BALANCE
@login_required
def begbalance_list(request, pk=None):
    begbalance = SetupBegBalanceMain.objects
    fieldCols = ['Account Year', 'Start Date', 'End Date', 'Duration (months)']
    args = {'fieldCols': fieldCols, 'begbalance': begbalance}
    return render(request, 'account/begbalance_list.html', args)


class BegBalanceClass(ListView):
    model = SetupBegbalanceDetails
    template_name = 'account/begbalance.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_period'] = SetupBegBalanceMain.objects.aggregate(max_val=Coalesce(
            Max(Cast('periodno', output_field=PositiveIntegerField())), Value(0)))

        # context['expense_acct'] = ChartSubCategory.objects.all()
        context['expense_acct'] = ChartSubCategory.objects.filter().exclude(
            Q(category_code_id='1') | Q(category_code_id='2'))

        # context['note_acct'] = ChartNoteItems.objects.all().values(
        #     'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        context['note_acct'] = ChartNoteItems.objects.filter().exclude(Q(sub_category__category_code_id='1') | Q(sub_category__category_code_id='2')).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        return context


class CreateBegBalance(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('BEG BALANCE def AJAX CLASS ')

        expense_date1 = request.GET.get('trans_date', None)
        period_number = request.GET.get('period_number', None)
        acct_year = request.GET.get('acct_year', None)
        month_dur = request.GET.get('month_dur', None)
        period_start = request.GET.get('period_start', None)
        period_end = request.GET.get('period_end', None)
        pkMain = request.GET.get('mainID', None)
        description = request.GET.get('description', None)
        expense_account1 = request.GET.get('expense_account', None)
        credit_account1 = request.GET.get('credit_account', None)
        debit_amount = float(request.GET.get(
            'debit_amount', 0).replace(',', ''))
        credit_amount = float(request.GET.get(
            'credit_amount', 0).replace(',', ''))
        total_debit = float(request.GET.get('total_debit', 0))
        total_credit = float(request.GET.get('total_credit', 0))
        pkSub = request.GET.get('subID', None)

        print('TRANSACTION ACCOUNT ID: ', credit_account1)
        # print('EXPENSE CLIENT ID: ', client_name1)

        expenseAccount = ChartSubCategory.objects.get(
            id=expense_account1).sub_category_name
        expenseCategoryID = ChartSubCategory.objects.get(
            id=expense_account1).category_code_id
        creditAccount = ChartNoteItems.objects.get(
            id=credit_account1).item_name

        if pkMain:
            print('UPDATE EXISTING RECORD ')
            print('EXISTING RECORD DATE ', expense_date1)
            print('EXISTING RECORD MAIN ID ', pkMain)
            obj = SetupBegBalanceMain.objects.get(id=pkMain)
            obj.entrydate = expense_date1
            obj.periodno = period_number
            obj.year = acct_year
            obj.duration = month_dur
            obj.periodstart = period_start
            obj.periodend = period_end
            obj.save()

        else:
            print('ENTER NEW BEGBALANCE RECORD ')

            obj = SetupBegBalanceMain.objects.create(
                entrydate=expense_date1,
                periodno=period_number,
                year=acct_year,
                duration=month_dur,
                periodstart=period_start,
                periodend=period_end,
            )

        if pkSub:
            print('EDIT BEG BALANCE DETAILS')
            obj2 = SetupBegbalanceDetails.objects.get(id=pkSub)
            obj2.date = expense_date1
            obj2.description = description
            obj2.sub_category = ChartSubCategory.objects.get(
                id=expense_account1)
            obj2.account_id = ChartNoteItems.objects.get(id=credit_account1)
            obj2.debit = debit_amount
            obj2.credit = credit_amount
            obj2.save()

        else:
            print('CREATE NEW BEG BALANCE DETAILS')
            obj2 = SetupBegbalanceDetails.objects.create(
                date=expense_date1,
                description=description,
                sub_category=ChartSubCategory.objects.get(id=expense_account1),
                account_id=ChartNoteItems.objects.get(id=credit_account1),
                debit=debit_amount,
                credit=credit_amount,
                mainid_id=obj.id,
            )

        total_debit = SetupBegbalanceDetails.objects.filter(
            mainid_id=obj.id).aggregate(Sum('debit'))['debit__sum'] or 0.00
        total_credit = SetupBegbalanceDetails.objects.filter(
            mainid_id=obj.id).aggregate(Sum('credit'))['credit__sum'] or 0.00
        print('TOTAL DEBIT SUM GENERATED : ', total_debit)
        print('TOTAL CREDIT SUM GENERATED : ', total_credit)

        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=period_number, journal_type='BB'))

        expense_main = {'Mainid': obj.id, 'date': obj.entrydate, 'period_number': obj.periodno,
                        'acct_year': obj.year, 'period_start': obj.periodstart, 'period_end': obj.periodend}

        expense_sub = {'Subid': obj2.id, 'description': obj2.description, 'expense_account': expenseAccount,
                       'debit_account': creditAccount, 'debit': obj2.debit, 'credit': obj2.credit}

        print('TRANSACTION DETAILS : ', expense_sub)

        data = {
            'expense_main': expense_main,
            'expense_sub': expense_sub,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'journal_list': journal_list
        }
        return JsonResponse(data)


def begbalanceedit(request, pk=None):
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_debit = SetupBegbalanceDetails.objects.filter(
            mainid_id=pk).aggregate(Sum('debit'))['debit__sum'] or 0.00
        total_credit = SetupBegbalanceDetails.objects.filter(
            mainid_id=pk).aggregate(Sum('credit'))['credit__sum'] or 0.00
        print('TOTAL DEBIT GENERATED : ', total_debit)

        expensemain = SetupBegBalanceMain.objects.get(id=pk)
        ref_number1 = SetupBegBalanceMain.objects.get(id=pk).periodno
        entry_date = SetupBegBalanceMain.objects.get(id=pk).entrydate
        # ref_number1 = SetupBegBalanceMain.objects.get(id=pk).periodno
        # ref_number1 = SetupBegBalanceMain.objects.get(id=pk).periodno
        print('PERIOD NO. RETRIEVED : ', ref_number1)
        print('ENTRY DATE. RETRIEVED : ', entry_date)

        expenseitems = SetupBegbalanceDetails.objects.filter(mainid_id=pk)

        # expense_acct = ChartSubCategory.objects.all()
        expense_acct = ChartSubCategory.objects.filter().exclude(
            Q(category_code_id='1') | Q(category_code_id='2'))

        # note_acct = ChartNoteItems.objects.all().values(
        #     'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        note_acct = ChartNoteItems.objects.filter().exclude(Q(sub_category__category_code_id='1') | Q(sub_category__category_code_id='2')).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        journal_list = GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='BB')
        print('JOURNAL ITEMS : ', journal_list)

        args = {'expensemain': expensemain, 'expenseitems': expenseitems,
                'expense_acct': expense_acct, 'note_acct': note_acct, 'total_debit': total_debit,
                'total_credit': total_credit, 'journal_list': journal_list,
                'entry_date': entry_date}
        return render(request, 'account/begbalance.html', args)
    else:
        return render(request, 'account/begbalance_list.html')


@login_required
def begbalance_savemain(request):
    print('BEG BALANCE def AJAX CLASS ')

    expense_date1 = request.GET.get('trans_date', None)
    period_number = request.GET.get('period_number', None)
    acct_year = request.GET.get('acct_year', None)
    month_dur = request.GET.get('month_dur', None)
    period_start = request.GET.get('period_start', None)
    period_end = request.GET.get('period_end', None)
    pkMain = request.GET.get('mainID', None)

    if pkMain:
        print('UPDATE EXISTING RECORD ')
        print('EXISTING RECORD DATE ', expense_date1)
        print('EXISTING RECORD MAIN ID ', pkMain)
        obj = SetupBegBalanceMain.objects.get(id=pkMain)
        obj.entrydate = expense_date1
        obj.periodno = period_number
        obj.year = acct_year
        obj.duration = month_dur
        obj.periodstart = period_start
        obj.periodend = period_end
        obj.save()
    else:
        print('ENTER NEW BEGBALANCE RECORD ')

        obj = SetupBegBalanceMain.objects.create(
            entrydate=expense_date1,
            periodno=period_number,
            year=acct_year,
            duration=month_dur,
            periodstart=period_start,
            periodend=period_end,
        )

    expense_main = {'Mainid': obj.id, 'date': obj.entrydate, 'period_number': obj.periodno,
                    'acct_year': obj.year, 'period_start': obj.periodstart, 'period_end': obj.periodend}

    data = {
        'expense_main': expense_main,
    }
    return JsonResponse(data)


@login_required
def begbalance_post(request):
    ref_number1 = request.GET.get('ref_number', None)
    pkMain = request.GET.get('mainID', None)
    trans_date = request.GET.get('trans_date', None)

    print('BEG. BALANCE POST VIEW REF NO', ref_number1)
    print('BEG. BALANCE POST VIEW PK', pkMain)

    GeneralLedger.objects.filter(
        ref_number=ref_number1, journal_type='BB').delete()

    for e in SetupBegbalanceDetails.objects.filter(mainid_id=pkMain):
        # print(e.description)
        expenseCategoryID = ChartSubCategory.objects.get(
            id=e.sub_category_id).category_code_id

        print('BEG. BALANCE ACCT. CODE', expenseCategoryID)
        obj4 = GeneralLedger.objects.create(
            date=trans_date,
            ref_number=ref_number1,
            journal_type='BB',
            account_id=ChartNoteItems.objects.get(id=e.account_id_id),
            sub_category=ChartSubCategory.objects.get(id=e.sub_category_id),
            category=ChartCategory.objects.get(id=expenseCategoryID),
            description=e.description,
            debit=e.debit,
            credit=e.credit,
        )

    data = {}
    return JsonResponse(data)


# GENERAL JOURNAL TRANSACTION
@login_required
def gjournal_list(request, pk=None):
    gjournal = GJournalMain.objects
    fieldCols = ['Date', 'Journal No.', 'Description']
    args = {'fieldCols': fieldCols, 'gjournal': gjournal}
    return render(request, 'account/gjournal_list.html', args)


class GJournalClass(ListView):
    model = GJournalDetails
    template_name = 'account/gjournal.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_expense'] = GJournalMain.objects.aggregate(max_val=Coalesce(
            Max(Cast('ref_number', output_field=PositiveIntegerField())), Value(1000)))
        context['staff_name'] = EmployeeProfile.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(
            category_code_id='3')

        context['expense_acct'] = ChartSubCategory.objects.all()
        context['note_acct'] = ChartNoteItems.objects.all().values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        # context['expense_acct'] = ChartSubCategory.objects.all()
        # context['note_acct'] = ChartNoteItems.objects.all()

        return context


@login_required
def gjournal_post(request):
    ref_number1 = request.GET.get('ref_number', None)
    pkMain = request.GET.get('mainID', None)
    trans_date = request.GET.get('trans_date', None)

    print('GJOURNAL POST VIEW PK', ref_number1)

    GeneralLedger.objects.filter(
        ref_number=ref_number1, journal_type='GJ').delete()

    for e in GJournalDetails.objects.filter(journal_main_id_id=pkMain):
        # print(e.description)
        expenseCategoryID = ChartSubCategory.objects.get(
            id=e.sub_category_id).category_code_id

        obj4 = GeneralLedger.objects.create(
            date=trans_date,
            ref_number=ref_number1,
            journal_type='GJ',
            account_id=ChartNoteItems.objects.get(id=e.account_id),
            sub_category=ChartSubCategory.objects.get(id=e.sub_category_id),
            category=ChartCategory.objects.get(id=expenseCategoryID),
            description=e.description,
            debit=e.debit,
            credit=e.credit,
        )

    data = {}
    return JsonResponse(data)


class CreateGJournal(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('Gournal def AJAX VIEW ')

        expense_date1 = request.GET.get('trans_date', None)
        voucher_number1 = request.GET.get('voucher_number', None)
        bill_to1 = request.GET.get('bill_to', None)
        # cash_account1 = request.GET.get('cash_account', None)
        # Debit_account1 = request.GET.get('Debit_account', None)
        pkMain = request.GET.get('mainID', None)
        description = request.GET.get('description', None)
        expense_account1 = request.GET.get('expense_account', None)
        credit_account1 = request.GET.get('credit_account', None)
        debit_amount = float(request.GET.get(
            'debit_amount', 0).replace(',', ''))
        credit_amount = float(request.GET.get(
            'credit_amount', 0).replace(',', ''))
        total_debit = float(request.GET.get('total_debit', 0))
        total_credit = float(request.GET.get('total_credit', 0))
        pkSub = request.GET.get('subID', None)

        print('TRANSACTION ACCOUNT ID: ', credit_account1)
        # print('EXPENSE CLIENT ID: ', client_name1)

        # ClientID = EmployeeProfile.objects.get(id = client_name1).id
        # cashAccount = ChartSubCategory.objects.get(id = cash_account1).sub_category_name
        # cashCategoryID = ChartSubCategory.objects.get(id = cash_account1).category_code_id
        # DebitAccount = ChartNoteItems.objects.get(id = Debit_account1).item_name
        expenseAccount = ChartSubCategory.objects.get(
            id=expense_account1).sub_category_name
        expenseCategoryID = ChartSubCategory.objects.get(
            id=expense_account1).category_code_id
        creditAccount = ChartNoteItems.objects.get(
            id=credit_account1).item_name

        if pkMain:
            print('UPDATE EXISTING GENERAL JOURNAL RECORD MAIN')
            obj = GJournalMain.objects.get(id=pkMain)
            obj.date = expense_date1
            obj.ref_number = voucher_number1
            obj.description = bill_to1
            obj.save()

        else:
            print('ENTER GENERAL JOURNAL RECORD MAIN ')

            obj = GJournalMain.objects.create(
                date=expense_date1,
                ref_number=voucher_number1,
                description=bill_to1,
            )

        if pkSub:
            print('EDIT GENERAL JOURNAL DETAILS')
            obj2 = GJournalDetails.objects.get(id=pkSub)
            obj2.description = description
            obj2.sub_category = ChartSubCategory.objects.get(
                id=expense_account1)
            obj2.account = ChartNoteItems.objects.get(id=credit_account1)
            obj2.debit = debit_amount
            obj2.credit = credit_amount
            obj2.save()

        else:
            print('CREATE NEW GENERAL JOURNAL DETAILS')
            obj2 = GJournalDetails.objects.create(
                description=description,
                sub_category=ChartSubCategory.objects.get(id=expense_account1),
                account=ChartNoteItems.objects.get(id=credit_account1),
                debit=debit_amount,
                credit=credit_amount,
                journal_main_id_id=obj.id,
            )

        # print('CREATE GENERAL JOURNAL DETAILS')
        # obj2 = GJournalDetails.objects.create(
        #     description=description,
        #     sub_category=ChartSubCategory.objects.get(id=expense_account1),
        #     account=ChartNoteItems.objects.get(id=credit_account1),
        #     debit=debit_amount,
        #     credit=credit_amount,
        #     journal_main_id_id=obj.id,
        # )

        total_debit = GJournalDetails.objects.filter(
            journal_main_id_id=obj.id).aggregate(Sum('debit'))['debit__sum'] or 0.00
        total_credit = GJournalDetails.objects.filter(
            journal_main_id_id=obj.id).aggregate(Sum('credit'))['credit__sum'] or 0.00
        print('TOTAL DEBIT SUM GENERATED : ', total_debit)
        print('TOTAL CREDIT SUM GENERATED : ', total_credit)

        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number1, journal_type='GJ'))

        expense_main = {'Mainid': obj.id, 'date': obj.date,
                        'voucher_number': obj.ref_number, 'bill_to': obj.description}

        expense_sub = {'Subid': obj2.id, 'description': obj2.description, 'expense_account': expenseAccount,
                       'debit_account': creditAccount, 'debit': obj2.debit, 'credit': obj2.credit}

        data = {
            'expense_main': expense_main,
            'expense_sub': expense_sub,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'journal_list': journal_list
        }
        return JsonResponse(data)


def gjournaledit(request, pk=None):
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_debit = GJournalDetails.objects.filter(
            journal_main_id_id=pk).aggregate(Sum('debit'))['debit__sum'] or 0.00
        total_credit = GJournalDetails.objects.filter(
            journal_main_id_id=pk).aggregate(Sum('credit'))['credit__sum'] or 0.00
        print('TOTAL DEBIT GENERATED : ', total_debit)

        expensemain = GJournalMain.objects.get(id=pk)
        ref_number1 = GJournalMain.objects.get(id=pk).ref_number
        print('EXPENSE NO. RETRIEVED : ', ref_number1)

        expenseitems = GJournalDetails.objects.filter(journal_main_id_id=pk)

        # expense_acct = ChartSubCategory.objects.all()
        # note_acct = ChartNoteItems.objects.all()
        expense_acct = ChartSubCategory.objects.all()
        note_acct = ChartNoteItems.objects.all().values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        journal_list = GeneralLedger.objects.filter(
            ref_number=ref_number1, journal_type='GJ')
        # print('EXPENSE JORNAL ITEMS : ', journal_list)

        args = {'expensemain': expensemain, 'expenseitems': expenseitems,
                'expense_acct': expense_acct, 'note_acct': note_acct, 'total_debit': total_debit,
                'total_credit': total_credit, 'journal_list': journal_list, }
        return render(request, 'account/gjournal.html', args)
    else:
        return render(request, 'account/gjournal_list.html')


# PURCHASE TRANSACTIONS
@login_required
def purchase_list(request, pk=None):
    expenses = PurchaseMain.objects
    fieldCols = ['Date', 'Purchase No.', 'Description']
    args = {'fieldCols': fieldCols, 'expenses': expenses}
    return render(request, 'account/purchase_list.html', args)


class PurchaseClass(ListView):
    model = PurchaseDetails
    template_name = 'account/purchase.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Sub Category

        context['max_expense'] = PurchaseMain.objects.aggregate(max_val=Coalesce(
            Max(Cast('voucher_number', output_field=PositiveIntegerField())), Value(1000)))
        context['vendor_name'] = SetupVendors.objects.all()
        context['cash_acct'] = ChartSubCategory.objects.filter(
            category_code_id='3')
        context['expense_acct'] = ChartSubCategory.objects.filter(
            Q(id='24') | Q(id='26'))

        ids = ChartSubCategory.objects.filter(
            id='24').values_list('id', flat=True)
        print('AM HERE NOW!!! :', ids)
        context['inventory_items'] = SetupInventoryItems.objects.all()
        context['note_acct_inventory'] = ChartNoteItems.objects.filter(
            sub_category__in=ids)
        ids = ChartSubCategory.objects.filter(
            id='21').values_list('id', flat=True)
        context['note_acct_cash'] = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')
        # context['note_acct'] = ChartNoteItems.objects.all()

        return context


class CreatePurchase(View):
    # print('receipt AJAX VIEW ')
    def get(self, request):
        print('Purchase def AJAX VIEW ')

        purchase_date1 = request.GET.get('trans_date', None)
        voucher_number1 = request.GET.get('voucher_number', None)
        pay_mode = request.GET.get('pay_mode', None)
        vendor_name1 = request.GET.get('vendor_name', None)
        bill_to1 = request.GET.get('bill_to', None)
        cash_account1 = request.GET.get('cash_account', None)
        Debit_account1 = request.GET.get('credit_account', None)
        pkMain = request.GET.get('mainID', None)
        purchase_item = request.GET.get('inventory_item', None)
        description = request.GET.get('description', None)
        purchase_account1 = request.GET.get('expense_account', None)
        credit_account1 = request.GET.get('Debit_account', None)
        unit_price = request.GET.get('unit_price', None)
        quantity = request.GET.get('quantity', None)
        amount1 = request.GET.get('amount', None)
        total_amount = float(request.GET.get('total_amount', 0))
        optionSelect = request.GET.get('optionSelect', None)

        amount2 = float(amount1.replace(',', ''))
        print('PURCHASE CASH ACCOUNT ID: ', cash_account1)
        print('PURCHASE CLIENT ID: ', vendor_name1)

        if vendor_name1:
            vendorID = SetupVendors.objects.get(id=vendor_name1).id

        cashAccount = ChartSubCategory.objects.get(
            id=cash_account1).sub_category_name
        cashCategoryID = ChartSubCategory.objects.get(
            id=cash_account1).category_code_id
        creditAccount = ChartNoteItems.objects.get(
            id=credit_account1).item_name
        purchaseAccount = ChartSubCategory.objects.get(
            id=purchase_account1).sub_category_name
        purchaseCategoryID = ChartSubCategory.objects.get(
            id=purchase_account1).category_code_id
        DebitAccount = ChartNoteItems.objects.get(id=Debit_account1).item_name

        if pkMain:
            print('UPDATE EXISTING PURCHASE RECORD ')
            obj = PurchaseMain.objects.get(id=pkMain)
            obj.date = purchase_date1
            obj.voucher_number = voucher_number1
            # obj.vendor = SetupVendors.objects.get(id=vendor_name1)
            obj.description = bill_to1
            obj.cash_account = ChartSubCategory.objects.get(id=cash_account1)
            obj.credit_account = ChartNoteItems.objects.get(id=credit_account1)
            obj.pay_mode = pay_mode
            obj.save()

            obj3 = GeneralLedger.objects.get(
                ref_number=voucher_number1, journal_type='PJ', main_Trans=True)
            obj3.date = purchase_date1
            obj3.ref_number = voucher_number1
            obj3.journal_type = 'PJ'
            obj3.account_id = ChartNoteItems.objects.get(id=credit_account1)
            obj3.sub_category = ChartSubCategory.objects.get(id=cash_account1)
            obj3.category = ChartCategory.objects.get(id=cashCategoryID)
            obj3.description = bill_to1
            obj3.credit = total_amount + amount2
            obj3.save()

        else:
            print('POST NEW PURCHASE RECORD ')

            obj = PurchaseMain.objects.create(
                date=purchase_date1,
                voucher_number=voucher_number1,
                # vendor=SetupVendors.objects.get(id=vendor_name1),
                description=bill_to1,
                cash_account=ChartSubCategory.objects.get(id=cash_account1),
                credit_account=ChartNoteItems.objects.get(id=credit_account1),
                pay_mode=pay_mode,
            )

            print('POST GENERAL LEDGER RECORD')
            obj3 = GeneralLedger.objects.create(
                date=purchase_date1,
                ref_number=voucher_number1,
                journal_type='PJ',
                account_id=ChartNoteItems.objects.get(id=credit_account1),
                sub_category=ChartSubCategory.objects.get(id=cash_account1),
                category=ChartCategory.objects.get(id=cashCategoryID),
                description=bill_to1,
                credit=total_amount + amount2,
                main_Trans=True
            )

        if optionSelect == 'inventory':
            print('POST INVENTORY PURCHASE DETAILS ')
            obj2 = PurchaseDetails.objects.create(
                inventory_item=SetupInventoryItems.objects.get(
                    id=purchase_item),
                description=description,
                expense_account=ChartSubCategory.objects.get(
                    id=purchase_account1),
                Debit_account=ChartNoteItems.objects.get(id=Debit_account1),
                unit_price=unit_price,
                quantity=quantity,
                amount=amount2,
                expense_main_id_id=obj.id,
            )
        else:
            print('POST ASSET PURCHASE DETAILS ')
            obj2 = PurchaseDetails.objects.create(
                asset_item=SetupFixedAssets.objects.get(id=purchase_item),
                description=description,
                expense_account=ChartSubCategory.objects.get(
                    id=purchase_account1),
                Debit_account=ChartNoteItems.objects.get(id=Debit_account1),
                unit_price=unit_price,
                quantity=quantity,
                amount=amount2,
                asset=True,
                expense_main_id_id=obj.id,
            )

        print('POST PURCHASE DETAILS LEDGER RECORD ')
        obj4 = GeneralLedger.objects.create(
            date=purchase_date1,
            ref_number=voucher_number1,
            journal_type='PJ',
            account_id=ChartNoteItems.objects.get(id=Debit_account1),
            sub_category=ChartSubCategory.objects.get(id=purchase_account1),
            category=ChartCategory.objects.get(id=purchaseCategoryID),
            description=description,
            debit=amount2,
        )

        total_sum = PurchaseDetails.objects.filter(
            expense_main_id_id=obj.id).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        journal_list = serializers.serialize(
            "json", GeneralLedger.objects.filter(ref_number=voucher_number1, journal_type='PJ'))

        purchase_main = {'Mainid': obj.id, 'date': obj.date,
                         'voucher_number': obj.voucher_number, 'bill_to': obj.description}

        purchase_sub = {'Subid': obj2.id, 'inventory_item': obj2.inventory_item, 'Debit_account': obj2.Debit_account,
                        'unit_price': obj2.unit_price, 'quantity': quantity, 'amount': obj2.amount}

        data = {
            'purchase_main': purchase_main,
            'purchase_sub': purchase_sub,
            'total_sum': total_sum,
            'journal_list': journal_list
        }
        return JsonResponse(data)


def purchaseedit(request, pk=None):
    print('AM HERE NOW!!!')
    if pk:
        print('PK RETRIEVED : ', pk)

        total_sum = PurchaseDetails.objects.filter(
            expense_main_id_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0.00
        print('TOTAL SUM GENERATED CREATED : ', total_sum)

        expensemain = PurchaseMain.objects.get(id=pk)
        expense_number1 = PurchaseMain.objects.get(id=pk).voucher_number
        print('EXPENSE NO. RETRIEVED : ', expense_number1)

        expenseitems = PurchaseDetails.objects.filter(expense_main_id_id=pk)

        vendor_name = SetupVendors.objects.all()
        ids = ChartSubCategory.objects.filter(
            id='24').values_list('id', flat=True)
        inventory_items = SetupInventoryItems.objects.all()
        note_acct_inventory = ChartNoteItems.objects.filter(
            sub_category__in=ids)
        ids = ChartSubCategory.objects.filter(
            id='21').values_list('id', flat=True)
        note_acct_cash = ChartNoteItems.objects.filter(sub_category__in=ids).values(
            'id', 'item_name', 'sub_category__sub_category_name', 'sub_category__category_code__category_name')

        cash_acct = ChartSubCategory.objects.filter(category_code_id='3')
        # expense_acct = ChartSubCategory.objects.filter(category_code_id='2')
        expense_acct = ChartSubCategory.objects.filter(Q(id='24') | Q(id='26'))
        note_acct = ChartNoteItems.objects.all()

        journal_list = GeneralLedger.objects.filter(
            ref_number=expense_number1, journal_type='PJ')
        # print('PURCHASE JORNAL ITEMS : ', journal_list)

        args = {'expensemain': expensemain, 'expenseitems': expenseitems, 'vendor_name': vendor_name,
                'cash_acct': cash_acct, 'expense_acct': expense_acct, 'note_acct': note_acct,
                'note_acct_cash': note_acct_cash, 'note_acct_inventory': note_acct_inventory,
                'total_sum': total_sum, 'journal_list': journal_list, }
        return render(request, 'account/purchase.html', args)
    else:
        return render(request, 'account/purchase_list.html')


@login_required
def purchase_post(request):
    # ref_number1 = request.GET.get('ref_number', None)
    # pkMain = request.GET.get('mainID', None)
    # trans_date = request.GET.get('trans_date', None)

    purchase_date1 = request.GET.get('trans_date', None)
    voucher_number1 = request.GET.get('voucher_number', None)
    pay_mode = request.GET.get('pay_mode', None)
    vendor_name1 = request.GET.get('vendor_name', None)
    bill_to1 = request.GET.get('bill_to', None)
    cash_account1 = request.GET.get('cash_account', None)
    credit_account1 = request.GET.get('Debit_account', None)
    pkMain = request.GET.get('mainID', None)
    total_amount = float(request.GET.get('total_amount', 0))

    print('PURCHASE POST VIEW PK', voucher_number1)

    GeneralLedger.objects.filter(
        ref_number=voucher_number1, journal_type='PJ').delete()

    if pkMain:
        print('UPDATE EXISTING PURCHASE RECORD ')
        obj = PurchaseMain.objects.get(id=pkMain)
        obj.date = purchase_date1
        obj.voucher_number = voucher_number1
        # obj.vendor = SetupVendors.objects.get(id=vendor_name1)
        obj.description = bill_to1
        obj.cash_account = ChartSubCategory.objects.get(id=cash_account1)
        obj.credit_account = ChartNoteItems.objects.get(id=credit_account1)
        obj.pay_mode = pay_mode
        obj.save()

        obj3 = GeneralLedger.objects.get(
            ref_number=voucher_number1, journal_type='PJ', main_Trans=True)
        obj3.date = purchase_date1
        obj3.ref_number = voucher_number1
        obj3.journal_type = 'PJ'
        obj3.account_id = ChartNoteItems.objects.get(id=credit_account1)
        obj3.sub_category = ChartSubCategory.objects.get(id=cash_account1)
        obj3.category = ChartCategory.objects.get(id=cashCategoryID)
        obj3.description = bill_to1
        obj3.credit = total_amount
        obj3.save()

        for e in PurchaseDetails.objects.filter(expense_main_id_id=pkMain):
            # print(e.description)
            expenseCategoryID = ChartSubCategory.objects.get(
                id=e.expense_account_id).category_code_id

            obj4 = GeneralLedger.objects.create(
                date=purchase_date1,
                ref_number=voucher_number1,
                journal_type='PJ',
                account_id=ChartNoteItems.objects.get(id=e.Debit_account_id),
                sub_category=ChartSubCategory.objects.get(
                    id=e.expense_account_id),
                category=ChartCategory.objects.get(id=expenseCategoryID),
                description=e.description,
                debit=e.amount,
            )

    else:
        print('POST NEW PURCHASE RECORD ')

        obj = PurchaseMain.objects.create(
            date=purchase_date1,
            voucher_number=voucher_number1,
            # vendor=SetupVendors.objects.get(id=vendor_name1),
            description=bill_to1,
            cash_account=ChartSubCategory.objects.get(id=cash_account1),
            credit_account=ChartNoteItems.objects.get(id=credit_account1),
            pay_mode=pay_mode,
        )

        print('POST GENERAL LEDGER RECORD')
        obj3 = GeneralLedger.objects.create(
            date=purchase_date1,
            ref_number=voucher_number1,
            journal_type='PJ',
            account_id=ChartNoteItems.objects.get(id=credit_account1),
            sub_category=ChartSubCategory.objects.get(id=cash_account1),
            category=ChartCategory.objects.get(id=cashCategoryID),
            description=bill_to1,
            credit=total_amount,
            main_Trans=True
        )

    data = {}
    return JsonResponse(data)


# JOURNAL VIEW

def journalview(request, pk=None, jt=None):
    print('JOURNAL REF : ', pk)
    print('JORNAL TYPE : ', jt)

    if jt == 'CDJ':
        j_title = 'Cash Disbursement Journal'
    elif jt == 'CRJ':
        j_title = 'Cash Receipt Journal'
    elif jt == 'GJ':
        j_title = 'General Journal'
    elif jt == 'PJ':
        j_title = 'Purchase Journal'
    else:
        j_title = 'Journal View'

    ref_num = pk
    journal_list = GeneralLedger.objects.filter(
        ref_number=ref_num, journal_type=jt)

    # print('JORNAL ITEMS : ', journal_list)

    return render(request, 'account/journal_view.html', {
        'journal_title': j_title,
        'journal_list': journal_list,
        'ref_num': ref_num,
    })


def noteview(request, pk=None):
    print('JOURNAL REF : ', pk)

    categories = GeneralLedger.objects.filter(sub_category__notes=pk).exclude(category_id__isnull=True).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes', 'category').annotate(totaldebit=Sum('debit'), totalcredit=Sum('credit')).order_by('sub_category__notes')
    items = GeneralLedger.objects.filter(sub_category__notes=pk).exclude(category_id__isnull=True).values(
        'account_id', 'account_id__item_name', 'sub_category', 'category').annotate(debit=Sum('debit'), credit=Sum('credit')).order_by('account_id__item_name')

    print('THE CATEGORIES ARE: ', categories)
    print('THE ITEMS ARE: ', items)

    args = {'category': categories, 'items': items}

    return render(request, 'smartsetup/financialnotes_byitem.html', args)


# REPORTS
@login_required
def financialperformance(request):
    # revenues = ChartSubCategory.objects.filter(category_code_id=1)
    # expenses = ChartSubCategory.objects.filter(category_code_id=2)

    # revenues = GeneralLedger.objects.filter(category_id=1)
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')
    revenues = GeneralLedger.objects.filter(category_id=1).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(credit=Sum('credit'))
    expenses = GeneralLedger.objects.filter(category_id=2).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(debit=Sum('debit'))
    total_revenue = GeneralLedger.objects.filter(
        category_id=1).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_expense = GeneralLedger.objects.filter(
        category_id=2).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_balance = (total_revenue - total_expense)
    print('RETURNED REVENUE : ', revenues)
    print('TOTAL REVENUE : ', total_revenue)
    print('RETURNED EXPENSES : ', expenses)
    print('COMPANY INFO : ', companyinfo)

    args = {'revenues': revenues, 'expenses': expenses, 'total_revenue': total_revenue,
            'total_expense': total_expense, 'total_balance': total_balance,
            'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialperformance.html', args)


@login_required
def financialposition(request, pk=None):

    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')

    # ASSETS
    curr_assets = GeneralLedger.objects.filter(category_id=3).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(debit=Sum('debit'), credit=-Sum('credit'))
    noncurr_assets = GeneralLedger.objects.filter(category_id=4).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(debit=Sum('debit'), credit=-Sum('credit'))

    total_curr_assets_debit = GeneralLedger.objects.filter(
        category_id=3).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_curr_assets_credit = GeneralLedger.objects.filter(
        category_id=3).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_curr_assets = total_curr_assets_debit - total_curr_assets_credit

    total_Ncurr_assets_debit = GeneralLedger.objects.filter(
        category_id=4).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_Ncurr_assets_credit = GeneralLedger.objects.filter(
        category_id=4).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_Ncurr_assets = total_Ncurr_assets_debit - total_Ncurr_assets_credit

    total_assets = total_curr_assets + total_Ncurr_assets

    # LIABITILIES
    curr_liab = GeneralLedger.objects.filter(category_id=5).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(credit=Sum('credit'), debit=-Sum('debit'))
    noncurr_liab = GeneralLedger.objects.filter(category_id=6).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(credit=Sum('credit'), debit=-Sum('debit'))

    total_curr_liab_debit = GeneralLedger.objects.filter(
        category_id=5).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_curr_liab_credit = GeneralLedger.objects.filter(
        category_id=5).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_curr_liab = total_curr_liab_credit - total_curr_liab_debit

    total_Ncurr_liab_debit = GeneralLedger.objects.filter(
        category_id=6).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_Ncurr_liab_credit = GeneralLedger.objects.filter(
        category_id=6).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_Ncurr_liab = total_Ncurr_liab_credit - total_Ncurr_liab_debit

    total_liabilities = total_curr_liab + total_Ncurr_liab

    # NET ASSET
    net_assets = total_assets - total_liabilities

    total_revenue = GeneralLedger.objects.filter(
        category_id=1).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_expense = GeneralLedger.objects.filter(
        category_id=2).aggregate(Sum('debit'))['debit__sum'] or 0.00
    accum_supplus = (total_revenue - total_expense)
    reserves = 0.00
    total_net_assetEq = reserves + accum_supplus

    print('TOTAL REVENUE : ', total_curr_assets)

    args = {'curr_assets': curr_assets, 'noncurr_assets': noncurr_assets, 'total_assets': total_assets,
            'total_curr_assets': total_curr_assets, 'total_Ncurr_assets': total_Ncurr_assets,
            'curr_liab': curr_liab, 'noncurr_liab': noncurr_liab, 'total_liabilities': total_liabilities,
            'total_curr_liab': total_curr_liab, 'total_Ncurr_liab': total_Ncurr_liab,
            'net_assets': net_assets, 'accum_supplus': accum_supplus, 'total_net_assetEq': total_net_assetEq,
            'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialposition.html', args)


@login_required
def financialnotes(request):
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')

    categories = GeneralLedger.objects.exclude(category_id__isnull=True).values('sub_category', 'sub_category__sub_category_name',
                                                                                'sub_category__notes', 'category').annotate(totaldebit=Sum('debit'), totalcredit=Sum('credit')).order_by('sub_category__notes')
    items = GeneralLedger.objects.exclude(category_id__isnull=True).values('account_id', 'account_id__item_name', 'sub_category', 'category').annotate(
        debit=Sum('debit'), credit=Sum('credit')).order_by('account_id__item_name')

    print('THE CATEGORIES ARE: ', categories)
    print('THE ITEMS ARE: ', items)

    args = {'category': categories, 'items': items, 'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialnotes.html', args)


@login_required
def financialcashflow(request):
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')

    # revenues = ChartSubCategory.objects.filter(category_code_id=1)
    # expenses = ChartSubCategory.objects.filter(category_code_id=2)

    revenues = GeneralLedger.objects.filter(category_id=1).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(credit=Sum('credit'))
    expenses = GeneralLedger.objects.filter(category_id=2).values(
        'sub_category', 'sub_category__sub_category_name', 'sub_category__notes').annotate(debit=Sum('debit'))
    total_revenue = GeneralLedger.objects.filter(
        category_id=1).aggregate(Sum('credit'))['credit__sum'] or 0.00
    total_expense = GeneralLedger.objects.filter(
        category_id=2).aggregate(Sum('debit'))['debit__sum'] or 0.00
    total_balance = (total_revenue - total_expense)

    args = {'revenues': revenues, 'expenses': expenses, 'total_revenue': total_revenue,
            'total_expense': total_expense, 'total_balance': total_balance,
            'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialcashflow.html', args)


@login_required
def financialnetasset(request):
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')

    revenues = ChartSubCategory.objects.filter(category_code_id=1)
    expenses = ChartSubCategory.objects.filter(category_code_id=2)

    args = {'revenues': revenues, 'expenses': expenses,
            'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialnetasset.html', args)


@login_required
def financialfixedasset(request):
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')

    revenues = ChartSubCategory.objects.filter(category_code_id=1)
    expenses = ChartSubCategory.objects.filter(category_code_id=2)

    args = {'revenues': revenues, 'expenses': expenses,
            'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialfixedasset.html', args)


# REPORTS (OTHERS)
@login_required
def financialacctchart(request):
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')
    category = ChartCategory.objects.all()
    subcategory = ChartSubCategory.objects.all()
    acctitems = ChartNoteItems.objects.all()

    print('MAIN CATEGORY : ', category)
    print('SUB CATEGORY : ', subcategory)
    print('ACCOUNT ITEMS : ', acctitems)
    print('COMPANY INFO : ', companyinfo)

    args = {'category': category, 'subcategory': subcategory,
            'acctitems': acctitems, 'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialacctchart.html', args)


@login_required
def financialbudget(request):
    companyinfo = CompanyRegistration.objects.filter(
        id=1).values('name', 'address', 'phone')
    budgetdept = BudgetDepartment.objects.all()

    expenses = ExpenseDetails.objects.all().values(
        'Debit_account', 'budget_dept__budget_item__item_name', 'budget_dept__budget_dept__department_code',
        'budget_dept__budget_dept__department_name', 'budget_dept__amount').annotate(
            amount=Sum('amount')).filter(expense_main_id__date__range=["2020-06-01", "2020-06-30"])

    budget = BudgetDetails.objects.all().order_by('budget_item')

    print('BUDGET ITEM NAME', budget)
    # acctitems = ChartNoteItems.objects.all()

    # budget2 = BudgetDetails.objects.raw('''SELECT * from smartsetup_BudgetDetails
    #                INNER JOIN smartsetup_GeneralLedger
    #                ON smartsetup_BudgetDetails.budget_item_id = smartsetup_GeneralLedger.account_id_id
    #                ''')

    # budget_dict = {}
    budget_records = []
    budget_totals = []

    for budgetItem in budget:
        department = budgetItem.budget_dept
        budgetName = budgetItem.budget_item
        budgetAmount = budgetItem.amount
        # print('DEPARTMENT CODE :', departmentCode)
        Jan = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-01-01", "2019-01-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Feb = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-02-01", "2019-02-28"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Mar = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-03-01", "2019-03-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Apr = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-04-01", "2019-04-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        May = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-05-01", "2019-05-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Jun = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-06-01", "2019-06-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Jul = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-07-01", "2019-07-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Aug = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-08-01", "2019-08-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Sep = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-09-01", "2019-09-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Oct = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-10-01", "2019-10-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Nov = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-11-01", "2019-11-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Dec = ExpenseDetails.objects.filter(Debit_account=budgetName, budget_dept__budget_dept=department, expense_main_id__date__range=[
                                            "2019-12-01", "2019-12-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        Total = float(Jan) + float(Feb) + float(Mar) + \
            float(Apr) + float(May) + float(Jun) + \
            float(Jul) + float(Aug) + float(Sep) + \
            float(Oct) + float(Nov) + float(Dec)
        Bal = float(budgetAmount) - float(Total)

        record = {'department': department, 'budgetName': budgetName, 'budgetAmount': budgetAmount,
                  'Jan': Jan, 'Feb': Feb, 'Mar': Mar, 'Apr': Apr, 'May': May, 'Jun': Jun, 'Jul': Jul,
                  'Aug': Aug, 'Sep': Sep, 'Oct': Oct, 'Nov': Nov, 'Dec': Dec, 'Total': Total, 'Bal': Bal
                  }

        Jan = 0.00
        Feb = 0.00
        Apr = 0.00
        Mar = 0.00
        May = 0.00
        Jun = 0.00
        Jul = 0.00
        Aug = 0.00
        Sep = 0.00
        Oct = 0.00
        Nov = 0.00
        Dec = 0.00
        Total = 0.00
        Bal = 0.00

        print('BUDGET ARRAYYY :', record)
        budget_records.append(record)

    for budget in budgetdept:
        department = budget.department_name
        budget_sum = BudgetDetails.objects.filter(
            budget_dept=budget.id).aggregate(Sum('amount'))['amount__sum'] or 0.00
        JanSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-01-01", "2019-01-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        FebSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-02-01", "2019-02-28"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        MarSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-03-01", "2019-03-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        AprSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-04-01", "2019-04-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        MaySum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-05-01", "2019-05-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        JunSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-06-01", "2019-06-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        JulSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-07-01", "2019-07-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        AugSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-08-01", "2019-08-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        SepSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-09-01", "2019-09-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        OctSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-10-01", "2019-10-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        NovSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-11-01", "2019-11-30"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        DecSum = ExpenseDetails.objects.filter(budget_dept__budget_dept__department_name=department, expense_main_id__date__range=[
            "2019-12-01", "2019-12-31"]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        TotalSum = float(JanSum) + float(FebSum) + float(MarSum) + float(AprSum) + float(MaySum) + float(JunSum) + \
            float(JulSum) + float(AugSum) + float(SepSum) + \
            float(OctSum) + float(NovSum) + float(DecSum)
        BalSum = float(budget_sum) - float(TotalSum)

        recordTotal = {'department': department, 'budget_sum': budget_sum, 'JanSum': JanSum, 'FebSum': FebSum,
                       'MarSum': MarSum, 'AprSum': AprSum, 'MaySum': MaySum, 'JunSum': JunSum, 'JulSum': JulSum, 'AugSum': AugSum,
                       'SepSum': SepSum, 'OctSum': OctSum, 'NovSum': NovSum, 'DecSum': DecSum, 'TotalSum': TotalSum, 'BalSum': BalSum
                       }

        Jan = 0.00
        Feb = 0.00
        Apr = 0.00
        Mar = 0.00
        May = 0.00
        Jun = 0.00
        Jul = 0.00
        Aug = 0.00
        Sep = 0.00
        Oct = 0.00
        Nov = 0.00
        Dec = 0.00
        Total = 0.00
        Bal = 0.00

        print('BUDGET SUM ARRAYYY :', recordTotal)
        budget_totals.append(recordTotal)

    # print('BUDGET ARRAYSSS :', budget_records)
    # budget_records['budgetItems'] = budget_records

    print('EXTRACTED BUDGET RECORDS :', expenses)
    print('COMPANY INFO : ', companyinfo)
    print('BUDGET DEPT : ', budgetdept)

    args = {'budgetdept': budgetdept, 'budgetItems': budget_records, 'budgetTotals': budget_totals,
            'companyinfo': companyinfo, 'expenses': expenses}

    # args = {'budgetdept': budgetdept, 'budget': budget, 'budget2': budget2,
    #         'acctitems': acctitems, 'companyinfo': companyinfo}
    return render(request, 'smartsetup/financialbudgetanalysis.html', args)
