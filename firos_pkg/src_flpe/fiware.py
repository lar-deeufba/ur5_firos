# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 21:37:35 2019

@author: IapichinoIntellimech
"""
import json
import requests

head = {"Content-Type": "application/json"}
class OrionClient:
    def __init__(self, host, port=1026):
        self.host=host
        self.port=port

    def createEntity(self, data):
        jsonData = json.dumps(data)

        url = 'http://'+self.host+':'+str(self.port)+'/v2/entities'
        response = requests.post(url, data=jsonData, headers=head)
        print(response)
        try:
            print(response.json())
        except Exception:
            pass


    def queryEntity(self, entity):
        url = 'http://'+self.host+':'+str(self.port)+'/v2/entities/'+ entity
        response = requests.get(url)
        print(response.text)
        #'http://'+host+':1026/v2/entities/Room1?options=values&attrs=temperature,pressure'

    def updateEntity(self,entity,data, force=False):
        jsonData = json.dumps(data)
        if force:
            url = 'http://'+self.host+':'+str(self.port)+'/v2/entities/'+ entity+'/attrs?options=forcedUpdate'
        else:
            url = 'http://'+self.host+':'+str(self.port)+'/v2/entities/'+ entity+'/attrs'
        response = requests.post(url, data=jsonData, headers=head)
        print(response)
        try:
            print(response.json())
        except Exception:
            pass


    def subscription(self,entityType):
        data = {
          "orionUrl": 'http://orion:1026/v2',
          "quantumleapUrl":'http://quantumleap:8668/v2',
          "entityType": entityType
        }

        url = 'http://'+self.host+':8668/v2/subscribe'
        response = requests.post(url,params=data)
        print(response)
        try:
            print(response.json())
        except json.decoder.JSONDecodeError:
            pass

    def getEntities(self, entityType=None):
        if entityType is None:
            url = 'http://'+self.host+':'+str(self.port)+'/v2/entities'
        else:
            url = 'http://'+self.host+':'+str(self.port)+'/v2/entities?type='+entityType
        response = requests.get(url)
        print(response.text)