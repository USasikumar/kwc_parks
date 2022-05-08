import requests
from bs4 import BeautifulSoup
import json
import base64
import re
import datetime
import urllib
import urllib.request
import mimetypes, urllib
# from urllib.request import urlopen
# from lxml import etree
import lxml.html
import unidecode
import sys

# data format
park = {
    "city": "kitchener",
    "name": "xxx",
    "address": "xxx",
    "hours": "xxx",
    "map": "yyy",
    "picture": [""],
    "amenities": [""],
    "description":"",
    "type":""
}

DATA = []
PAGE = 1

def cambridge_process_page(page) :

    url = f'https://facilities.cambridge.ca/?CategoryIds=&FacilityTypeIds=77%2C75%2C38%2C44&Keywords=&ScrollTo=facilityResultsContainer&CloseMap=true&Page={page}'

    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    rows = soup.select('.result-body > .row .row a.detail-trigger')

    for row in rows:

        park = {
            "city": CITY,
            "picture": [],
            "amenities": [],
            "description":"",
        }



        name = row.get_text().strip()


        try :

         if 'read more' in name:
             continue

         # if 'sport' in name.lower() :
         #    park['type'] = 'Sport Park'
         if 'trail' in name.lower() :
            park['type'] = 'Trail'
         # elif 'garden' in name.lower() :
         #    park['type'] = 'Garden'
         # elif 'dog' in name.lower() :
         #    park['type'] = 'Dog Park'
         else :
            park['type'] = 'Park'


         print(f'Getting {park["type"]} -> {name}')
    
          # Getting image
         try :
             element = row.parent.parent.parent.parent.find_previous_sibling('div')
             img = element.select('img')[0]
             park['picture'].append(img.attrs['src'])
             print(f'Got image ! {park["picture"]}')
         except:
             print('No image for this park')

         park['name'] = name.strip()
         code= row.attrs['data-value']

         link = f'https://facilities.cambridge.ca/Home/Detail?CategoryIds=&FacilityTypeIds=77%2C75%2C38%2C44&Keywords=&ScrollTo=facilityResultsContainer&CloseMap=true&Page={page}&Id={code}'

         response = requests.get(link)

         if (response.status_code == 200) :

           inner_soup = BeautifulSoup(response.content,'html.parser')

           gmap = inner_soup.select('#google-map-container ~ script')
           park['map'] = base64.b64encode(gmap[0].encode_contents()).decode()

           # tree = lxml.html.fromstring(response.content)
           # amenities = tree.xpath("//h2[contains(text(),'Amenities')]/following-sibling::p[1]/following-sibling::ul[1]/li")


           irows = inner_soup.select('#facilityModule > .bootstrap > div > .container-box:first-child > .row > .facility-detail > .row')
           for irow in irows :
            try:
              keyel = irow.select('strong')
              key = keyel[0].get_text().lower().replace(':','').strip()
              valel = irow.select('.col-md-9')
              val = valel[0].get_text().lower().replace(':','').strip()
              park[key] = val
              # print(f'INFO -> {key} : {val}')
            except:
              # print('item not found')
              pass

           irows = inner_soup.select('#facilityModule > .bootstrap > div > .container-box:first-child > .row > .facility-detail > .desktop-display > .row')

           park['amenities'] = []
           for idx,irow in enumerate(irows) :
            try:

              keyel = irow.select('strong')
              key = keyel[0].get_text().lower().replace(':','').strip()

              valel = irows[idx+1].select('.col-md-4')
              if key == 'features' :
                key = 'amenities'
              
              for vl in valel:
                val = vl.get_text().lower().replace(':','').strip()
                park[key].append(val)

                # print(f'INFO -> {key} : {val}')

            except:
              # print('item not found')
              pass

           print('done !')

         # print(park)
         DATA.append(park)

        except Exception as err:
            print(f'Error getting this park info ...',err)


