from django.contrib import admin
from django.urls import path

from vacancies.views import MainView, CompaniesView, VacanciesListView, VacancyView, VacanciesSpecializationView, \
    custom_handler500, custom_handler404

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('vacancies', VacanciesListView.as_view()),
    path('vacancies/cat/<str:vac_specialty>', VacanciesSpecializationView.as_view()),
    path('companies/<int:comp_id>', CompaniesView.as_view()),
    path('vacancies/<int:vac_id>', VacancyView.as_view()),
]
