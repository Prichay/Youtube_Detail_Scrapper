import signal
import os
import time
import sys
from requests import get
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import redis
import time
import logging
# defining few func to check for the SIGTERM to receive and soft terminate the script.
def terminateProcess(signalNumber, frame):
    print ('(SIGTERM) terminating the process')
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, terminateProcess)#look for the signal to teminate the script
    print('My PID is:', os.getpid()) #broadcast PID of the process to use with the signal
# Run the script indefinately to constantly look for the 'process' Redis list and when anything added, process it.
while True:
    r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
    # When the list contain some info
    if bool(r.exists('process'))==True:
        Url= r.lpop('process')
        ses = HTMLSession()
        webpage = ses.get(Url)
        webpage.html.render(timeout=10,sleep=3)
        soup = BeautifulSoup(webpage.html.html, 'html.parser')
        meta = []
        meta.append(soup.find("div", {"id": "date"}).text[1:])# extract Upload Date
        date=meta[0]# Making sure that date has some value, if dosen', seudo value will be given
        if bool(date) == True:
            logging.critical("Got the date")
        else:
            logging.critical("Video do not have a date. Will be given Seudo Value 'dd-mm-yyyy'")
            meta[0] = "dd-mm-yyyy"
        time.sleep(1)
        #Extract Video Title
        meta.append(soup.find("h1").text.strip())
        title = meta[1]
        if bool(title) == True:
            logging.critical("Got the Title")
        else:
            logging.critical("Video do  not have a title. Will be given Seudo Value 'xxxxxx'")
            meta[1] = "XXXX"
        time.sleep(1)
        #Extract View Count
        meta.append(soup.find("span", class_="view-count").text)
        views = meta[2]
        if bool(views) == True:
            logging.critical("Got the Views")
        else:
            logging.critical("Video do not have a Views. Will be given Seudo Value '0'")
            meta[2] = "0"
        time.sleep(1)
        #Extract Hash Tags
        meta.append(soup.find("yt-formatted-string", class_="super-title style-scope ytd-video-primary-info-renderer").text)
        tags = meta[3]
        if bool(tags) == True:
            logging.critical("Got the Tags")
        else:
            logging.critical("Video do not have a Tags. Will be given Seudo Value '##'")
            meta[3] = "##"
        time.sleep(1)
        #extract Channel Name
        meta.append(soup.find("div", {"id": "text-container"}).text[1:-1])
        ch_name = meta[4]
        if bool(ch_name) == True:
            logging.critical("Got the Channel Name")
        else:
            logging.critical("Video do not have a Channel Name. Will be given Seudo Value 'xxxx'")
            meta[4] = "XX"
        time.sleep(1)
        #Extract Subscribers
        meta.append(soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text)
        subs = meta[5]
        if bool(subs) == True:
            logging.critical("Got the Subscribers")
        else:
            logging.critical("Video do not have Subscribers. Will be given Seudo Value 'xx'")
            meta[5] = "XX"
        time.sleep(1)
        #extract Duration
        meta.append(soup.find("span", {"class": "ytp-time-duration"}).text)
        duration = meta[6]
        if bool(duration) == True:
            logging.critical("Got the Dureation Of the Video")
        else:
            logging.critical("Video do not have Fixed Duration. Will be given Seudo Value 'xx:xx'")
            meta[6] = "xx:xx"
        time.sleep(1)
        #Extract Description
        meta.append(soup.find("div", {"id":"description"}).text)
        des = meta[7]
        if bool(des) == True:
            logging.critical("Got the Description")
        else:
            logging.critical("Video do not have a Discription. Will be given Seudo Value 'xxxx'")
            meta[7] = "XXXX"
        att = ['Date', 'Title', 'View', 'Tag', 'Ch_Name', 'Subs', 'Duration', 'Description']
        dict = {}
        #Ussing a Dict{} to make Key-Value pair for the Attributes and Corresponding Values
        for i in range(8):
            dict.update({att[i]: meta[i]})
        #apusing the Attributes in a 'Keys' List and vlaues in a 'Values' List
        for i in dict.keys():
            r.lpush('Keys', i)
            r.lpush('Values', dict[i])
        #Delete the 'process' List to stay looping indefinately with overdoing anything
        r.delete('process')
        #again print to get PID on top again
        print("\n","My PID Is :",os.getpid())