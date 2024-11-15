import requests
import json

# TODO:
# * date range as parameter
# * variable page size?
# * check if results don't exceed 10000 results (we can't access more after that => restrict amount via date range)
def get_page(page): 
    page_size=100
    json_data = """{
                    'searchType': ['all'],
                    'searchScope': ['all'],
                    'date_range':['2023-01-01T00:00:00.000Z', '2023-12-31T23:59:00.000Z'],
                    'category': ['Protokolle'] }"""
    headers = { 'Content-Type': 'application/json'}
    
    api = "https://www.parlament.gv.at/Filter/api/filterform/vts/data?page={page}&pagesize={page_size}" \
          .format(page=page, page_size=page_size)
    
    response = requests.post(api, headers=headers, data=json_data).json()

    return response, "{begin} to {end} of {all}".format(begin=(page-1)*page_size, end=page*page_size, all=response['count'])

print(get_page(2)[1])