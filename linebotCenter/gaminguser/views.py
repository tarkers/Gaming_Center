from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    FollowEvent,
    UnfollowEvent,
    TextSendMessage
)
from gamingcenter import userpost
line_bot_api = LineBotApi(settings.USER_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(settings.USER_CHANNEL['LINE_CHANNEL_SECRET'])


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, FollowEvent):
                response = userpost.userprofile(event.source.user_id)
                print(response)
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=response)
                )
            elif isinstance(event, MessageEvent):  # 如果有訊息事件
                reply = event.message.text
                if "**" in reply:
                    reply=reply.replace("*","")
                    response=userpost.changename(event.source.user_id,reply)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=response)
                    )
                else:
                    reply =reply.split(" ")
                    # postsend.user_response(event.source.user_id,reply)
                    userpost.user_response(reply[0],reply[1])
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