def kitchener_process_page(page) :

    url = f'https://facilities.kitchener.ca/?CategoryIds=&FacilityTypeIds=40972%2C40984%2C40967%2C40970%2C40973%2C40977%2C40964%2C40938%2C40979&Keywords=&ScrollTo=facilityResultsContainer&CloseMap=true&Page={page}'

    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    rows = soup.select('.result-body > .row .row a')

    for row in rows:

        park = {
                "city": CITY,
                "picture": [],
                "amenities": [],
                "description":"",
        }


        try :

         name = row.get_text()

         # if 'sport' in name.lower() :
         #    park['type'] = 'Sport Park'
         if 'trail' in name.lower() :
            park['type'] = 'Trail'
         # elif 'garden' in name.lower() :
         #    park['type'] = 'Garden'
         # elif 'dog' in name.lower() :
         #    park['type'] = 'Dog Park'
         else :
            park['type'] = 'Park'

         # if 'sport' in name.lower() :
         #    park['type'] = 'Sport Park'
         # elif 'trail' in name.lower() :
         #    park['type'] = 'Trail'
         # elif 'garden' in name.lower() :
         #    park['type'] = 'Garden'
         # elif 'dog' in name.lower() :
         #    park['type'] = 'Dog Park'
         # else :
         #    park['type'] = 'Park'

         print(f'Getting {park["type"]} -> {name}')

         try :
             element = row.parent.parent.parent.parent.parent.find_next_sibling('div')
             img = element.select('img')[0]
             park['picture'].append(img.attrs['src'])
             print(f'Got image !!! {park["picture"]}')
         except:
             print('No image for this park')

         park['name'] = name.strip()

         # href = row.attrs['href']
         code= row.attrs['data-value']

         link = f'https://facilities.kitchener.ca/Home/Detail?CategoryIds=&FacilityTypeIds=40972%2C40984%2C40967%2C40970%2C40973%2C40977%2C40964%2C40938%2C40979&Keywords=&ScrollTo=facilityResultsContainer&CloseMap=true&Page={page}&Id={code}'

         response = requests.get(link)

         if (response.status_code == 200) :

           inner_soup = BeautifulSoup(response.content,'html.parser')

           gmap = inner_soup.select('#google-map-container ~ script')
           park['map'] = base64.b64encode(gmap[0].encode_contents()).decode()

           irows = inner_soup.select('#facilityModule > .bootstrap:first-child .container-box > .row > .facility-detail > .row')
           for irow in irows :
              keyel = irow.select('strong')
              key = keyel[0].get_text().lower().replace(':','').strip()
              valel = irow.select('.col-md-9')
              val = valel[0].get_text().lower().replace(':','').strip()
              park[key] = val
              # print(f'INFO -> {key} : {val}')

           irows = inner_soup.select('#facilityModule > .bootstrap:first-child .container-box > .row > .facility-detail > .desktop-display ')
           for irow in irows :
              keyel = irow.select('strong')
              key = keyel[0].get_text().lower().replace(':','').strip()
              valel = irow.select('.col-md-4')
              val = valel[0].get_text().lower().replace(':','').strip()
              park[key] = [val]
              # print(f'INFO -> {key} : {val}')

           print('done !')

         DATA.append(park)

        except Exception as err:
            print(f'Error getting this park info ...',err)
         


