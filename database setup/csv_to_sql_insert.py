import mysql.connector 
f=open('','r')

def csvfile(f):
    s=0
    for i in f:
        s=s+1
        if s<12211:#no. of rows in  file
            server(i.split(','),s)
        else:
            break
connection = mysql.connector.connect(host='localhost',
                             database='SocialBlade',
                             user='root',
                             password='root@123')
def server(row,s):
    # 35622,805,457,284,Abhishekjha09 #sample insert data
    data=[]
    print(s)
    if connection.is_connected():
       db_Info = connection.get_server_info()
       
       cursor = connection.cursor()
       cursor.execute('''
       Insert into Tracker (followers,like1,like2,like3,userid) values (%s, %s, %s,%s,%s)''',(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4].replace('\n',''))))#row
    #    record = cursor.fetchone()
       connection.commit()
    else:
        print("There is a problem with connection!!!")

csvfile(f)