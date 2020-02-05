import requests
import json



import pycurl
from io import BytesIO
from urllib.parse import urlencode

url_to_work = 'https://jsonplaceholder.typicode.com/posts'


def main():
    


    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://jsonplaceholder.typicode.com/posts')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    #body.decode('iso-8859-1')
    
    jsonized_body = json.loads(body.decode('utf-8'))
    #print(type(jsonized_body))
    jsonized_body.reverse()
    #print(jsonized_body)


    #sending part
    #urlencoding ->> form data must be provided already urlencoded
    c2 = pycurl.Curl()
    c2.setopt(c.URL, 'https://jsonplaceholder.typicode.com/posts')
    #c2.setopt(c.WRITEDATA, buffer)
    

    for data in jsonized_body:
        postfields = urlencode(data)
        c2.setopt(c.POSTFIELDS, postfields)
        c2.perform()

    c2.close()

    
    
    #************
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
