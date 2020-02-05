import requests
import json


#FOR PYCURL
import pycurl
from io import BytesIO
from urllib.parse import urlencode

#FOR THREADING
import threading

url_to_work = 'https://jsonplaceholder.typicode.com/posts'

proxies_dict = {
        'http': 'http://195.154.176.130:4030',
        'https' : 'https://195.154.176.130:4030'

    }

lock = threading.Lock()

def get_with_proxy():

    s = requests.Session()
    
    response = s.get(url_to_work,proxies=proxies_dict)

    return response

def reverse_prepare_data(rsp):

    reversed_response_list = []

    response = json.loads(rsp.text)
    response.reverse()
    for val in response:
        data_holder = json.dumps(val)
        reversed_response_list.append(data_holder)
    return reversed_response_list




def post_with_proxy(value):
    s = requests.Session()
    
    print((s.post(url_to_work,data=value,
       headers={
        "Content-type": "application/json; charset=UTF-8"
        },
        proxies=None)).text)


def main():
    #***********************    THREADING   **********************

    response_after_get = get_with_proxy()

    list_in_main = reverse_prepare_data(response_after_get)

    threads=[]

    for val in list_in_main:
        t= threading.Thread(target=post_with_proxy,args=(val,))
        t.start()
        threads.append(t)
      
    #print(response.text)
    
    for val in threads:
        val.join()
    
    print('ayaktayım')














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
