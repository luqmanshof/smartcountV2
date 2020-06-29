from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views_ajax
from django.contrib.admin import AdminSite

# admin.site.site_url = 'localhost'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('list_signup', views.list_signup, name='list_signup'),
    path('edit_signup', views.edit_signup, name='edit_signup'),
    path('edit_signup/(<int:pk>)', views.edit_signup_with_pk,
         name='edit_signup_with_pk'),

    # path('admin/',admin.site.urls),

    # path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/change_password_form.html'),name='password_change'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/change_password_success.html'), name='password_change_done'),
    path('password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/change_password_form.html'), name='password'),

    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_page.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_success.html'), name='password_reset_done'),
    path('password_reset_confirm/(<uidb64>[0-9A-Za-z]+)-(<token>.+)', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_sure.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_completed.html'), name='password_reset_complete'),

    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    # COMPANY REGISTRATION
    path('setupcompanyreg/(<int:pk>)',
         views.setupcompanyreg, name='setupcompanyreg'),

    # DEPARTMENT
    path('setupdepartment_list', views.setupdepartment_list,
         name='setupdepartment_list'),
    path('setupdepartment/(<int:pk>)',
         views.setupdepartment, name='setupdepartment'),
    path('setupdepartment/(<int:pk>)/detail',
         views.SetupDepartmentDetail.as_view(), name='setupdepartment_detail'),
    path('setupdepartment/(<int:pk>)/delete',
         views.SetupDepartmentDelete.as_view(), name='setupdepartment_delete'),

    # DIVISION
    path('setupdivision_list', views.setupdivision_list,
         name='setupdivision_list'),
    path('setupdivision/(<int:pk>)',
         views.setupdivision, name='setupdivision'),
    path('setupdivision/(<int:pk>)/detail',
         views.SetupDivisionDetail.as_view(), name='setupdivision_detail'),
    path('setupdivision/(<int:pk>)/delete',
         views.SetupDivisionDelete.as_view(), name='setupdivision_delete'),


    # UNIT
    path('setupunit_list', views.setupunit_list,
         name='setupunit_list'),
    path('setupunit/(<int:pk>)',
         views.setupunit, name='setupunit'),
    path('setupunit/(<int:pk>)/detail',
         views.SetupUnitDetail.as_view(), name='setupunit_detail'),
    path('setupunit/(<int:pk>)/delete',
         views.SetupUnitDelete.as_view(), name='setupunit_delete'),


    # CHART MAIN CATEGORIES
    path('chartcategory_list', views.chartcategory_list, name='chartcategory_list'),
    path('chartcategory/(<int:pk>)', views.chartcategory, name='chartcategory'),
    path('chartcategory/(<int:pk>)/detail',
         views.ChartCategoryDetail.as_view(), name='chartcategory_detail'),
    path('chartcategory/(<int:pk>)/delete',
         views.ChartCategoryDelete.as_view(), name='chartcategory_delete'),

    # CHART SUB-CATEGORY
    path('chartsubcategory_list', views.chartsubcategory_list,
         name='chartsubcategory_list'),
    # path('chartsubcategory',views.chartsubcategory,name='chartsubcategory'),
    path('chartsubcategory/(<int:pk>)',
         views.chartsubcategory, name='chartsubcategory'),
    path('chartsubcategory/(<int:pk>)/detail',
         views.ChartSubCategoryDetail.as_view(), name='chartsubcategory_detail'),
    path('chartsubcategory/(<int:pk>)/delete',
         views.ChartSubCategoryDelete.as_view(), name='chartsubcategory_delete'),
    path('ajax/validate_noteno/', views_ajax.ValidateNoteNo, name='validate_noteno'),


    # CHART NOTE-ITEMS
    path('chartnoteitems_list', views.chartnoteitems_list,
         name='chartnoteitems_list'),
    path('chartnoteitems/(<int:pk>)',
         views.chartnoteitems, name='chartnoteitems'),
    path('chartnoteitems/(<int:pk>)/delete',
         views.ChartNoteItemsDelete.as_view(), name='chartnoteitems_delete'),

    # INVENTORY CATEGORY
    path('setupinventorycategory_list', views.setupinventorycat_list,
         name='setupinventorycategory_list'),
    path('setupinventorycategory/create',
         views.SetupInventoryCat.as_view(), name='setupinventorycat_create'),
    path('setupinventorycategory/(<int:pk>)/update',
         views.SetupInventoryCatUpdate.as_view(), name='setupinventorycat_update'),
    path('setupinventorycategory/(<int:pk>)/detail',
         views.SetupInventoryCatDetail.as_view(), name='setupinventorycat_detail'),
    path('setupinventorycategory/(<int:pk>)/delete',
         views.SetupInventoryCatDelete.as_view(), name='setupinventorycat_delete'),

    path('setupinventoryitems_list', views.setupinventoryitems_list,
         name='setupinventoryitems_list'),
    path('setupinventoryitems/(<int:pk>)',
         views.setupinventoryitems, name='setupinventoryitems'),
    path('setupinventoryitems/(<int:pk>)/detail',
         views.SetupInventoryItemsDetail.as_view(), name='setupinventoryitems_detail'),
    path('setupinventoryitems/(<int:pk>)/delete',
         views.SetupInventoryItemsDelete.as_view(), name='setupinventoryitems_delete'),


    # FIXED ASSETS
    path('setupfixedasset_list', views.setupfixedasset_list,
         name='setupfixedasset_list'),
    path('fixedasset_new', views.FixedAsset.as_view(), name='fixedasset_new'),
    path('fixedasset_edit/(<int:pk>)',
         views.fixedassetedit, name='fixedasset_edit'),
    path('setupfixedasset/(<int:pk>)',
         views.setupfixedasset, name='setupfixedasset'),
    path('ajax/fixedasset/create/',  views.CreateFixedAsset.as_view(),
         name='fixedasset_ajax_create'),
    path('setupfixedasset/(<int:pk>)/detail',
         views.SetupFixedAssetDetail.as_view(), name='setupfixedasset_detail'),
    path('setupfixedasset/(<int:pk>)/delete',
         views.SetupFixedAssetDelete.as_view(), name='setupfixedasset_delete'),


    # SETUP EMPLOYEES
    path('employees_list', views.employees_list, name='employees_list'),
    path('employees/(<int:pk>)', views.employees, name='employees'),
    path('employees/(<int:pk>)/detail',
         views.EmployeesDetail.as_view(), name='employees_detail'),
    path('employees/(<int:pk>)/delete',
         views.EmployeesDelete.as_view(), name='employees_delete'),

    # SETUP CLIENT
    path('setupclients_list', views.setupclients_list, name='setupclients_list'),
    path('setupclients/(<int:pk>)', views.setupclients, name='setupclients'),
    path('setupclients/(<int:pk>)/detail',
         views.SetupClientsDetail.as_view(), name='setupclients_detail'),
    path('setupclients/(<int:pk>)/delete',
         views.SetupClientsDelete.as_view(), name='setupclients_delete'),

    # SETUP VENDORS
    path('setupvendors_list', views.setupvendors_list, name='setupvendors_list'),
    path('setupvendors/(<int:pk>)', views.setupvendors, name='setupvendors'),
    path('setupvendors/(<int:pk>)/detail',
         views.SetupVendorsDetail.as_view(), name='setupvendors_detail'),
    path('setupvendors/(<int:pk>)/delete',
         views.SetupVendorsDelete.as_view(), name='setupvendors_delete'),

    # RECEIPT
    path('receipt_list', views.receipt_list, name='receipt_list'),
    path('receipt_new', views.ReceiptClass.as_view(), name='receipt_new'),
    path('ajax/receipt/create/',  views.CreateReceipt.as_view(),
         name='receipt_ajax_create'),
    path('receipt_edit/(<int:pk>)', views.receiptedit, name='receipt_edit'),
    path('ajax/receipt_items/delete/',  views_ajax.DeleteRececiptItem.as_view(),
         name='receipt_ajax_delete'),
    path('ajax/receipt/delete/',  views_ajax.DeleteRececipt.as_view(),
         name='receipt_delete'),

    path('ajax/getacctID/',  views.GetAcctIDs.as_view(),
         name='ajax_getacctID'),


    # EXPENSES
    path('expense_list', views.expense_list, name='expense_list'),
    path('expense_new', views.ExpenseClass.as_view(), name='expense_new'),
    path('expense_edit/(<int:pk>)', views.expenseedit, name='expense_edit'),
    path('ajax/expense/create/',  views.CreateExpense.as_view(),
         name='expense_ajax_create'),
    path('ajax/expense_items/delete/',  views_ajax.DeleteExpenseItem.as_view(),
         name='expense_ajax_delete'),
    path('ajax/expense/delete/',  views_ajax.DeleteExpense.as_view(),
         name='expense_delete'),

    # BUDGET
    path('budget_list', views.budget_list, name='budget_list'),
    path('budget_new', views.BudgetClass.as_view(), name='budget_new'),
    path('ajax/budget/create/',  views.CreateBudget.as_view(),
         name='budget_ajax_create'),
    path('budget_edit/(<int:pk>)', views.budgetedit, name='budget_edit'),
    path('ajax/budget/delete/',  views_ajax.DeleteBudget.as_view(),
         name='budget_delete'),
    path('ajax/budget_items/delete/',  views_ajax.DeleteBudgetItem.as_view(),
         name='budget_ajax_delete'),
    path('budget_savemain', views.BudgetSaveMain.as_view(),
         name='budget_savemain'),     # SAVE MAIN FORM RECORDS

    # BUDGET DEPARTMENT SETUP
    path('budgetdept_list', views.budgetdept_list,
         name='budgetdept_list'),
    path('budgetdept/(<int:pk>)',
         views.budgetdept, name='budgetdept'),
    path('budgetdept/(<int:pk>)/detail',
         views.BudgetDeptDetail.as_view(), name='budgetdept_detail'),
    path('budgetdept/(<int:pk>)/delete',
         views.BudgetDeptDelete.as_view(), name='budgetdept_delete'),
    path('get_budgetexp',  views_ajax.get_budgetexp,
         name='get_budgetexp'),


    # GENERAL JOURNAL POSTINGS
    path('gjournal_list', views.gjournal_list, name='gjournal_list'),
    path('gjournal_new', views.GJournalClass.as_view(), name='gjournal_new'),
    path('ajax/gjournal/create/',  views.CreateGJournal.as_view(),
         name='gjournal_ajax_create'),
    path('gjournal_edit/(<int:pk>)', views.gjournaledit, name='gjournal_edit'),
    path('gjournal_post', views.gjournal_post, name='gjournal_post'),
    path('gjournal_unpost', views_ajax.UnpostGJournal,
         name='gjournal_ajax_unpost'),
    path('ajax/gjournal_items/delete/',  views_ajax.DeleteGJournalItem.as_view(),
         name='gjournal_ajax_delete'),
    path('ajax/gjournal/delete/',  views_ajax.DeleteGJournal.as_view(),
         name='gjournal_delete'),


    # BEGINNING BALANCE POSTINGS
    path('begbalance_list', views.begbalance_list, name='begbalance_list'),
    path('begbalance_new', views.BegBalanceClass.as_view(), name='begbalance_new'),
    path('ajax/begbalance/create/',  views.CreateBegBalance.as_view(),
         name='begbalance_ajax_create'),
    path('begbalance_edit/(<int:pk>)',
         views.begbalanceedit, name='begbalance_edit'),
    path('ajax/begbalance_items/delete/',  views_ajax.DeleteBegBalanceItem.as_view(),
         name='begbalance_ajax_delete'),
    path('ajax/begbalance/delete/',  views_ajax.DeleteBegBalance.as_view(),
         name='begbalance_delete'),
    path('begbalance_savemain', views.begbalance_savemain,
         name='begbalance_savemain'),
    path('begbalance_post', views.begbalance_post, name='begbalance_post'),


    # PURCHASE POSTINGS
    path('purchase_list', views.purchase_list, name='purchase_list'),
    path('purchase_new', views.PurchaseClass.as_view(), name='purchase_new'),
    path('ajax/purchase/create/',  views.CreatePurchase.as_view(),
         name='purchase_ajax_create'),
    path('purchase_edit/(<int:pk>)', views.purchaseedit, name='purchase_edit'),
    path('purchase_post', views.purchase_post, name='purchase_post'),
    path('ajax/purchase_items/delete/',  views_ajax.DeletePurchaseItem.as_view(),
         name='purchase_ajax_delete'),
    path('ajax/purchase/delete/',  views_ajax.DeletePurchase.as_view(),
         name='purchase_delete'),




    # VIEW JOURNALS
    path('journal_view/(<str:pk>)/(<str:jt>)',
         views.journalview, name='journal_view'),

    # Reports
    path('financialperformance', views.financialperformance,
         name='financialperformance'),
    # path('financialperformanceprint',views.financialperformanceprint,name='financialperformanceprint'),
    path('financialposition', views.financialposition, name='financialposition'),
    path('financialnotes', views.financialnotes, name='financialnotes'),
    path('financialcashflow', views.financialcashflow,
         name='financialcashflow'),
    path('financialnetasset', views.financialnetasset, name='financialnetasset'),
    path('financialfixedasset', views.financialfixedasset,
         name='financialfixedasset'),
    path('financialbudget', views.financialbudget, name='financialbudget'),
    path('note_view/(<str:pk>)', views.noteview, name='note_view'),

    # Reports (OTHERS)
    path('financialacctchart', views.financialacctchart,
         name='financialacctchart'),


    ########### URL Path to Ajax views ######################
    path('note_items', views_ajax.ChartNoteItem.as_view(), name='note_items'),
    #     path('note_items/filter/', views_ajax.chartnote_filter,
    #          name='note_items_filter'),
    path('note_items/create/',  views_ajax.CreateNoteItem.as_view(),
         name='note_ajax_create'),
    path('ajax/note_items/update/',  views_ajax.UpdateNoteItem.as_view(),
         name='note_ajax_update'),
    path('ajax/note_items/delete/',  views_ajax.DeleteNoteItem.as_view(),
         name='note_ajax_delete'),

    path('list_items/filter/', views_ajax.list_filter,
         name='list_items_filter'),

    path('note_items/populate/',  views_ajax.populate_noteitems,
         name='populate_noteitems'),
    path('get_acctcat',  views_ajax.get_acctcat,
         name='get_acctcat'),
    path('purchase_items/populate/',  views_ajax.populate_purchaseitems,
         name='populate_purchaseitems'),
    path('get_date_value',  views_ajax.get_date_value,
         name='get_date_value'),
    path('get_assetaccts',  views_ajax.get_assetaccts,
         name='get_assetaccts'),
]