def waterloo_process_page():

    url = 'https://www.waterloo.ca/en/things-to-do/parks-directory.aspx#Parks-with-amenities'

    response = requests.get(url)

    if (response.status_code == 200) :

      soup = BeautifulSoup(response.content,'html.parser')

      items = soup.select('.icrtAccordion ul>li')
      for item in items:

        park = {
                "city": CITY,
                "picture": [],
                "amenities": [],
                "description":"",
        }
        name = item.get_text()

        try :

         # if 'sport' in name.lower() :
         #    park['type'] = 'Sport Park'
         if 'trail' in name.lower() :
            park['type'] = 'Trail'
         # elif 'garden' in name.lower() :
         #    park['type'] = 'Garden'
         # elif 'dog' in name.lower() :
         #    park['type'] = 'Dog Park'
         else :
            park['type'] = 'Park'

         # if 'sport' in name.lower() :
         #    park['type'] = 'Sport Park'
         # elif 'trail' in name.lower() :
         #    park['type'] = 'Trail'
         # elif 'garden' in name.lower() :
         #    park['type'] = 'Garden'
         # elif 'dog' in name.lower() :
         #    park['type'] = 'Dog Park'
         # else :
         #    park['type'] = 'Park'

         parts = []
         pattern =r"([A-Za-z0-9\'\_\-\s\.]+),?\(?\s*([A-Za-z0-9\'\_\-\s\.]+)\s*\(([A-Za-z0-9\'\_\-\s,\.\/]+)\)"
         # pattern= r"(.*)\s+(.*)"

         try :
            parts = re.findall(pattern,name)[0]


            park['name'] = parts[0].strip()
            print(f'Getting {park["type"]} -> {name}')

            park['address'] = parts[1].strip()

            all_amenities = []
            try:
                park['description'] = parts[2]
                amenities = parts[2].split(',')

                all_amenities = [[y.split('with') for y in x.split('and')] for x in amenities]
                all_amenities = [item for sublist in all_amenities for item in sublist]
                all_amenities = [item.strip() for sublist in all_amenities for item in sublist if item.strip()!='']
            except:
               pass

            park['amenities'] = all_amenities


         except Exception as e :
            print('Erro -> ',e,name)
             # Special parks ... access their pages
            # try access park page
            parkname =name.lower().replace(' ','-')

            print(f'Trying through own park page ->  {parkname}.aspx')
            url = f'https://www.waterloo.ca/en/things-to-do/{parkname}.aspx'

            response = requests.get(url)

            if (response.status_code == 200) :

              park['name'] = name.strip()
              print('Got Park info')
              soup = BeautifulSoup(response.content,'html.parser')

              desc = soup.select('.IntroParagraph')

              desc_text = ''
              for d in desc :
                if not '(PDF)' in d.get_text() :
                    desc_text = desc_text + '\n' + d.get_text()
              
              all_amenities =[]

              # if 'rim' in name.lower():
              #     print(response.content)

              amenities = soup.select('table tr td h3')
              for am in amenities :
                all_amenities.append(am.get_text())

              # others
              if not len(all_amenities) :

               # try other way 
               tree = lxml.html.fromstring(response.content)
               amenities = tree.xpath("//h2[contains(text(),'Amenities')]/following-sibling::p[1]/following-sibling::ul[1]/li")

               for am in amenities :
                 all_amenities.append(am.text)

               if not len(all_amenities) :
                   amenities = tree.xpath("//p[contains(text(),'General amenities')]/following-sibling::ul[1]/li")

                   for am in amenities :
                     all_amenities.append(am.text)

               # try address
              try:

               all_as = soup.select('a')

               for aitem in all_as :

                href = aitem.attrs['href']

                if 'https://goo.gl/maps' in href :

                 gmap_link = href
                 park['map'] = gmap_link
                 park['address'] = aitem.get_text()
                 break

              except :
                pass

             # waterloo park is different 
              try:

               all_as = soup.select('li > a')

               for aitem in all_as :

                href = aitem.attrs['href']

                if 'https://goo.gl/maps' in href  and not ('address' in park) :

                 gmap_link = href
                 park['map'] = gmap_link
                 park['address'] = aitem.get_text()
                 break

              except :
                pass
            
              park['description'] = desc_text.strip()
              park['amenities'] = all_amenities
              park['type'] = 'Park'
              # print(park)
              
         a_item = item.select('a')
         gmap_link = a_item[0].attrs['href']
         park['map'] = gmap_link

         print('No image for this park')

        except Exception as err:

         print('error',err)

        DATA.append(park)


