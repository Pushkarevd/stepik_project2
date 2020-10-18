from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Specialty, Vacancy


def custom_handler404(request, exception):
    return HttpResponseNotFound("Страница не найдена!")


def custom_handler500(request):
    return HttpResponseServerError("Server error!")


class MainView(View):

    def get(self, request):
        vacancies = Specialty.objects.annotate(count=Count("vacancies"))
        companies = Company.objects.annotate(count=Count("vacancies"))
        return render(request, "index.html", {"vacancies": vacancies, "companies": companies})


class VacanciesListView(View):

    def get(self, request):
        vacancies = Vacancy.objects.all()
        count_vacancies = Vacancy.objects.count()
        return render(request, "vacancies.html",
                      {"count_vacancies": count_vacancies, "vacancies": vacancies, "title": "Все вакансии"})


class VacanciesSpecializationView(View):

    def get(self, request, vac_specialty):
        try:
            Specialty.objects.get(code=vac_specialty)
        except Specialty.DoesNotExist:
            raise Http404
        vacancies = Vacancy.objects.filter(specialty__code=vac_specialty)
        title = Specialty.objects.get(code=vac_specialty).title
        count_vacancies = vacancies.count()
        return render(request, "vacancies.html",
                      {"count_vacancies": count_vacancies, "vacancies": vacancies, "title": title})


class CompaniesView(View):

    def get(self, request, comp_id):
        try:
            company = Company.objects.get(id=comp_id)
        except Company.DoesNotExist:
            raise Http404
        vacancies = Vacancy.objects.filter(company__id=comp_id)
        count_vacancies = vacancies.count()
        return render(request, "company.html",
                      {"vacancies": vacancies, "count_vacancies": count_vacancies, "company": company})


class VacancyView(View):

    def get(self, request, vac_id):
        try:
            vacancy = Vacancy.objects.get(id=vac_id)
        except Vacancy.DoesNotExist:
            raise Http404
        return render(request, "vacancy.html", {"vacancy": vacancy})
