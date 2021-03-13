import redis
import csv
r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
#write the details scrapped into a CSV File
with open('requests_save.csv','w',newline='',encoding="utf-8") as file:
    write=csv.writer(file,delimiter='\t') # Every Two values will be seperated by a TAB space
    write.writerow(['\tKeys''\t\t''\tValues']) # HEADINGS
    for i in range (r.llen('Keys')):
        write.writerow([r.lpop('Keys'),r.lpop('Values')]) # push the KEYS and VALUES in the CSV FILE
    print("All the Work in done\nYou Will find the details about the video in \n\t'requests_save.csv'\nin your working script directory")