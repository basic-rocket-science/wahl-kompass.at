from datetime import datetime
import requests
import json
import os.path
import pickle

base_url = "https://www.parlament.gv.at"

def _get_page(page=1, page_size=100, date_begin="2000-01-01", date_end="2000-12-31"):
    json_data = "{ 'searchType': ['all'], \
                   'searchScope': ['all'], \
                   'date_range': [ '" + datetime.strptime(date_begin, "%Y-%m-%d").isoformat() + ".000Z', \
                                   '" + datetime.strptime(date_end, "%Y-%m-%d").isoformat() + ".000Z' ], \
                   'category': ['Protokolle'] }"
    headers = { 'Content-Type': 'application/json' }

    # more than 100 for pagesize is not possible as not more data is returned
    api = base_url + "/Filter/api/filterform/vts/data?page={page}&pagesize={page_size}" \
          .format(page=page, page_size=page_size)
    
    response = requests.post(api, headers=headers, data=json_data).json()

    return { 'response': response,
             'answer': "{begin} to {end} of {all} from {date_begin} to {date_end}".format(begin=(page-1)*page_size,
                                                                                          end=page*page_size if page*page_size < response['count'] else response['count'],
                                                                                          all=response['count'],
                                                                                          date_begin=date_begin,
                                                                                          date_end=date_end) }

def get_results():
    page_size=100
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
            response = _get_page(page, page_size, date_begin, date_end)['response']

            results['protocols'].extend(response['rows'])
        
        # show progress
        print(year, "cumulative results", results['count'])
    return results

def download_results():
    results = None
    results_file = "results.pickle"

    # load pickle file if catalog is already downloaded
    if os.path.isfile(results_file):
        results = pickle.load(open(results_file, 'rb'))
    else:
        results = get_results()
        pickle.dump(results, open(results_file, 'wb'))

    print(results['count'], "protocols found on parlament.gv.at")

    # loop through results with counter
    for i, result in zip(range(results['count']), results['protocols']):
        # show progress
        if i % 1000 == 0: print(i, "of", results['count'], "protocols downloaded")

        link = result['link']

        # get folder and file names
        dir_name = '/'.join(link.replace('SEITE_', '')[1:].split('/')[0:-1]) + '/'
        file_name = link.replace('SEITE_', '').split('/')[-1]

        # create dir recursively
        if not os.path.exists(dir_name): os.makedirs(dir_name, exist_ok=True)

        # check if file already exists
        if os.path.isfile(dir_name+file_name): continue

        # download file or show exception but continue
        try:
            response = requests.get(base_url + link)

            with open(dir_name+file_name, 'w') as fd:
                fd.write(response.text)
        except Exception as ex:
            print(ex)
            print(file_name + " not downloaded")
        

download_results()