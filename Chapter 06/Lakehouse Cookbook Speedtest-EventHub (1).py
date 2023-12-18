#!/usr/bin/env python
# coding: utf-8

# In[1]:


from configparser import ConfigParser
parser = ConfigParser()
_ = parser.read('notebook.cfg')
eventHubConnectString = parser.get('my_Notebook','eventHubConnectString')


# In[2]:


# pip install azure-eventhub


# In[3]:


eventhub_name = 'speedtest'
sleepMinutes = 10


# In[ ]:





# In[4]:


# pip install speedtest-cli


# In[5]:


import os
import speedtest 


# In[6]:


import socket
import requests
import json


# In[ ]:





# In[7]:


def test():
    s = speedtest.Speedtest()
    ip = socket.gethostbyname(socket.gethostname())
    ipUrl = "https://api.ipify.org/?format=json"
    response= json.loads(requests.get(ipUrl).text)
    print(response)
    print(response["ip"])
    externalIp = response["ip"]
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    return res["download"], res["upload"], res["ping"],externalIp


# In[8]:


import datetime
import time


# In[9]:


from azure.eventhub import EventHubProducerClient, EventData
def SendToEventHub(data):
    try:
        print("enter SendToEventHub", data)
        client = EventHubProducerClient.from_connection_string(eventHubConnectString, eventhub_name=eventhub_name)
        event_data_batch = client.create_batch()
        event_data_batch.add(EventData(data))
        with client:
            client.send_batch(event_data_batch)
        print("Sent data")
    except Exception as e:
        print("Unable to send data to event hub",e)


# In[10]:


import time
import calendar
def GetTimestamp():
    gmTime= time.gmtime()    
    now = calendar.timegm( gmTime)
    print("GetTimestamp",now,gmTime)
    return now


# In[ ]:


import time
print("ready to start work")
linesToWrite = []
while (True):  
    try:
        now = GetTimestamp()
        d, u, p,ip = test()
        print(d,u,p,ip)
    except  Exception as ex:
        print("exception",ex)
        d = -1
        u = -1
        p = -1
        ip = socket.gethostbyname(socket.gethostname())
    eventData = json.dumps( {"utc":now,"ip":ip,"download":d,"upload":u,"ping":p})
    SendToEventHub(eventData)
    print("sent to event hub")
    if sleepMinutes>0:
        print('sleeping',sleepMinutes)
        time.sleep(sleepMinutes * 10) # time.sleep takes seconds as parameter


# In[ ]:




