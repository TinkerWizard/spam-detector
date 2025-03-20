from django.urls import path
from .views import SearchView, SearchDetailedView, PersonalContactView, SpamReportView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),  
    path("search/<int:pk>/", SearchDetailedView.as_view(), name="search_detail"),
    path('personal-contacts/', PersonalContactView.as_view(), name="personal_contacts"),  
    path('report-spam/', SpamReportView.as_view(), name='report_spam'),  
]
