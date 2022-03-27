from flask import Flask, render_template,request,jsonify
import requests
import json
from bs4 import BeautifulSoup as bs
import json
import requests,csv
import random
import re,time
from faker import Faker
import mysql.connector 
from main  import get_followers_list_server,like_list_server
names=[]
fake=Faker()
app = Flask(__name__)
connection = mysql.connector.connect(host='localhost',
                             database='SocialBlade',
                             user='root',
                             password='root@123')




def get_data_from_server(name):
      return 0

@app.route('/index/<hello>', methods = ['GET' , 'POST'])
def hello_name(hello):
      user_id=[]
      followers=[]
      # whole_data = get_data_from_server(hello)
      # for key, value in whole_data.items() :
      #       user_id.append(key)
      #       followers.append(value)
      # pid = request.args.get('pid')
      return render_template('index.html',userid=user_id,followers=followers)

@app.route('/graph/<name>')
def draw_graph(name):
      user_id=[]
      val=0
      whole_data = get_followers_list_server(name)
      like1,like2,like3=like_list_server(name)

      for ca in range(0,len(whole_data)):
            val=val+1
            user_id.append(val)
      # for key, value in whole_data.items() :
      #       user_id.append(key)
      #       followers.append(value)
      return render_template('graph.html',userid=user_id,followers=whole_data,l1=like1,l2=like2,l3=like3)

if __name__ == '__main__':
   app.run(debug = True)
