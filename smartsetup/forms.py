from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from smartsetup.models import (
    UserProfile, ChartCategory, ChartSubCategory, ChartNoteItems, SetupInventoryItems,
    SetupClients, SetupVendors, ReceiptMain, ReceiptDetails, ExpenseMain,
    ExpenseDetails, GJournalMain, GJournalDetails
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .widgets import BootstrapDateTimePickerInput


class UserProfileForm(forms.ModelForm):
    # image = forms.ImageField(required=False)
    # signature = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = (
            'job_description',
            'city',
            'website',
            'phone',
            'image',
            'signature',
        )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=256, help_text='Required. Inform a valid email address.')
    # description = forms.Textarea(queryset=UserProfile.objects.select_related())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2',)


class EditProfileForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password\">this form</a>."))

    class Meta:
        model = User
        # exclude = () this can be used to specify fields to exclude'
        fields = ('email', 'first_name', 'last_name',)


class ChartCategoryForm(forms.ModelForm):
    class Meta:
        model = ChartCategory
        fields = ('category_code', 'category_name')


class ChartSubCategoryForm(forms.ModelForm):
    notes = forms.ChoiceField(choices=[(x, x) for x in range(1, 50)])

    class Meta:
        model = ChartSubCategory
        fields = ('category_code', 'sub_category_code',
                  'sub_category_name', 'notes')


class ChartNoteItemsForm(forms.ModelForm):
    class Meta:
        model = ChartNoteItems
        fields = ('sub_category', 'item_name')


class SetupInventoryItemsForm(forms.ModelForm):
    class Meta:
        model = SetupInventoryItems
        fields = ('inventory_category_code', 'inventory_code',
                  'inventory_name', 'description')


class SetupClientsForm(forms.ModelForm):
    class Meta:
        model = SetupClients
        fields = ('client_name', 'address', 'city',
                  'website', 'phone', 'account_officer')


class SetupVendorsForm(forms.ModelForm):
    class Meta:
        model = SetupVendors
        fields = ('vendor_name', 'address', 'city', 'website', 'phone')


class ReceiptMainForm(forms.ModelForm):

    class Meta:
        model = ReceiptMain
        fields = (
            'date', 'receipt_number', 'client', 'bill_to',
            'cash_account', 'Debit_account', 'pay_mode', 'total_amount'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cash_account'].queryset = ChartSubCategory.objects.filter(
            category_code_id='3')
        self.fields['date'].widget.attrs.update(
            {'id': 'date-picker', 'class': 'form-control pull-right'})


class ReceiptDetailsForm(forms.ModelForm):

    class Meta:
        model = ReceiptDetails
        fields = (
            'quantity', 'description', 'revenue_account', 'credit_account', 'unit_price',
            'amount', 'receipt_main_id'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['revenue_account'].queryset = ChartSubCategory.objects.filter(
            category_code_id='1')


class ExpenseMainForm(forms.ModelForm):

    class Meta:
        model = ExpenseMain
        fields = (
            'date', 'voucher_number', 'payee',
            'cash_account', 'pay_mode', 'total_amount'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cash_account'].queryset = ChartSubCategory.objects.filter(
            category_code_id='3')
        self.fields['date'].widget.attrs.update(
            {'id': 'date-picker', 'class': 'form-control pull-right'})


class ExpenseDetailsForm(forms.ModelForm):

    class Meta:
        model = ExpenseDetails
        fields = (
            'quantity', 'description', 'expense_account', 'unit_price',
            'amount', 'expense_main_id'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_account'].queryset = ChartSubCategory.objects.filter(
            category_code_id='2')


class GJournalMainForm(forms.ModelForm):

    class Meta:
        model = GJournalMain
        fields = (
            'date', 'ref_number', 'description', 'total_debit', 'total_credit'
        )


class GJournalDetailsForm(forms.ModelForm):
    class Meta:
        model = GJournalDetails
        fields = (
            'description', 'account', 'debit', 'credit', 'journal_main_id'
        )
