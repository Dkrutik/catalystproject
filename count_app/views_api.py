from rest_framework.decorators import api_view
from rest_framework.response import Response
from count_app.models import CompanyDataset
from count_app.utility import filter_fields


@api_view(['POST'])
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(['POST'])
def get_query_count(request):
    json_data = request.data
    filters = {}

    for field in filter_fields:
        value = json_data.get(field)
        if value:
            if field in ['city', 'state']:
                filters[f'locality__{"startswith" if field == "city" else "contains"}'] = value
            elif field in ['keyword']:
                filters[f'name__{"contains"}'] = value
            elif field in ['employee_from', 'employee_to']:
                filters[f'total_employee_estimate__{"gte" if field == "employee_from" else "lte"}'] = int(value)
            else:
                filters[f'{field}_founded' if field == 'year' else field] = value
    # apply filters to the queryset and get the count
    count_result = CompanyDataset.objects.filter(**filters).count()
    json_data["count"] = count_result
    # print("json", json_data)
    return Response(json_data)
