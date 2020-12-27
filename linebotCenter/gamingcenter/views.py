from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from . import(
    Bomb,
    BigTwo,
    Wolf,
    var,
    postsend,
    modelset
)
from linebot.models import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    JoinEvent,
    MemberJoinedEvent,
    TextSendMessage,
    ImageSendMessage
)

from .pushmsg import (
    gamechoice
)


import json
line_bot_api = LineBotApi(settings.GROUP_CHANNEL['LINE_CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(settings.GROUP_CHANNEL['LINE_CHANNEL_SECRET'])


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

            if isinstance(event, PostbackEvent):
                reply = event.postback.data
                var.Gameset = reply
              #  print(reply)
            elif isinstance(event, MessageEvent):  # 如果有訊息事件
                print(event.source.user_id)
                reply = event.message.text
                result=False
                if var.Gameset == None and reply.rstrip() == "menu":     # user check the game mode
                    line_bot_api.reply_message(
                        event.reply_token,
                        gamechoice()
                    )
                elif var.Gameset ==None:
                    if reply=="fsm":
                        line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url='https://i.imgur.com/TFwXPnh.png', preview_image_url='https://i.imgur.com/TFwXPnh.png')
                    )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="輸入menu可進入選單"),
                        )
                else:
                    if var.Gameset == "Bomb":
                        result = Bomb.process(event.source.user_id,reply)
                    elif var.Gameset == "BigTwo":
                        result = BigTwo.process(event.source.user_id,reply)                
                    elif var.Gameset =="Wolf":   
                        result = Wolf.process(event.source.user_id,reply)
                    if result!=False and type(result) is list:
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token, [
                                TextSendMessage(text=result[0]),
                            ]
                        )       
                        if result[1] == True:
                            var.Gameset = None
                # # else:
                #     # modelset.get_user_id(event.source.user_id)
                #     # postsend.user_post(event.source.user_id,1,"123")
                #     result = postsend.groupprofile(event.source.user_id)
                #     # print(result)
                #     # modelset.createdata(event.source.user_id,"te")
                #     # postsend.user_post("Ufda97cb77d9cfc59f5e8565a99e74c83","text","testcodesend")
                #     # line_bot_api.reply_message(  # 回復傳入的訊息文字
                #     #     event.reply_token, [
                #     #         TextSendMessage(text=result),
                #     #     ]
                #     # )
            # elif isinstance(event,UnfollowEvent):
            #     print(123456)
            elif isinstance(event, MemberJoinedEvent) or isinstance(event,FollowEvent):
                # save the user id into models
                welcome = postsend.groupprofile(event.source.user_id)
                print(welcome)
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    [
                        TextSendMessage(text=welcome),
                        TextSendMessage(text='https://lin.ee/0wV3Kd4')
                    ]
                )
            elif isinstance(event, JoinEvent):
                print(event)
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    {
                        TextSendMessage(text=welcome),
                    }
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
