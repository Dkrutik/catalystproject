import csv
import requests
import time
from django.db import transaction
from .models import CompanyDataset

filter_fields = ['keyword', 'year', 'industry', 'city', 'state', 'country', 'employee_from', 'employee_to', 'count']


def handle_uploaded_file(f):
    file_path = "static/csv/my_csv_file.csv"
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks(chunk_size=8192):
            destination.write(chunk)
            chunk_contents = chunk.decode('utf-8')
            # print(chunk_contents)
            for line in chunk_contents.splitlines():
                line_list = line.split(',')
                # print("list:", line_list)
                if len(line_list) == 13:
                    create_dict = {}
                    if line_list[1] == 'name':
                        continue
                    else:
                        try:
                            data_id = CompanyDataset.objects.filter(data_id=line_list[0]).first()
                            if data_id:
                                print("skipped")
                                continue
                            else:
                                print(type(line_list[3]))
                                create_dict['data_id'] = line_list[0] if line_list[0] != "" else None
                                create_dict['name'] = line_list[1] if line_list[1] != "" else None
                                create_dict['domain'] = line_list[2] if line_list[2] != "" else None
                                create_dict['year_founded'] = round(int(line_list[3].replace(".0", ""))) if line_list[3] != "" else 0
                                create_dict['industry'] = line_list[4] if line_list[4] != "" else None
                                create_dict['size_range'] = line_list[5] if line_list[5] != "" else None
                                if line_list[6] != "":
                                    create_dict['locality'] = ','.join([str(line_list[6]), str(line_list[7]), str(line_list[8])])
                                    create_dict['locality'] = create_dict['locality'].replace('"', '')
                                else:
                                    create_dict['locality'] = ""
                                create_dict['country'] = line_list[9] if line_list[0] != "" else None
                                create_dict['linkedin_url'] = line_list[10] if line_list[0] != "" else None
                                create_dict['current_employee_estimate'] = round(int(line_list[11].replace(".0", ""))) if line_list[11] != "" else 0
                                create_dict['total_employee_estimate'] = round(int(line_list[12].replace(".0", ""))) if line_list[12] != "" else 0
                                company_dataset = CompanyDataset(**create_dict)
                                company_dataset.save()
                        except Exception as e:
                            print(f"error at create: {str(e)}")
                            continue
                else:
                    continue
        return file_path


def import_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                domain = CompanyDataset.objects.filter(domain=row['domain']).first()
                if domain:
                    print("skipped")
                else:
                    with transaction.atomic():
                        CompanyDataset.objects.create(
                            name=row['name'] if row['name'] else None,
                            domain=row['domain'] if row['domain'] else None,
                            year_founded=int(row['year founded']) if row['year founded'].isdigit() else None,
                            industry=row['industry'] if row['industry'] else None,
                            size_range=row['size range'] if row['size range'] else None,
                            locality=row['locality'] if row['locality'] else None,
                            country=row['country'] if row['country'] else None,
                            linkedin_url=row['linkedin url'] if row['linkedin url'] else None,
                            current_employee_estimate=int(row['current employee estimate'])
                            if row['current employee estimate'].isdigit() else None,
                            total_employee_estimate=int(row['total employee estimate'])
                            if row['total employee estimate'].isdigit() else None,
                        )
            except Exception as e:
                print(f"Error occurred while creating object: {e}")
                continue


def get_unique_values(companies, field=None):
    if field == "locality":
        city_set, state_set = set(), set()
        for company in companies:
            location = getattr(company, field)
            if len(location.split(', ')) == 3:
                city, state, country = location.split(', ')
                city_set.add(city)
                state_set.add(state)
            elif len(location.split(', ')) == 2:
                city, state = location.split(', ')
                city_set.add(city)
                state_set.add(state)
            else:
                pass
        return city_set, state_set
    elif field in ['current_employee_estimate', 'total_employee_estimate']:
        unique_values = set(getattr(company, field) for company in companies)
        gNo = round(max(unique_values), -5)
        range_list = [n for n in range(0, gNo, 100000)]
        return range_list
    else:
        unique_values = set(getattr(company, field) for company in companies)
        return unique_values


def api_request(api=None, json_data=None):
    try:
        response = requests.post(api, json=json_data)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return {f"error at api_request: {str(e)}"}
