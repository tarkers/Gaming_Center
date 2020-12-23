from .models import MemberData

#create the group id from center
def createdata(ud, dn):
    check = MemberData.objects.filter(userid=ud).exists()
    if check == False:
        print(dn)
        MemberData.objects.create(userid=ud, displayname=dn)
        return "請加Gaming_user為好友~"
    else:
        data = MemberData.objects.filter(userid=ud)
        data.update(displayname=dn)


def firstconnect(ud,dn):
    if not MemberData.objects.filter(userid=ud).exists() \
        or  MemberData.objects.filter(displayname=dn)[0].nickname=="":
        return "已加入好友，修改輸入暱稱，格式(**暱稱)"
    else:
        data = MemberData.objects.filter(userid=ud)
        data.update(displayname=dn)
        nickname =data.nickname
        return "已有名稱為"+nickname+"修改暱稱，格式(**暱稱)"

def checkexists(kind,name):
    return MemberData.objects.filter(kind=name).exists()


def updatedn(ud, nn):
    if MemberData.objects.filter(nickname=nn) \
        and MemberData.objects.filter(nickname=nn)[0].userid !=ud:
        return "名字已被擁有，請再想一個"
    else:
        data = MemberData.objects.filter(userid=ud)
        data.update(nickname=nn)
        return "您的暱稱改為: "+nn

def deluser(ud):
    data=MemberData.objects.filter(userid=ud)[0]
    data.delete()



def getnickname(ud):
    data = MemberData.objects.get(userid=ud)
    nickname = data.nickname
    return nickname

def useridget():
    return 11
