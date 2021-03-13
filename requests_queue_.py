import time
import argparse
from requests import get
import redis
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import logging
#using the argparse function to use the script in CLI
p=argparse.ArgumentParser(prog='Store the parsed Youtube URL into Redis List',usage='Input a Valid Youtube URL to parse',description='Help Menu',allow_abbrev=False)
p.add_argument('-URL',required=True,type=str,help='URL of Youtube Video',metavar='')
arg=p.parse_args()
try:#creating a localhost connection with Redis Server to use the List function
    r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
except:
    logging.critical('Connection with the Redis server is not established')
try:
    #creating a URL Session to get HTML of the desired Youtube Video
    ses = HTMLSession()
    webpage = ses.get(arg.URL)
    #rendering the javascript to compile the downloded HTML code for parsing
    webpage.html.render(timeout=10,sleep=3)# timeout is 8 sec by default but given 10 to make sure that all the required lines are compiled.
    soup = BeautifulSoup(webpage.html.html, 'html.parser')#using bs4 liberary to parse the HTML code
    time.sleep(1)
    meta = []
    meta.append(soup.find("h1").text.strip())#check the validity of the URL by striping the name of the Video.
    title = meta[0]
    if bool(title)==True:# if URL has a video name then it is a youtube URl.
        print('\tURL VARRIFIED')
        r.rpush('process',arg.URL)#Tail pushing the URL given in parsearg in redis list named 'process' for further processing
        print("\tSuccessfully carried out the request_queue.py script\n\tdata is fetched in redis list 'process' in localhost\n\tto be used by requests_process.py")
    else:
        print("\tINVALID URL")
except:
    logging.critical('Something Went wrong\nEither the validity of the given URL\nOR\nBeautiful Soup Object\nSuggestion: Rerun the script')