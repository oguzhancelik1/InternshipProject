import requests
import json


#FOR PYCURL
import pycurl
from io import BytesIO
from urllib.parse import urlencode

#FOR THREADING
import threading

#FOR ARGPARSE
import argparse

#FOR BEUTIFULSOUP4
from bs4 import BeautifulSoup
# this url is used to get the information within posts, or post information to posts 
url_to_work   = 'https://jsonplaceholder.typicode.com/posts'
# this url is used to scrape the content of the main page
url_to_scrape = 'https://jsonplaceholder.typicode.com'


proxies_dict = {
        'http': 'http://195.154.176.130:4030',
        'https' : 'https://195.154.176.130:4030'

    }

lock = threading.Lock()

proxy_selection=None


def get_information(url):

    s = requests.Session()
    
    response = s.get(url,proxies=None)

    return response

def reverse_prepare_data(rsp):

    reversed_response_list = []

    response = json.loads(rsp.text)
    response.reverse()
    for val in response:
        data_holder = json.dumps(val)
        reversed_response_list.append(data_holder)
    return reversed_response_list




def post_information(value,proxy_selection,url):

    
    s = requests.Session()
    
    print((s.post(
        url,
        data=value,
        headers={
            "Content-type": "application/json; charset=UTF-8"
        },
        proxies=proxy_selection)).text)
def get_page_content():
    s = requests.Session()
    
    response = s.get(url_to_scrape,proxies=None)

    return response

    
def scrape_data(page):
    page = page
    soup = BeautifulSoup(page.content, 'lxml')

    # get the div
    match_of_divs_routes = soup.find('div', class_='container')
    # get the table within div
    match_of_tables_routes = match_of_divs_routes.find_all('table') # match_of_tables_routes is a list
    # get the tr in the appropriate table(in this case the second one)
    match_of_trs_routes = match_of_tables_routes[1].find_all('tr')
    # create a list to hold the postable endpoints
    endpoints_with_post_in_routes=[]

    for each in match_of_trs_routes:
            # get each td value within tr
            match_of_tds_routes = each.find_all('td')
            # check if the td has the 'POST' 
            if match_of_tds_routes[0].text=='POST':
              #print('this is a td with post in the routes')
              endpoints_with_post_in_routes.append(match_of_tds_routes[1].text.strip())
            #else:
              #print('this is a td without post in the routes')  
    

    print('All postable endpoints are : ')
    for each in endpoints_with_post_in_routes:
        print(repr(each))

    # get the match of the tables, find() will find the first occurence
    # which in this case what is needed
    match_of_tables_resources= soup.find('table',class_='resources')
    # get the trs within the table
    match_of_trs_resources = match_of_tables_resources.find_all('tr')
    # create a list to hold the the all possible endpoints in resources
    endpoints_in_resources = []

    for each in match_of_trs_resources:
        # get the match of tds for each tr 
        match_of_tds_resources=each.find_all('td')
        endpoints_in_resources.append(match_of_tds_resources[0].text.strip())

    print('All endpoints in resources are :')
    intersection_list = []

    for each in endpoints_in_resources:
        print(repr(each))
    
    for each in endpoints_with_post_in_routes:
        checker=each
        for val in endpoints_in_resources:
            
            if checker==val:
                intersection_list.append(each)

            else:
                print('lol')

    for each in intersection_list:
        print(each)

    return intersection_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
         '-s','--selection', 
         help='Type 1 for proxies, type 2 for non proxies',
         type = int
         )
    parser.add_argument(
         '-t','--threading',
         help ='Type 1 for threading, type 2 for non threading',
         type=int )    
    args = parser.parse_args()


    info_to_scrape = get_page_content()

    # get the endpoints that are postable
    intersection_list_returned = scrape_data(info_to_scrape)

    dict_holds_data_from_endpoints = {}

    for each in intersection_list_returned:
        url_to_get = url_to_scrape + each

        response_after_get = get_information(url_to_get)
        list_of_reversed_jsons = reverse_prepare_data(response_after_get)
        dict_holds_data_from_endpoints[each] = list_of_reversed_jsons
    #get information from /posts enpoint
    
  
    #url_to_scrape is the default site
    url_to_post   = url_to_scrape
    
    if (args.selection == 1):
        proxy_selection= proxies_dict

    
    elif(args.selection == 2):
        proxy_selection= None

    if(args.threading == 1):

        

        for key in dict_holds_data_from_endpoints:

            url_to_post = url_to_scrape + key
            list_of_reversed_jsons = dict_holds_data_from_endpoints[key]
        
            threads = []
             # create separate threads for all items and call post_information function
            for val in list_of_reversed_jsons:
                t= threading.Thread(target=post_information, args = (val,proxy_selection,url_to_post,))
                t.start()
                threads.append(t)
                
            for val in threads:
                val.join()

    elif(args.threading == 2):

        for key in dict_holds_data_from_endpoints:
            url_to_post = url_to_scrape + key
            list_of_reversed_jsons = dict_holds_data_from_endpoints[key]
            
            for val in list_of_reversed_jsons:

                post_information(val,proxy_selection,url_to_post)






















    #***********************    ARGPARSE    **********************************
       
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-s','--selection', 
    #     help='Type 1 for proxies, type 2 for non proxies',
    #     type = int
    #     )
    # parser.add_argument(
    #     '-t','--threading',
    #     help ='Type 1 for threading, type 2 for non threading',
    #     type=int )    
    # args = parser.parse_args()
    
   
    # #it will get the posts using proxies
    # response_after_get = get_information()

    # #it will hold the json strings of each entry
    # list_of_reversed_jsons = reverse_prepare_data(response_after_get)
    
    # if (args.selection == 1):
    #     proxy_selection= proxies_dict

    
    # elif(args.selection == 2):
    #     proxy_selection= None

    # if(args.threading == 1):

    #     threads = []

    #     for val in list_of_reversed_jsons:
    #         t= threading.Thread(target=post_information, args = (val,proxy_selection,))
    #         t.start()
    #         threads.append(t)
            
    #     for val in threads:
    #         val.join()

    # elif(args.threading == 2):

    #     for val in list_of_reversed_jsons:

    #         post_information(val,proxy_selection)


    #***********************    THREADING   **********************

    # response_after_get = get_information()

    # list_of_reversed_jsons = reverse_prepare_data(response_after_get)

    # threads=[]

    # for val in list_of_reversed_jsons:
    #     t= threading.Thread(target=post_information,args=(val,))
    #     t.start()
    #     threads.append(t)
      
    # #print(response.text)
    
    # for val in threads:
    #     val.join()
    
    # print('ayaktayım')














