import requests
import json
from django.conf import settings
from . import modelset,var

API_personurl = "https://api.line.me/v2/bot/message/push"
API_multiurl = "https://api.line.me/v2/bot/message/multicast"
API_PROFILE="https://api.line.me/v2/bot/profile/"


def groupprofile(userid):
    profile_data = {'Authorization': 'Bearer ' + settings.GROUP_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN']}
    profile = requests.get(API_PROFILE+ userid, headers=profile_data)
    
    tmpdn=profile.json()['displayName']
    reply =modelset.createdata(userid,tmpdn)
    print(tmpdn)
    return reply

#test
def user_post(userid, backmode, text):
    data = {
        "to": 'U6f785ac264021840cba6bb56b334b95d',#userid,
        "messages": [
            {
                "type": "text",
                "text": text
            },
        ]
    }
    headers = {
        'Authorization': 'Bearer '+settings.USER_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    requests.post(API_personurl, data=json.dumps(data), headers=headers)

def multi_post(userlist,backmode,text):
    #test 
    userlist=[]
    userlist.append('U6f785ac264021840cba6bb56b334b95d')
    data={}
    data["to"]=userlist
    data["messages"]=[]
    for i in range(0, len(backmode)): 
        tmp={}
        tmp["type"]=backmode[i]
        tmp["text"]=text[i]       
        data["messages"].append(tmp)
    headers = {
        'Authorization': 'Bearer '+settings.USER_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    requests.post(API_multiurl, data=json.dumps(data), headers=headers)

def userleave(userid):
    modelset.deluser(userid)


