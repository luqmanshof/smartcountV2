from django.db import models
from django.contrib.auth.models import User
# from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# SETUP MODELS


class CompanyRegistration(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    website = models.CharField(max_length=100, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_description = models.CharField(blank=True, max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='', blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    image = models.ImageField(upload_to='images/profilepix/', blank=True)
    signature = models.ImageField(upload_to='images/signature/', blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class SetupDepartment(models.Model):
    department_name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.department_name


class SetupDivision(models.Model):
    division_name = models.CharField(max_length=256, verbose_name='section')
    department = models.ForeignKey(
        SetupDepartment, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.division_name


class SetupUnit(models.Model):
    unit_name = models.CharField(max_length=256)
    division = models.ForeignKey(
        SetupDivision, on_delete=models.SET_NULL, null=True, verbose_name='section')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.unit_name


TITLE = (
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Ms', 'Ms'),
    ('Dr', 'Dr'),
    ('Engr', 'Engr'),
    ('Prof', 'Prof'),
    ('Chief', 'Chief'),
    ('Sir', 'Sir'),
    ('Pr', 'Pr'),
    ('Imam', 'Imam'),
    ('Elder', 'Elder'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

M_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
)


class EmployeeProfile(models.Model):
    employee_number = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=50, choices=TITLE, default='Mr')
    first_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    nick_name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=50, choices=GENDER, default='Male')
    birthdate = models.DateTimeField()
    marital_status = models.CharField(
        max_length=50, choices=M_STATUS, default='Single')
    address = models.TextField()
    phone = models.CharField(max_length=100, default='')
    login_profile = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, default='')
    email = models.CharField(max_length=200, default='', blank=True)
    hire_date = models.DateTimeField()
    department = models.ForeignKey(
        SetupDepartment, on_delete=models.SET_NULL, blank=True, null=True, default='')
    division = models.ForeignKey(
        SetupDivision, on_delete=models.SET_NULL, blank=True, null=True, default='')
    unit = models.ForeignKey(
        SetupUnit, on_delete=models.SET_NULL, blank=True, null=True, default='')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class ChartCategory(models.Model):
    category_code = models.PositiveSmallIntegerField()
    category_name = models.CharField(max_length=256)

    def __str__(self):
        return self.category_name


class ChartSubCategory(models.Model):
    category_code = models.ForeignKey(ChartCategory, on_delete=models.CASCADE)
    sub_category_code = models.PositiveIntegerField()
    sub_category_name = models.CharField(max_length=256)
    notes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sub_category_name"]

    def __str__(self):
        return self.sub_category_name


class ChartNoteItems(models.Model):
    # sub_category = models.CharField(max_length=256)
    sub_category = models.ForeignKey(
        ChartSubCategory, on_delete=models.CASCADE, default='', related_name='noteitems')
    item_name = models.CharField(max_length=256)

    class Meta:
        ordering = ["item_name"]

    def __str__(self):
        return self.item_name


DURATION = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)


class SetupBegBalanceMain(models.Model):
    entrydate = models.DateTimeField()
    duration = models.CharField(max_length=50, choices=DURATION, default='12')
    periodno = models.PositiveIntegerField(default=0)
    periodstart = models.DateTimeField()
    periodend = models.DateTimeField()
    year = models.CharField(max_length=100)


class SetupBegbalanceDetails(models.Model):
    mainid = models.ForeignKey(SetupBegBalanceMain, on_delete=models.CASCADE)
    date = models.DateTimeField()
    account_id = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        ChartCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256, default='')
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)


class SetupClients(models.Model):
    client_name = models.CharField(max_length=256)
    address = models.TextField()
    city = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    phone = models.CharField(max_length=100, default='')
    account_officer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.client_name


VENDOR_TYPES = (
    ('Agency', 'Agency'),
    ('Supplier', 'Supplier'),
    ('contractor', 'contractor'),
)


class SetupVendors(models.Model):
    vendor_name = models.CharField(max_length=256)
    vendor_type = models.CharField(
        max_length=200, choices=VENDOR_TYPES, default='Supplier')
    address = models.TextField()
    city = models.CharField(max_length=200, default='', blank=True, null=True)
    website = models.URLField(default='', blank=True, null=True)
    phone = models.CharField(max_length=100, default='')
    tin_number = models.CharField(
        max_length=200, default='', blank=True, null=True)
    payer_id = models.CharField(
        max_length=200, default='', blank=True, null=True)

    def __str__(self):
        return self.vendor_name


DEPR_METHODS = (
    ('Straight-line', 'Straight-line'),
    ('Double declining balance', 'Double declining balance'),
    ('Sum of years', 'Sum of years'),
    ('Units of production', 'Units of production'),
)


class SetupFixedAssets(models.Model):
    asset_id = models.CharField(max_length=256)
    serial_no = models.CharField(max_length=256, null=True)
    description = models.CharField(max_length=256)
    acquisition_date = models.DateTimeField(
        default=timezone.now, blank=True)
    department = models.ForeignKey(
        SetupDepartment, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    purchase_value = models.FloatField(default=0)
    useful_life = models.CharField(max_length=256, null=True)
    salvage_value = models.FloatField(default=0)
    asset_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True, related_name='asset_account')
    expense_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True, related_name='expense_account')
    accumulated_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True, related_name='accumulated_account')
    depreciation_method = models.CharField(
        max_length=50, choices=DEPR_METHODS, default='Straight-line')
    status = models.BooleanField(default=False)
    others = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.description


class SetupInventoryCategory(models.Model):
    inventory_category_code = models.PositiveSmallIntegerField(blank=True)
    inventory_category_name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.inventory_category_name


