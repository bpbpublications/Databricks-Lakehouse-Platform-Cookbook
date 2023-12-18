#!/usr/bin/env python
# coding: utf-8

# In[11]:


import socket
import requests
import json
import datetime
import time
import calendar


# In[12]:


from configparser import ConfigParser
parser = ConfigParser()
_ = parser.read('notebook.cfg')
eventHubConnectString = parser.get('GetISPInfo_Notebook','eventHubConnectString')
eventhub_name ="ispinfo"


# In[13]:


sleepMinutes =10


# In[14]:



def GetTimestamp():
    gmTime= time.gmtime()    
    now = calendar.timegm( gmTime)
    print("GetTimestamp",now,gmTime)
    return now


# In[15]:


def GetISPInfo():
    ipUrl = "http://ip-api.com/json"
    response= json.loads(requests.get(ipUrl).content)
    print(response)
    print(response["query"])
    return response


# In[16]:


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


# In[ ]:


import time
print("ready to start work")
linesToWrite = []
while (True):  
    try:
        ip = socket.gethostbyname(socket.gethostname())
        now = GetTimestamp()
        ispInfo= GetISPInfo()
        print(now,ispInfo)
    except  Exception as ex:
        print("exception",ex)
        now = GetTimestamp()
        ispInfo = None
        ip = socket.gethostbyname(socket.gethostname())
    eventData = json.dumps( {"utc":now,"ip":ip,"ispInfo":ispInfo})
    SendToEventHub(eventData)
    print("sent to event hub",eventData)
    if sleepMinutes>0:
        print('sleeping',sleepMinutes)
        time.sleep(sleepMinutes * 10) # time.sleep takes seconds as parameter


# In[ ]:




