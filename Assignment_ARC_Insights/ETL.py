#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import json
import time


# #  Ingesting Data Using An API

# In This our goal is to extract the available data stock news on polygon.ai
# 
# <br> Step 1:  we will look for the endpoint -api (https://polygon.io/docs/stocks/get_v2_reference_news) that provides the data we need. In the case of news extraction, it appears that the GET /v3/reference/news endpoint fits our task.
# 
# <br> Step 2: we are defining the parameters which are required for the below extraction function. However, due to the 1,000 ticker limit per page, we are using the next_url response attribute to obtain the next page of information

# In[2]:


from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(1)
yest_date = datetime.strftime(yesterday, '%Y-%m-%d')


# In[3]:


def return_commonstock_tickers(token, initial_load=False):
    url = 'https://api.polygon.io/v2/reference/news'
#     ticker=AAPL&published_utc.lte=2022-07-01&apiKey=Oqpqg_khSPFkn0cXejujjGR9VBDp13bu
    # taking yesterdays date for using in our inc load 
    yesterday = datetime.now() - timedelta(1)
    yest_date = datetime.strftime(yesterday, '%Y-%m-%d')

    published_utc ="1900-01-01" if  initial_load else yest_date
    print("published_utc::", published_utc)
    parameters = {
        'apiKey': token, # your API key
        'ticker': 'AAPL', # query common stocks
        'published_utc.gte': published_utc,
        'limit': 500 # extract max data possible
    }

    try:
        tickers_json = requests.get(url, parameters).json()
        tickers_list = tickers_json['results']
        if 'next_url' not in tickers_json.keys():
            return tickers_list
#         print(tickers_json['next_url'])
        next_url = tickers_json['next_url'] if tickers_json['next_url'] else None
#         print(next_url)
        while next_url:
            tickers_json = requests.get(tickers_json["next_url"], parameters).json()
            tickers_list.extend(tickers_json["results"])
            if 'next_url' not in tickers_json.keys():
                break
            # trigger a wait since free tier is limited to 5 calls/min
            time.sleep(12)
            
    except Exception as e:
        print(e)
        return None
    
    return tickers_list


# #  Write Data into CSV or Text file
# 
# <br> here we are first calling our extraction function which is created above and initialize a variable with the returned data. To write out as a CSV file, the response must be converted into a Pandas DataFrame then utilize the .to_csv() method.
# 
# <br> Apart from our API Token we are also passing True or flase flag. True indicates for the full load of the data where are False flag indicates the inc load 

# In[4]:


token = 'Oqpqg_khSPFkn0cXejujjGR9VBDp13bu'

#True for initial load and False for inc loads
tickers = return_commonstock_tickers(token, False)

print(tickers)
# write out as csv
df_cs_tickers = pd.DataFrame(tickers)
df_cs_tickers.to_csv('polygon_stock_news.csv', index = False)

# # write out as txt
# with open('polygon_cs_tickers_1.txt', 'w') as outfile:
#     json.dump(tickers, outfile, indent=4)


# In[5]:


data = pd.read_csv("polygon_stock_news.csv")
data.head() 


# In[6]:


news_df = data[["id","title","author","published_utc", "keywords"]].copy()
news_df.head()


# In[7]:


len(news_df)


# In[8]:


news_df = news_df.fillna("NoData")


# In[9]:


Id_list ="','".join(news_df['id'])
#"select '" + Id_list + '\'from'
#type(Id_list)


# In[10]:


# "DELETE FROM stock_news WHERE id in ('"+Id_list+"')"


# In[11]:


# mydata.head()


# In[12]:


# data.info()


# # Loading the ingested data into MySql server 

# <br> Here we are conneting to local mysql server giving required parameters as below and then creating the database

# In[13]:


import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',  
                        password='Qwerty@123')#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS stock")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)


# In[14]:


news_df.columns


# <br> In this section we are creating the structure of the table with the required attributes and doing delete and insert operation 

# In[15]:


# import mysql.connector as msql
# from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', database='stock', user='root', password='Qwerty@123')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS stock_news;')
        print('Creating table....')
# in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE stock_news(id varchar(255),title varchar(1000),author varchar(255),published_utc varchar(255),keywords varchar(1000))")
        print("Table is created....")
        #loop through the data frame
        sql1 = "DELETE FROM stock_news WHERE id in ('"+Id_list+"')"
        #print(sql1)
        cursor.execute(sql1)
        conn.commit()
        for i,row in news_df.iterrows():
            #here %S means string values 
            
            #print("No of records deleted: ", len())
            sql2 = "INSERT INTO stock.stock_news VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql2, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)


# In[16]:


# Execute query
sql = "SELECT * FROM stock.stock_data"
cursor.execute(sql)
# Fetch all the records
result = cursor.fetchall()
for i in result:
    print(i)


# In[ ]:





# In[ ]:




