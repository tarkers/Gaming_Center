from . import BigTwo,Wolf,var

def user_response(userid,reply):
    if  var.Gameset=="BigTwo":
        if BigTwo.check_id(userid)==False:
            return
        else:
            BigTwo.gamesection(userid,reply)
    elif var.Gameset =="Wolf":
        Wolf.gamesection(userid,reply)