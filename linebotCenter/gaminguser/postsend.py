import requests
import json
from django.conf import settings
API_personurl = "https://api.line.me/v2/bot/message/push"
API_multiurl = "https://api.line.me/v2/bot/message/multicast"




def send_to_person(id, backmode, text):
    data = {
        "to": id,
        "messages": [
            {
                "type": backmode,
                "text": text
            },
            # {
            #     "type": "sticker",
            #     "packageId": "1",
            #     "stickerId": "3"
            # }
        ]
    }

    headers = {
        'Authorization': 'Bearer '+settings.USER_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    requests.post(API_personurl, data=json.dumps(data), headers=headers)
