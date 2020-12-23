import random
import re
import numpy as np
from . import modelset, postsend
from . import var
carddict = {
    44: "♣A", 48: "♣2", 0: "♣3", 4: "♣4", 8: "♣5", 12: "♣6", 16: "♣7", 20: "♣8", 24: "♣9", 28: "♣10", 32: "♣J", 36: "♣Q", 40: "♣K",
    45: "♦A", 49: "♦2", 1: "♦3", 5: "♦4", 9: "♦5", 13: "♦6", 17: "♦7", 21: "♦8", 25: "♦9", 29: "♦10", 33: "♦J", 37: "♦Q", 41: "♦K",
    46: "♥A", 50: "♥2", 2: "♥3", 6: "♥4", 10: "♥5", 14: "♥6", 18: "♥7", 22: "♥8", 26: "♥9", 30: "♥10", 34: "♥J", 38: "♥Q", 42: "♥K",
    47: "♠A", 51: "♠2", 3: "♠3", 7: "♠4", 11: "♠5", 15: "♠6", 19: "♠7", 23: "♠8", 27: "♠9", 31: "♠10", 35: "♠J", 39: "♠Q", 43: "♠K",
}
ordersplit=['JQKA2' , '10JQKA' , '910JQK' , '8910JQ' , '78910J' , '678910' , '56789' , '45678' , '34567' , '23456' , 'A2345']
please={
    0:"單張",
    1:"對子",
    2:"順子",
    3:"葫蘆",
    4:"鐵支",
    5:"桐花順"
}
main=""
state = -2
orids=[]
center_ids = [] #have the ordered
nicknames=[]
carrand = [1,2]
number=0
order=-1
big=None
nowmode=["♣3",-2]  # node and size
def test():
    global state, carddict, center_ids,number,nicknames
    center_ids = ['1','2'] #have the ordered
    nicknames=['大繃繃','小蹦蹦']
    number=2
    state=1
    tmp = []
    for num in range(0,2):
        tmp.append(carddict[num])
    tmp.sort()
    carrand[0]=carrand[1]=tmp
    postsend.user_post(center_ids[0], "text", "♣♦♥♠")
    postsend.user_post(center_ids[0], "text", ",".join(tmp))

# ************************test code **************************
# test()

def reset(mode):
    global center_ids,nicknames,carrand,number,order,big,nowmode,orids
    if mode==-2:
        center_ids = []
        nicknames=[]
        center_ids = []
        orids=[]
        var.Gameset=None
    center_ids=orids.copy()
    carrand = []
    number=0
    order=-1
    big=None
    nowmode=["♣3",-2]  # node and size

def process(userid, reply):
    print(reply)
    global state, carddict, center_ids,number,orids,main,nicknames,order
    if reply == "退出" :         #退出遊戲
        if userid in center_ids:
            center_ids.remove(userid)
            if order> len(center_ids):
                order=0
            return[modelset.getnickname(userid)+"退出遊戲",False]
        elif main==userid:
            reset(-1)
            state = -2
            return ["遊戲結束", True]
        else:
            return False
    elif reply =="Again":       #再玩一次
        return firstcard(number)
    elif state == -2:
        state += 1
        return ["請管理員隨便打個字", False]
    elif state == -1:
        state += 1
        main=userid #set the 管理員
        return ["請輸入遊玩人數(2~4)", False]
    elif state == 0:
        number = int(reply)          
        if isinstance(number, int):
            state += 1 
            return ["請要遊玩的人說HI", False]
        else:
            return["請輸入正確數字",False]
    elif len(center_ids) < number:
        if "HI" not in reply:
            return ["要遊玩請say HI", False]
        elif userid in center_ids:
                return["您已加入了，還剩"+str(number-len(center_ids))+"位", False]
        else:
            center_ids.append(userid)
            nicknames.append(modelset.getnickname(userid))
            if len(center_ids) < number:
                return["收到，還剩"+str(number-len(center_ids))+"位", False]
            else:
                orids=center_ids.copy()
                return firstcard(number)
    else:
        return False

def firstcard(number):
    global carrand,carddict
    carrand = list(range(0, 52))
    random.shuffle(carrand)
    carrand = np.array_split(carrand, number)
    for i in range(0, number):
        tmp = []
        for num in carrand[i]:
            tmp.append(carddict[num])
        tmp.sort()
        carrand[i]=tmp
        postsend.user_post(center_ids[i], "text", "♣♦♥♠")
        postsend.user_post(center_ids[i], "text", ",".join(tmp))
    var.gamestart=True
    return["牌已發送 遊戲開始 \n梅花三先出\n(請按照張數大小輸入\n ex:♣3,♦3,♣A,♦A,♥A)", False]