#*****************  PROXIES AND SESSION ********************************
    # s = requests.Session()
    # proxies_dict = {
    #     'http': 'http://195.154.176.130:4030',
    #     'https' : 'https://195.154.176.130:4030'

    # }
    # response = s.get(url_to_work,proxies=proxies_dict)

    # asd = json.loads(response.text)
    # asd.reverse()
    # # print(type(response.text))
    # # print(type(asd))
    # # print(type(response.json()))
    # # print(type(response))
    # for val in asd:
    #    print((s.post(url_to_work,data=json.dumps(val),
    #    headers={
    #     "Content-type": "application/json; charset=UTF-8"
    #     },
    #     proxies=proxies_dict)).text)
    # #print(response.text)




 
    #*******************  PYCURL   ******************************************

    # buffer = BytesIO()
    # c = pycurl.Curl()
    # c.setopt(c.URL, 'https://jsonplaceholder.typicode.com/posts')
    # c.setopt(c.WRITEDATA, buffer)
    # c.perform()
    # c.close()

    # body = buffer.getvalue()
    # # Body is a byte string.
    # # We have to know the encoding in order to print it to a text file
    # # such as standard output.
    # #body.decode('iso-8859-1')
    
    # jsonized_body = json.loads(body.decode('utf-8'))
    # #print(type(jsonized_body))
    # jsonized_body.reverse()
    # #print(jsonized_body)


    # #sending part
    # #urlencoding ->> form data must be provided already urlencoded
    # c2 = pycurl.Curl()
    # c2.setopt(c.URL, 'https://jsonplaceholder.typicode.com/posts')
    
    

    # for data in jsonized_body:
    #     postfields = urlencode(data)
    #     c2.setopt(c.POSTFIELDS, postfields)
    #     c2.perform()

    # c2.close()

    
    
    #************   REQUESTS  ******************************************
    # rsp = get_request()
    # writejson = json.loads(rsp.text)
    # writejson.reverse()
    # for data in writejson:
    #     print(post_request(json.dumps(data)).text)
    #**************


def post_request(data):

    rsp = requests.post(url_to_work,data=data, headers={
        "Content-type": "application/json; charset=UTF-8"
    })
    return rsp
    # for val in writejson:
    #     id_no = val.get('id')
    #     print(id_no)
    # result = Session.post(SubmitURL, data=post_data)
    # if result.status_code == requests.codes.ok:
    #     print(result.text)


def get_request():
    response = requests.get(url_to_work)
    # writejson = json.loads(response.text)

    return response







if __name__ == '__main__':
    main()
