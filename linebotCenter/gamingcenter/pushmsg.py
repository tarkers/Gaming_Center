from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackTemplateAction,
    DatetimePickerTemplateAction,
)


def gamechoice():
    template = TemplateSendMessage(
        alt_text='choodse the Game',
        template=ButtonsTemplate(
            title="遊戲主選單",
            text=('請選擇您想遊玩的遊戲'),
            actions=[
                 PostbackTemplateAction(
                     label='數字炸彈',
                     text='遊玩數字炸彈',
                     data='Bomb',

                 ),
                PostbackTemplateAction(
                     label='大老二',
                     text='遊玩大老二',
                     data='BigTwo',

                 ),
                PostbackTemplateAction(
                     label='狼人殺',
                     text='遊玩狼人殺',
                     data='Wolf'
                 ),
            ]
        )
    )
    return template