def get_full_image_dict(soup):

    # print('\nGoogle Images Metadata:')

    # for google_image in soup.select('.isv-r.PNCib.MSM1fd.BUooTd'):
    #     title = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['title']
    #     source = google_image.select_one('.fxgdke').text
    #     link = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['href']
    #     print(f'{title}\n{source}\n{link}\n')

    # this steps could be refactored to a more compact
    all_script_tags = soup.select('script')
    # print(all_script_tags)

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ', '.join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(', ')

    # print('Google Image Thumbnails:')  # in order
    # for fixed_google_image_thumbnail in matched_google_images_thumbnails:
    #     # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
    #     google_image_thumbnail_not_fixed = bytes(fixed_google_image_thumbnail, 'ascii').decode('unicode-escape')

    #     # after first decoding, Unicode characters are still present. After the second iteration, they were decoded.
    #     google_image_thumbnail = bytes(google_image_thumbnail_not_fixed, 'ascii').decode('unicode-escape')
    #     print(google_image_thumbnail)

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '', str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\].*?\"2008\":\[[^,]+,\"([^\"]+)\"\]",
                                                       removed_matched_google_images_thumbnails)

    # print("REMOVED       ", removed_matched_google_images_thumbnails)

    relation = {}
    # print('\nFull Resolution Images:')  # in order
    for (index, (fixed_full_res_image,desc)) in enumerate(matched_google_full_resolution_images):
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
        original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')
        # print(desc, original_size_img)
        relation[desc] = original_size_img

        # ------------------------------------------------
        # Download original images
        # print(f'Downloading {index} image...')
        # opener=urllib.request.build_opener()
        # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
        # urllib.request.install_opener(opener)
        # print('saving ... full image')
        # urllib.request.urlretrieve(original_size_img, f'{savename}.jpg')

    return relation

def get_suggested_search_data(soup):

    for suggested_search in soup.select('.PKhmud.sc-it.tzVsfd'):

        suggested_search_name = suggested_search.select_one('.hIOe2').text
        suggested_search_link = f"https://www.google.com{suggested_search.a['href']}"

        # https://regex101.com/r/y51ZoC/1
        suggested_search_chips = ''.join(re.findall(r'=isch&chips=(.*?)&hl=en-US', suggested_search_link))
        print(f"{suggested_search_name}\n{suggested_search_link}\n{suggested_search_chips}\n")

    # this steps could be refactored to a more compact
    all_script_tags = soup.select('script')

    # https://regex101.com/r/48UZhY/6
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))

    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps() it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # search for only suggested search thumbnails related
    # https://regex101.com/r/ITluak/2
    suggested_search_thumbnails_data = ','.join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

    # https://regex101.com/r/MyNLUk/1
    suggested_search_thumbnail_links_not_fixed = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails_data)

    print('Suggested Search Thumbnails:')  # in order
    for suggested_search_fixed_thumbnail in suggested_search_thumbnail_links_not_fixed:
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        suggested_search_thumbnail = bytes(suggested_search_fixed_thumbnail, 'ascii').decode('unicode-escape')
        print(suggested_search_thumbnail)

def is_url_image(url):    

    mimetype,encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))

def check_url(url):
    """Returns True if the url returns a response code between 200-300,
       otherwise return False.
    """
    try:

        opener=urllib.request.build_opener()
        opener.addheaders=[("Range","bytes=0-10"),("User-Agent","MyTestAgent"),("Accept","*/*")]
        urllib.request.install_opener(opener)

        response = urllib.request.urlopen(url,timeout=10)

        return response.code in range(200, 209)

    except Exception:

        return False

def is_image_and_ready(url):
    return is_url_image(url) and check_url(url)

