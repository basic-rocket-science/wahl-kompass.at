from datetime import datetime
import requests
import json

# TODO:
# * check if results don't exceed 10000 results (we can't access more after that => restrict amount via date range)
def _get_page(page=1, page_size=100, date_begin="2000-01-01", date_end="2000-12-31"): 
    json_data = "{ 'searchType': ['all'], \
                   'searchScope': ['all'], \
                   'date_range': [ '" + datetime.strptime(date_begin, "%Y-%m-%d").isoformat() + ".000Z', \
                                   '" + datetime.strptime(date_end, "%Y-%m-%d").isoformat() + ".000Z' ], \
                   'category': ['Protokolle'] }"
    headers = { 'Content-Type': 'application/json' }

    api = "https://www.parlament.gv.at/Filter/api/filterform/vts/data?page={page}&pagesize={page_size}" \
          .format(page=page, page_size=page_size)
    
    response = requests.post(api, headers=headers, data=json_data).json()

    return { 'response': response,
             'answer': "{begin} to {end} of {all} from {date_begin} to {date_end}".format(begin=(page-1)*page_size,
                                                                                          end=page*page_size if page*page_size < response['count'] else response['count'],
                                                                                          all=response['count'],
                                                                                          date_begin=date_begin,
                                                                                          date_end=date_end) }

def get_results(page_size):
    results = { 'count': 0, 'protocols': [] }

    # from 1996 onwards there is enough data
    for year in range(1996, datetime.now().year + 1):
        date_begin = "{year}-01-01".format(year=year)
        date_end = "{year}-12-31".format(year=year)

        # get count of results
        count = int(_get_page(date_begin=date_begin, date_end=date_end)['response']['count'])

        # we can't iterate through more than 10000 results
        if count > 10000:
            print("More than 10000 results in {year}".format(year=year))
            exit()

        results['count'] += count
        for page in range(1, count // page_size + 2):
            response = _get_page(page)['response']

            results['protocols'].append(response['rows'])
        
        print(year, "cumulative results", results['count'])

get_results(10000)