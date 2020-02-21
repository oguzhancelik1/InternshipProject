import requests
import json

#FOR PYCURL
import pycurl
from io import BytesIO
from urllib.parse import urlencode
import time

#FOR THREADING
import threading

#FOR ARGPARSE
import argparse
trial_url='https://api.ipify.org/?format=json'

scrape_url = 'https://twitter.com/i/trends'

search_api_url ='https://stream.twitter.com/1.1/statuses/sample.json'
#https://stream.twitter.com/1.1/statuses/sample.json REQUIRES NO AUTHENTICATION
#https://api.twitter.com/1.1/search/tweets.json REQUIRES AUTHENTICATION
#FOR BEUTIFULSOUP4
from bs4 import BeautifulSoup

import twitter_credentials

lock = threading.Lock()


from requests_oauthlib import OAuth1

proxies_dict = {
        'http': 'http://195.154.176.130:4030',
        'https' : 'https://195.154.176.130:4030'

    }

start_time = time.time()

consumer_secret = twitter_credentials.consumer_secret
consumer_key = twitter_credentials.consumer_key
access_token_secret = twitter_credentials.access_token_secret
access_token = twitter_credentials.access_token
class RestApi:
   
    
    def __init__(self, endpoint_url):
        self.url=endpoint_url    
    
    @staticmethod
    def authenticate_access():
        authentication = OAuth1(consumer_key,consumer_secret,access_token,access_token_secret)

        return authentication

    @staticmethod
    def get_request(url,proxy_selection):
        auth = RestApi.authenticate_access()
        response = requests.get(url,auth = auth,timeout=10,stream=True,proxies=proxy_selection)
        return response
    
    @staticmethod
    def get_pycurl(url):
        

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)

        c.setopt(pycurl.PROXY, '195.154.176.130')
        c.setopt(pycurl.PROXYPORT, 4030)
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        

        c.perform()
        c.close()

        #byte type value 
        response = buffer.getvalue()

        #string type value
        response=response.decode('iso-8859-1')

        #dictionary type value
        #response = json.loads(response.decode('utf-8'))
        
        # print(response)
        # print(type(response))
        
        

    
        
        
       
        return response
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    #body.decode('iso-8859-1')
    
    



    
    def post_request(self):
        pass

class Tweets:
    tweet_arr = []
    #keywords_file='keywords.text'
    
    def __init__(self,keywordsfile_name):
        self.keywords_file = keywordsfile_name
        

    
    
    def form_keyword_string(self):
        with open(self.keywords_file, 'r') as file:
            keyword_string = file.read().replace('\n', ' ')
        keyword_string = keyword_string.split(' ')

        return keyword_string

    

    def get_tweets(self,val,get_response,keyword_string):
        #
        # val is only used to discern threads
        # if no threads, pass in None
        response= get_response
        i=0
        a=0
        lock.acquire()
        for line in response.iter_lines():
            lock.release()
            if line: # filter out keep-alive new lines
                #print(line)
                if 'delete' not in json.loads(line):
                    a=a+1
                    if 'text' in json.loads(line) and all(keyword in json.loads(line)['text'] for keyword in keyword_string):
                        # if  not in json.loads(line)['id_str']:
                        Tweets.tweet_arr.append(json.loads(line)['id_str'])
                        print('**********************' + str(json.loads(line)['text']) + '*****************')
                        i=i+1
                    #print(json.loads(line))
                print('********************'+str(i)+'*****************************')
                print('total tweets********'+str(a)+'*******************************')
                print('Hey I am thread no  *********'+str(val)+'********** I work ')
            if time.time() - start_time > 300:
                break
            lock.acquire()
        
    def save_tweets_with_keywords(self):        
        pass
    def calculate_percentage(self):
        pass

def scrape_trends(response):
    page = response

    #works for requests.get response, to utilize pycurl instead of page.text use page
    soup = BeautifulSoup(json.loads(page.text)["module_html"], 'lxml')
    match_of_spans = soup.find_all('span', class_='u-linkComplex-target trend-name')
    trends=[]

    for each in match_of_spans:
        for val in each:
            trends.append(val)

    return trends