# First attempt
def get_some_images():

   file_name = 'parks_data.json'

   f = open(file_name, "r")
   DATA = json.loads(f.read())
   f.close()

   print(f'Total Data ->  {len(DATA)}')
   DATA_NO_IMAGE = [d for d in DATA if not len(d['picture'])]
   print(f'Total Data with no images ->  {len(DATA_NO_IMAGE)}')

   EXCLUDES = [' madsp ','realtor','mapcarta',' us ', ' tx ',' maps','sale','price','robbed']
   check_excludes = lambda item : len([ exc_item for exc_item in EXCLUDES if exc_item.lower() in item.lower()]) == 0

   for i in  range(len(DATA)) :

       try : 
           data = DATA[i]

           # print(f'Getting {i}')
           if not len(data['picture']) :
              park_name  = re.sub(r'\s+', ' ',data['name'].lower().strip()) 

              name = data['city'].lower() +' '+ park_name

              headers = {
                    'authority': 'www.google.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
                    'cache-control': 'no-cache',
                    'dnt': '1',
                    'pragma': 'no-cache',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                    'sec-ch-ua-arch': '"x86"',
                    'sec-ch-ua-bitness': '"64"',
                    'sec-ch-ua-full-version': '"100.0.4896.88"',
                    'sec-ch-ua-full-version-list': '" Not A;Brand";v="99.0.0.0", "Chromium";v="100.0.4896.88", "Google Chrome";v="100.0.4896.88"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"14.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
                }

              params = {
                    'q': name,
                    'tbm': 'isch',
                }

              response = requests.get('https://www.google.com/search', headers=headers, params=params)

              if (response.status_code == 200) :

                  soup = BeautifulSoup(response.content,'html.parser')
                  relation = get_full_image_dict(soup)

                  # print('RELATIONS ',relation)
                  suggestions = sorted([ (len(val),val) for val in  relation.keys() if (park_name in val.lower()) and check_excludes(val.lower()) ],key = lambda x : x[0])
                  # print('SUGGESTIONS ',suggestions)

                  # max 3 suggestions
                  max_img = 0

                  for len_suggestion,suggestion in suggestions :

                      image_link = relation[suggestion]

                      if is_image_and_ready(image_link):

                          print(f'Setting image {suggestion} to {park_name}')
                          print(f'{image_link}')
                          DATA[i]['picture'].append(image_link)

                          max_img = max_img + 1
                          if max_img > 3 :
                              break

       except Exception as err:
            print('Error ',err)

   DATA_NO_IMAGE = [d for d in DATA if not len(d['picture'])]
   print(f'Total Data with no images after this threatment  -> {len(DATA_NO_IMAGE)}')

   print('Saving new filled data to parks_data_complete.json ...')
   f = open("parks_data_complete.json", "w")
   f.write(json.dumps(DATA))
   f.close()


def break_down_json_into_js() :

   file_name = 'parks_data_complete.json'

   f = open(file_name, "r")
   DATA_COMPLETE = json.loads(f.read())
   f.close()

   print(f'Total Data ->  {len(DATA_COMPLETE)}')
   DATA_NO_IMAGE = [d for d in DATA_COMPLETE if not len(d['picture'])]
   print(f'Total Data with no images ->  {len(DATA_NO_IMAGE)}')

   #Reclassify

   DATA_COMPLETE = [
        { key:
            ('garden' if ('garden' in dc['description'] or 'garden' in ' '.join(dc['amenities'])) else dc[key])
               if key =='type' else dc[key]
            for key in dc} for dc in DATA_COMPLETE]

   cities =  set([el["city"] for el in DATA_COMPLETE])
   types =  set([el["type"] for el in DATA_COMPLETE])

   for city in cities :
       for _type in types :
          
          DATA_CHUNK = [ el for el in DATA_COMPLETE if el["city"] == city and el["type"] == _type]

          print(f'Fixing and generating data for ... {city} - {_type}')
          f = open(f"backend/kwc-{city.lower().replace(' ','')}-{_type.lower().replace(' ','')}.js", "w")
          f.write(f"{city.lower().replace(' ','')}_{_type.lower().replace(' ','')}=JSON.parse(`" + unidecode.unidecode(json.dumps(DATA_CHUNK)).replace(r'\n',' ').replace('\\u00a0',' ').replace('\\','\\\\') + "`)")
          f.close()

##EXECUTION OF SCRAPPING ....

DO_KITCHENER = False
DO_WATERLOO = False
DO_CAMBRIDGE = False

DATA =[]

