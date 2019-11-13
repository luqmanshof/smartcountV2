from django.db import models
from django.contrib.auth.models import User
# from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# SETUP MODELS


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_description = models.CharField(blank=True, max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='images/profilepix/', blank=True)
    signature = models.ImageField(upload_to='images/signature/', blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


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

    def __str__(self):
        return self.sub_category_name


class ChartNoteItems(models.Model):
    # sub_category = models.CharField(max_length=256)
    sub_category = models.ForeignKey(
        ChartSubCategory, on_delete=models.CASCADE, default='', related_name='noteitems')
    item_name = models.CharField(max_length=256)

    def __str__(self):
        return self.item_name


class SetupClients(models.Model):
    client_name = models.CharField(max_length=256)
    address = models.TextField()
    city = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    phone = models.CharField(max_length=100, default='')
    account_officer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, default='')

    def __str__(self):
        return self.client_name


class SetupVendors(models.Model):
    vendor_name = models.CharField(max_length=256)
    address = models.TextField()
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.vendor_name


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

# ACCOUNT MODELS


class GeneralLedger(models.Model):
    date = models.DateTimeField()
    ref_number = models.PositiveIntegerField(default='')
    journal_type = models.CharField(max_length=256, default='', blank=True)
    account_id = models.ForeignKey(
        ChartNoteItems, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256, default='')
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)


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

# Expense Models


class ExpenseMain(models.Model):
    date = models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Expense Date/Time')
    voucher_number = models.PositiveIntegerField(default=100)
    payee = models.CharField(max_length=256, default='',
                             blank=True, verbose_name='Payee')
    description = models.TextField(default='')
    cash_account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Cash Account')
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
        ChartSubCategory, on_delete=models.SET_NULL, null=True, verbose_name='Revenue Account')
    unit_price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    expense_main_id = models.ForeignKey(
        ExpenseMain, on_delete=models.CASCADE, default=0)


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
    description = models.CharField(max_length=256, default='')
    account = models.ForeignKey(
        ChartSubCategory, on_delete=models.SET_NULL, null=True)
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    journal_main_id = models.ForeignKey(
        GJournalMain, on_delete=models.CASCADE, default=0)
