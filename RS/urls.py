from django.urls import path
from RS import views

urlpatterns =[

    path('main/', views.main),
    path('RepairmentApply', views.RepairmentApply),
    path('RepairmentCheck', views.RepairmentCheck),
    path('RepairModify/<int:id>', views.RepairModify),
    path('RepairDelete/<int:id>', views.ReportDelete),

    path('ReportApply', views.ReportApply),
    path('ReportCheck', views.ReportCheck),
    path('ReportModify/<int:id>', views.RepairModify),
    path('ReportDelete/<int:id>', views.ReportDelete),

]