if DO_KITCHENER :

    CITY = 'KITCHENER'
    print('Kitchener')
    kitchener_url = 'https://facilities.kitchener.ca/?CategoryIds=&FacilityTypeIds=40972%2C40984%2C40967%2C40970%2C40973%2C40977%2C40964%2C40938%2C40979&Keywords=&ScrollTo=google-map-trigger&CloseMap=true'
    response = requests.get(kitchener_url)

    if (response.status_code == 200) :

      soup = BeautifulSoup(response.content,'html.parser')
      pages = int(soup.select('.pagination-pageof')[0].get_text().split('of ')[-1])

      # pages = 1
      if (response.status_code == 200) :

          for page in range(1,pages+1):
            print(f'Processing page {page}')

            kitchener_process_page(page)

    print('KITCHENER All info collected ...')
    # print((DATA))

    # # write
    # f = open("parks_data.json", "w")
    # f.write(json.dumps(DATA))
    # f.close()

if DO_WATERLOO :

    CITY = 'WATERLOO'

    print('Waterloo')


    print('WATERLOO All info collected ...')

    waterloo_process_page()

    # write
    # f = open("parks_data.json", "a")
    # f.write(json.dumps(DATA))
    # f.close()

if DO_CAMBRIDGE :

    CITY = 'CAMBRIDGE'
    print('Cambridge')
    url = 'https://facilities.cambridge.ca/?CategoryIds=&FacilityTypeIds=77%2C75%2C38%2C44&Keywords=&ScrollTo=google-map-trigger&CloseMap=true'
    response = requests.get(url)

    if (response.status_code == 200) :

      soup = BeautifulSoup(response.content,'html.parser')
      pages = int(soup.select('.pagination-pageof')[0].get_text().split('of ')[-1])

      # pages = 1
      if (response.status_code == 200) :

          for page in range(1,pages+1):
            print(f'Processing page {page}')

            cambridge_process_page(page)

    print('CAMBRIDGE All info collected ...')

    # write
    # f = open("parks_data.json", "a")
    # f.write(json.dumps(DATA))
    # f.close()

# EXPORT DATA
if len(DATA) :

    print('Exporting data to parks_data.json ...')
    f = open("parks_data.json", "w")
    f.write(json.dumps(DATA))
    f.close()

# sys.exit(0)

#ADD SOME MISSING IMAGES ...
# Try to get images from web
 
# get some photos...
print('Filling some blank images from Google Images ...')
# get_some_images()


print('Breaking down files and exporting as JS')
# break_down_json_into_js()

def fix_waterloo_map() :

   file_name = 'parks_data_complete.json'

   f = open(file_name, "r")
   DATA_WATERLOO = json.loads(f.read())
   f.close()

   DATA_WATERLOO = [ dc for dc in DATA_WATERLOO if dc['city'] == 'WATERLOO']

   cities =  set([el["city"] for el in DATA_WATERLOO])
   types =  set([el["type"] for el in DATA_WATERLOO])

   for idx in range(len(DATA_WATERLOO)):
     map = DATA_WATERLOO[idx]['map']
     map_data = requests.get(map)
     if (map_data.status_code == 200):
         coords = re.findall(r'\/@(-?\d+\.?\d*),(-?\d+\.?\d*)',map_data.url)
         print(f'Park name {DATA_WATERLOO[idx]["name"]}')
         print(f'Getting map coordinates {coords}')
         DATA_WATERLOO[idx]['map'] = list(coords[0])

   for city in cities :
       for _type in types :
        
          DATA_CHUNK = [ el for el in DATA_WATERLOO if el["city"] == city and el["type"] == _type]

          print(f'Fixing and map data for ... {city} - {_type}')
          f = open(f"backend/kwc-{city.lower().replace(' ','')}-{_type.lower().replace(' ','')}.js", "w")
          f.write(f"{city.lower().replace(' ','')}_{_type.lower().replace(' ','')}=JSON.parse(`" + unidecode.unidecode(json.dumps(DATA_CHUNK)).replace(r'\n',' ').replace('\\u00a0',' ').replace('\\','\\\\') + "`)")
          f.close()

print('Fixing Waterloo maps ...')
fix_waterloo_map()