def check_id(userid):
    global center_ids
    if userid not in center_ids:
        return False

def gamesection(userid,reply):
    global order,big
    if order ==-1:
        if  "♣3" in reply:      
            order=center_ids.index(userid)
            big=order
            givecard(userid,reply)
        else:
            postsend.user_post(userid, "text","請出梅花三")
    elif center_ids[order] ==userid:
        if reply =="PASS":
            now=order
            order=(order+1)%len(center_ids)
            print(big,order)
            if big==order:
                nowmode[1]=-2
            postsend.multi_post(center_ids, ["text","text"], [nicknames[now]+"PASS","下一位輪到"+nicknames[order]])
        else:
            big=order
            givecard(userid,reply)
            

    return False

def givecard(userid,reply): 
    global order,nowmode,please
    tmplist=reply.split(",")
    now=order
    print(reply)
    for item in tmplist:
        if item not in carrand[order]:
            print("???")
            postsend.user_post(center_ids[now], "text","您的手牌無"+item)
            return
            
    tmpmode=check_mode(tmplist) 
    print(tmpmode,nowmode)  
    if tmpmode[1]==-1 :
        postsend.user_post(center_ids[now], "text","您出的牌不符規定")
        return  
    elif nowmode[1]==-2 or (tmpmode[1]>3 and tmpmode[1]>nowmode[1]):
        nowmode=tmpmode
    elif nowmode[1]!=tmpmode[1]:
        postsend.user_post(center_ids[now], "text","請出"+please[nowmode[1]])
        return 
    elif nowmode[1]==tmpmode[1]:
        if get_key(nowmode[0])<get_key(tmpmode[0]):
            nowmode=tmpmode
        else:
            postsend.user_post(center_ids[now], "text","您的牌較小，無法出牌")
            return 
    tmp = list(set(carrand[order])^set(tmplist))
    carrand[order]=sorted(tmp)
    otherid = center_ids.copy()
    otherid.remove(userid) 
    order=(order+1)%len(center_ids)
    
    if carrand[now]==[]:
        postsend.user_post(center_ids[now], "text","你是第"+str(number-len(center_ids)+1)+"名")
        if len(center_ids)-1==1:
                postsend.multi_post(center_ids, ["text","text"], [nicknames[now]+"出了"+reply+"贏了","遊戲結束","退出輸入:退出\n再一次輸入:Again\n"])
        else:
            postsend.multi_post(otherid, ["text","text"], [nicknames[now]+"出了"+reply+"贏了",\
            "下一位輪到"+nicknames[order]])
        center_ids.remove(userid) #remove the id from others
        nicknames.remove(nicknames[now])
    else:
        print(otherid)
        postsend.user_post(center_ids[now], "text",",".join(carrand[now]))
        postsend.multi_post(otherid, ["text","text"], [nicknames[now]+"出了"+reply,\
            "下一位輪到"+nicknames[order]])
       
            

def get_key(val):
    global carddict
    for key, value in carddict.items():
         if val == value:
             return key
    return "key doesn't exist"
        
def check_mode(outlist):
    print(outlist)
    global ordersplit,nowmode
    if len(outlist)==1:
        return [outlist[0],0]        #single 
    elif len(outlist)==2:
        num1=outlist[0][1:]
        num2=outlist[1][1:]
        if num1==num2:
            return [outlist[1],1]        #pay
        else:
            return ["no",-1]
    elif len(outlist)==5:
        tmpnum={}
        tmpflower={}
        checkorder=""
        for item in outlist:
            num=item[1:]
            checkorder+=num
            if num not in tmpnum:
                tmpnum[num]=0
                print(item[:1],num)
            if item[:1] not in tmpflower:
                 tmpflower[item[:1]]=0
            tmpnum[num]+=1
            tmpflower[item[:1]]+=1
        if len(tmpnum)==5:  
            if checkorder in ordersplit:
                if len(tmpflower)==1:
                    return [outlist[4],5]  #桐花順
                else:           #順子
                    return [outlist[4],2]
            else:
                return -1
        elif len(tmpnum)==2:
            for key,value in tmpnum.items():
                if value==4 or value==1:
                    return [outlist[4],4]    #tigi
                else:
                    return [outlist[4],3]    #盧
    return ["no",-1]