class SetupInventoryItems(models.Model):
    inventory_code = models.CharField(max_length=256, default='', blank=True)
    inventory_name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    inventory_category_code = models.ForeignKey(
        SetupInventoryCategory, on_delete=models.CASCADE, verbose_name='Inventory Category')

    def __str__(self):
        return self.inventory_name


class InventoryJournal(models.Model):
    date = models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Date/Time')
    ref_number = models.PositiveIntegerField(default=100)
    inventory_code = models.CharField(max_length=256)
    inventory_name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    store = models.CharField(max_length=256, default='', blank=True)


# ACCOUNT MODELS


class GeneralLedger(models.Model):
    date = models.DateTimeField()
    ref_number = models.PositiveIntegerField(default='')
    journal_type = models.CharField(max_length=256, default='', blank=True)
    account_id = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        ChartCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256, default='')
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    main_Trans = models.BooleanField(default=0)

    class Meta:
        ordering = ["-credit"]


PAYMENT_MODES = (
    ('cash', 'Cash'),
    ('cheque', 'Cheque'),
    ('transfer', 'Transfer'),
    ('draft', 'Draft'),
)


class ReceiptMain(models.Model):
    date = models.DateTimeField(verbose_name='Receipt Date/Time')
    receipt_number = models.PositiveIntegerField(default=100)
    client = models.ForeignKey(SetupClients, on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name='Client Name')
    bill_to = models.CharField(
        max_length=256, default='', blank=True, verbose_name='Received from')
    description = models.TextField(default='')
    cash_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Cash Account')
    Debit_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    pay_mode = models.CharField(
        max_length=50, choices=PAYMENT_MODES, default='Cheque')
    total_amount = models.FloatField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.receipt_number


class ReceiptDetails(models.Model):
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=256, default='')
    revenue_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Revenue Account')
    credit_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    unit_price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    receipt_main_id = models.ForeignKey(
        ReceiptMain, on_delete=models.CASCADE, default=0)


class BudgetDepartment(models.Model):
    department_code = models.CharField(max_length=256, default='')
    department_name = models.CharField(max_length=256, default='')
    description = models.TextField(max_length=256, default='')

    def __str__(self):
        return self.department_name


class BudgetMain(models.Model):
    period_start = models.DateTimeField(default=timezone.now, blank=True)
    period_end = models.DateTimeField(default=timezone.now, blank=True)
    description = models.CharField(max_length=256, default='')
    budget_no = models.IntegerField(default=0)


BUDGET_TYPES = (
    ('Revenue', 'Revenue'),
    ('Expense', 'Expense'),
)


class BudgetDetails(models.Model):
    budget_dept = models.ForeignKey(
        BudgetDepartment, on_delete=models.SET_NULL, null=True)
    budget_item = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    budget_cat = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256, default='')
    budget_type = models.CharField(
        max_length=256, choices=BUDGET_TYPES, default='')
    amount = models.FloatField(default=0)
    budget_main_id = models.ForeignKey(
        BudgetMain, on_delete=models.CASCADE, default=0)


# Expense Models

class ExpenseMain(models.Model):
    date = models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Expense Date/Time')
    voucher_number = models.PositiveIntegerField(default=100)
    payee = models.ForeignKey(
        EmployeeProfile, on_delete=models.SET_NULL, null=True, blank=True, default='')
    description = models.TextField(default='')
    cash_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Cash Account')
    credit_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    pay_mode = models.CharField(
        max_length=50, choices=PAYMENT_MODES, default='Cheque')
    total_amount = models.FloatField(default=0)

    # class Meta:
    #     get_latest_by = 'receipt_number'

    def __str__(self):
        return self.voucher_number


class ExpenseDetails(models.Model):
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=256, default='')
    expense_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Expense Category')
    Debit_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    unit_price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    expense_main_id = models.ForeignKey(
        ExpenseMain, on_delete=models.CASCADE, default=0)
    budget_dept = models.ForeignKey(
        BudgetDetails, on_delete=models.SET_NULL, null=True)


class GJournalMain(models.Model):
    date = models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Date/Time')
    ref_number = models.PositiveIntegerField(default=100)
    description = models.CharField(max_length=256, default='')
    total_debit = models.FloatField(default=0)
    total_credit = models.FloatField(default=0)

    def __str__(self):
        return self.ref_number


class GJournalDetails(models.Model):
    sub_category = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256, default='')
    debit = models.FloatField(default=0, blank=True, null=True)
    credit = models.FloatField(default=0, blank=True, null=True)
    journal_main_id = models.ForeignKey(
        GJournalMain, on_delete=models.CASCADE, default=0)


class PurchaseMain(models.Model):
    date = models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Expense Date/Time')
    voucher_number = models.PositiveIntegerField(default=100)
    vendor = models.ForeignKey(
        SetupVendors, on_delete=models.SET_NULL, null=True, blank=True, default='')
    description = models.TextField(default='')
    cash_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Cash Account')
    credit_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    pay_mode = models.CharField(
        max_length=50, choices=PAYMENT_MODES, default='Cheque')
    total_amount = models.FloatField(default=0)

    def __str__(self):
        return self.voucher_number


class PurchaseDetails(models.Model):
    inventory_item = models.ForeignKey(
        SetupInventoryItems, on_delete=models.SET_NULL, null=True)
    asset_item = models.ForeignKey(
        SetupFixedAssets, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256, default='')
    quantity = models.IntegerField(default=1)
    expense_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Expense Category')
    Debit_account = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    unit_price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    expense_main_id = models.ForeignKey(
        PurchaseMain, on_delete=models.CASCADE, default=0)
    asset = models.BooleanField(default=False)
