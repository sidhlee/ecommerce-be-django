from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import os


@api_view(['GET'])
def get_country_codes(request):
    dirpath = os.path.dirname(os.path.abspath(__file__))
    file = open(os.path.join(dirpath, '../../static/country_codes.json'))
    data = file.read()
    file.close()

    json_data = json.loads(data)
    # set safe to False since we're sending a list
    return JsonResponse(json_data, safe=False)
