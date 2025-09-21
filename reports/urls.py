from django.urls import path
from .views import ReportGenerateView

urlpatterns = [
    path('', ReportGenerateView.as_view(), name="report_list")

]