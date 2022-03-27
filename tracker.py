from bs4 import BeautifulSoup as bs
import json
import requests,csv
import random
import re,time
from faker import Faker

def createfile(row):
    with open('/home/krishna/work/SocialBlade/influencers_details.csv', 'a',encoding='UTF-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    
fake=Faker()
yt=[]
ys=[]
list1= []
names=[]
f=open('/home/krishna/work/SocialBlade/userids.csv','r',encoding="UTF-8")
#collect data from csv
#append data
for line in f:
    names.append(line.strip())

j=0
person_count=0

for i in range(0,len(names)):
    count=0
    try:#requesting data of each userid after 0.3 sec wait
        time.sleep(0.3)
        source_data = requests.get("https://www.instagram.com/"+str(names[i]),headers={'User-Agent':fake.user_agent() })
    
    except OSError:#avoiding os error and retrying
        source_data = requests.get("https://www.instagram.com/"+str(names[i]),headers={'User-Agent':fake.user_agent() })

    if source_data.status_code is 200:#200 is http code for data existing 
        #if true collect data and parse it
         bs_data = bs(source_data.text,'html.parser')
    else:
        continue
    body = bs_data.find('body')#go to the data inside body tag
    if len(body)==0:
        print("body empty")
    script_tag = body.find('script')#got o  body tag and move to data inside script tag
    #take data present inside window._sharedData = and replace it with '' as it is not necessary
    raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
    #data inside raw string is in json format
    #use json.loads to parse
    try:
        mydata = json.loads(raw_string)
    except:
        print("JSONDecodeError")
        time.sleep(10)
        script_tag = body.find('script')
        print(len(script_tag))
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        print(len(raw_string))
        mydata = json.loads(raw_string)
#  #   soup=bs(source_data.text,'html.parser')
    
#  #   emaildata = soup.find_all('script', attrs={'type': 'application/ld+json'})
#""""logic is to map inside the data  which is in key value pairs i.e
# in json format step by step and pull out values assigned to keys""""


    for v in mydata['entry_data']['ProfilePage']:#travese through json
        person_count=person_count+1
        print(person_count)
        for some in v['graphql']['user']['edge_followed_by']:
            followers=v['graphql']['user']['edge_followed_by']['count']
            print(followers)
            row=[followers]

    
        for vv in v['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            count=count+1
            likes=vv['node']['edge_liked_by']['count']
            row.append(likes)

            if count==3:
                row.append(names[i])
                createfile(row)
                break
#             row=[names[i],followers,vv['node']['shortcode'],timestamp,vv['node']['edge_liked_by']['count'],vv['node']['edge_media_to_comment']['count'],contain_caption,loc_id,slug,vv['node']['display_url'],caption_data,hashtags,tagged,links]

