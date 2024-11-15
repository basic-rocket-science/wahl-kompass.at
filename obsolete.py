#from ckanapi import RemoteCKAN
#from ckanapi import RemoteCKAN
#from bs4 import BeautifulSoup
#import re

## ID for all Gatherings at data.gv.at API
#plenarsitzungen_id = "285022f8-59c5-4462-9417-c35f350a52d4"
#
## Create a custom session with `allow_redirects=True`
#session = requests.Session()
#session.allow_redirects = True
#
## Connect to the data.gv.at CKAN API
#ckan = RemoteCKAN("https://www.data.gv.at/katalog/", session=session)
#
#plenarsitzungen = ckan.action.package_show(id=plenarsitzungen_id)
#
#resource_url = plenarsitzungen['resources'][0]['url']
#
##bundesrat_id = [item['id'] for item in plenarsitzungen['tags'] if item['display_name'] == "Bundesrat"][0]
###nationalrat_id = [item['id'] for item in plenarsitzungen['tags'] if item['display_name'] == "Nationalrat"][0]
##parlament_id = [item['id'] for item in plenarsitzungen['tags'] if item['display_name'] == "Parlament"][0]
##plenarsitzungen_id = [item['id'] for item in plenarsitzungen['tags'] if item['display_name'] == "Plenarsitzungen"][0]
#
##ckan = RemoteCKAN("https://www.parlament.gv.at/katalog/", session=session)
#
##bundesrat_sitzungen = ckan.action.package_show(id=plenarsitzungen_id)
##print(bundesrat_sitzungen)
#print(resource_url)


### DATA FROM parlament.gv.at
#base_url = "https://www.parlament.gv.at"
#resource_url = base_url + "/recherchieren/plenarsitzungen/index.html"
#
#response = requests.get(resource_url)
#soup = BeautifulSoup(response.text, 'html.parser')
#document_links = soup.find_all("a", href=re.compile("index.html"))
#
#for link in document_links:
#    print(base_url + link['href'])