def main():
    #******************* Scrape for both pycurl and requests************************************ 
    # get_pycurl returns a dictionary already, also page.text is not needed nor supported by pycurl

    # rsp=RestApi.get_pycurl(scrape_url)
    # #rsp=RestApi.get_request(scrape_url,None)
    # t=scrape_trends(rsp)
    # for each in t:
    #     print(each)
    # import sys
    # sys.exit(1)



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
    parser.add_argument(
         '-c','--threadcount',
         help ='Number of threads to be created',
         type=int )
        
    args = parser.parse_args()

    #print(args.threadcount)

   
    #************************************
    # ******** Read for func()***********
    # gets the get_request() return value, passes it to get_tweets() function
    # Tweets.form_keyword_string takes a file consisting of keywords and returns a string to pass
    def func(val,response,keyword_string,tweets_obj):
        
        
        tweets_obj.get_tweets(val,response,keyword_string)


    if (args.selection == 1):
        proxy_selection= proxies_dict
        
    
    elif(args.selection == 2):
        proxy_selection= None


    response= RestApi.get_request(search_api_url,proxy_selection)
    tweets_obj = Tweets('keywords.text')
    keyword_string = tweets_obj.form_keyword_string()

    if(args.threading == 1):

        if(args.threadcount>0):

            
            threads = []
            
            # print(args.threadcount)
            # import sys
            # sys.exit(1)
            for val in range(args.threadcount):
                t= threading.Thread(target=func, args = (val,response,keyword_string,tweets_obj))
                t.start()
                threads.append(t)
                
            for val in threads:
                val.join()
        else:
            print('You wish to operate with threads, please specify threadcount bigger than 0')
    elif(args.threading == 2):

        if(args.threadcount == 0):
            val='No Threading'
            func(val,response,keyword_string,tweets_obj)

        else:
            print('You wish to operate with no threads, please specify threadcount to 0')
    
    
   


    
   


















    #****************************************   Beatifulsoup4 get trends    *******************************
    # page = RestApi.get_request(scrape_url)
    
    # soup = BeautifulSoup(json.loads(page.text)["module_html"], 'lxml')
    # #print(soup.prettify())
    
    
    # match_of_spans = soup.find_all('span', class_='u-linkComplex-target trend-name')
    # trends=[]


    
    
    # for each in match_of_spans:
    #     for val in each:
    #         trends.append(val)


    # for each in trends:
    #     print(each)



    #**************   twittersearch api with classed structure    *************************

    # tweets_obj = Tweets('keywords.text')
    # response = RestApi.get_request(search_api_url)

    # keyword_string = tweets_obj.form_keyword_string()
    # tweets_obj.get_tweets(response,keyword_string)
    

    



















    #***********************************Twitter Search Api get from sample.json or tweets.json******************
    
    # authentication = OAuth1(consumer_key,consumer_secret,access_token,access_token_secret)
    
    # print(type(authentication))
    

    # with open('keywords.text', 'r') as file:
    #     keyword_string = file.read().replace('\n', ' ')
    # print(keyword_string)
    # keyword_string = keyword_string.split(' ')
    # print(keyword_string)
    # # keyword_string=''
    # # for each in keywords:
    # #     word = keywords[each]
    # #     keyword_string=keyword_string+''+each

    # # actualkeywords={'q': keyword_string}
    
    # params={'q': keyword_string}
    # #params['q'] = 'oguzhan'
    # response = requests.get(search_api_url,auth = authentication,timeout=10,stream=True)
    # i=0
    # a=0
    # tweet_arr = []
    # for line in response.iter_lines():
    #     if line: # filter out keep-alive new lines
    #         if 'delete' not in json.loads(line):
    #             a=a+1
    #             if 'text' in json.loads(line) and all(keyword in json.loads(line)['text'] for keyword in keyword_string):
    #                 # if  not in json.loads(line)['id_str']:
    #                 tweet_arr.append(json.loads(line)['id_str'])
    #                 print('**********************' + str(json.loads(line)['text']) + '*****************')
    #                 i=i+1
    #             #print(json.loads(line))
    #         print('********************'+str(i)+'*****************************')
    #         print('total tweets********'+str(a)+'*******************************')
                
                
            



if __name__ == '__main__':
    main()