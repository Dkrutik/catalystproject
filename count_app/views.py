import os

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from count_app.models import CompanyDataset
from count_app.utility import import_csv_file, handle_uploaded_file, get_unique_values, filter_fields, api_request
from django.utils.http import urlencode
import environ
from django.contrib.auth import logout

env = environ.Env()


# Create your views here.
def home(request):

    return redirect(reverse('account_login'))



def profile(request):
    
    return render(request, 'count_app/profile.html')


def upload_data(request):
    if request.method == 'GET':
        data = {'is_file': False}
        return render(request, 'count_app/upload_data.html', data)
    elif request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            file_path = handle_uploaded_file(csv_file)  
            data = {'is_file': True}
        else:
            data = {'is_file': False, 'error': 'No file uploaded.'}
        return render(request, 'count_app/upload_data.html', data)


def query_builder(request):
    if request.method == 'GET':
        context = {}
        for field in filter_fields:
            context[field] = request.GET.get(field)
        companies = CompanyDataset.objects.all()
        if companies:
            unique_industry = get_unique_values(companies, "industry")
            unique_year = get_unique_values(companies, "year_founded")
            unique_country = get_unique_values(companies, "country")
            unique_total_employee = get_unique_values(companies, "total_employee_estimate")
            unique_city, unique_state = get_unique_values(companies, "locality")
            context['unique_industry'] = unique_industry
            context['unique_year'] = unique_year
            context['unique_total_employee'] = unique_total_employee
            context['unique_country'] = unique_country
            context['unique_city'] = unique_city
            context['unique_state'] = unique_state
            return render(request, 'count_app/query_builder.html', context)
        else:
            context = {"message": "No Records In Database"}
            return render(request, 'count_app/query_builder.html', context)

    elif request.method == 'POST':
        context = {}
        json_data = {}
        request_data = request.POST

        for key in filter_fields:
            if key == "count":
                pass
            elif request_data[key] != "":
                json_data[key] = request_data[key]

        response = api_request(api=env('API_ENDPOINT'), json_data=json_data)

        if response:
            redirect_url = reverse('query_builder') + '?' + urlencode(response)
            return redirect(redirect_url)


def list_users(request):
    context = {}
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'count_app/list_users.html', context)


def custom_logout(request):
    logout(request)
    return render(request, 'account/logged.html')