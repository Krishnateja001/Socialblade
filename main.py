import requests
import json
from bs4 import BeautifulSoup as bs
import requests,csv
import random
import re,time
from faker import Faker
import itertools
import mysql.connector 
names=[]

connection = mysql.connector.connect(host='localhost',
                             database='SocialBlade',
                             user='root',
                             password='root@123')


def server(row):
    print(row)  
    if connection.is_connected():
       db_Info = connection.get_server_info()
      #  print("Connected to MySQL database... MySQL Server version on ",db_Info)
       cursor = connection.cursor()

       cursor.execute('''
       Insert into Tracker (followers,like1,shortcode_1,like2,shortcode_2,like3,shortcode_3,userid) values (%s, %s, %s,%s,%s,%s,%s,%s)''',row )#(str(row[4]),str(row[0]),str(row[1]),str(row[2]),str(row[3]))
    #    record = cursor.fetchone()
       connection.commit()

def get_data_from_server(name):
      cursor = connection.cursor()
      select_query="select * from Tracker where userid = '{x}' order by ID desc limit 1".format(x=name)
      print(select_query)
      cursor.execute(select_query)
      data=cursor.fetchall()
      print(list(data[0]))
      
def like_list_server(name):
      cursor = connection.cursor()
      latest_shortcode="select shortcode_1,shortcode_2,shortcode_3 from Tracker  where userid='{userid}' order by ID desc limit 1;".format(userid=name)
      cursor.execute(latest_shortcode)
      lis=cursor.fetchone()

      like1="select like1 from Tracker where shortcode_1='{x}' ".format(x=lis[0])
      cursor.execute(like1)
      data=cursor.fetchall()
      out1 = list(itertools.chain(*data))


      like2="select like2 from Tracker where shortcode_2='{x}' ".format(x=lis[1])
      cursor.execute(like2)
      data=cursor.fetchall()
      out2 = list(itertools.chain(*data))

      like3="select like3 from Tracker where shortcode_3='{x}' ".format(x=lis[2])
      cursor.execute(like3)
      data=cursor.fetchall()
      out3 = list(itertools.chain(*data))
      # like2="select like2 from Tracker where userid = '{x}' ".format(x=name)
      # cursor.execute(like2)
      # data=cursor.fetchall()
      # out2 = list(itertools.chain(*data))
      # like3="select like3 from Tracker where userid = '{x}' ".format(x=name)
      # cursor.execute(like3)
      # data=cursor.fetchall()
      # out3 = list(itertools.chain(*data))
      return out1,out2,out3


def get_followers_list_server(name):
      cursor = connection.cursor()
      select_query="select followers from Tracker where userid = '{x}' ".format(x=name)
      print(select_query)
      cursor.execute(select_query)
      data=cursor.fetchall()#form of list of tuples 
      out = list(itertools.chain(*data))
      return out



def get_followers():
      followers_list=[]
      person_list=[]
      person_count=0
      f=open('/home/krishna/work/SocialBlade/userids.csv','r',encoding="UTF-8")
#collect data from csv
#append data
      for line in f:
            names.append(line.strip())
      for i in range(0,len(names)):#len(names)
            count=0
            try:#requesting data of each userid after 0.3 sec wait
                  time.sleep(0.3)
                  source_data = requests.get("https://www.instagram.com/"+str(names[i]))
            
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
            script_tag = body.find('script')#got a body tag and move to data inside script tag
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
                  person_list.append(person_count)
                  row=[]
                  for some in v['graphql']['user']['edge_followed_by']:
                        followers=v['graphql']['user']['edge_followed_by']['count']
                        print(followers)
                        row=[followers]
                        followers_list.append(followers)
                  for vv in v['graphql']['user']['edge_owner_to_timeline_media']['edges']:
                      count=count+1
                      likes=vv['node']['edge_liked_by']['count']
                      shortcode=vv['node']['shortcode']
                      row.append(likes)
                      row.append(shortcode)
                      if count==3:
                        row.append(names[i])
                        print(row)
                        server(row)  
                        break
                                          
      dictionary = dict(zip(person_list, followers_list))
      print( dictionary)
    
get_followers()
#get_data_from_server('foodiesground')
#  get_followers_list_server()
# like_list_server('foodiesground')