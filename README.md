# Youtube_Detail_Scrapper
Files in this repo can be publically used to scrape details of a youtube video with a valid URL using REDIS Lists
## Liberary Used
### Signal 
* Use to detect the SIGTERM signal to soft terminate the requests_process script using its PID
### os
* Use to know the PID of the process for soft termination 
### time
* Use to slow down the script for better processing
### sys
* To exit out the script 
### requests.get
* To fetch the url of given Youtube Video
### BeautifulSoup
* HTML parcer
* Find() Func to extract detalis
### requests_html.HTMLSession
* To initiate a WebSession to get HTML Code
### redis
* In-memory fast paced push/pull DB
* To transfer key-value dict of details and URL to its memory to be extracted by following script to process
### logging
* To Log criticle messages
### csv
* To write a file with scraped details of the video for further processing
## Prep the machine
Before running any script make sure that you had installed all the above given liberaries to avoid any confliction.
### Installing a REDIS server to you machine:
* First, try to install the server originally from the official release.
* In some cases your machine is not capable of handling all this processing of continuous script, server and data manipulation at the same time. So there are files in
the repo to give you a temporary server which will do all the original work and is not a burden on your system. You can create lists, manipulate data and validate and 
do all those 
