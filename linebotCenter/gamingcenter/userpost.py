import requests
from . import BigTwo,Wolf,var,modelset
from django.conf import settings

API_PROFILE="https://api.line.me/v2/bot/profile/"

def userprofile(userid):
    profile_data = {'Authorization': 'Bearer ' + settings.USER_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN']}
    profile = requests.get(API_PROFILE+ userid, headers=profile_data)
    tmpdn=profile.json()['displayName']
    print(tmpdn)
    reply =modelset.firstconnect(userid,tmpdn)
    return reply


def changename(userid,name):
    reply =modelset.updatedn(userid,name)
    return reply
def user_response(userid,reply):
    if reply =="我的名字":
        return modelset.getnickname(userid)
    elif  var.Gameset=="BigTwo":
        if BigTwo.check_id(userid)==False:
            return
        else:
            BigTwo.gamesection(userid,reply)
    elif var.Gameset =="Wolf":
        print(userid,reply)
        Wolf.gamesection(userid,reply)