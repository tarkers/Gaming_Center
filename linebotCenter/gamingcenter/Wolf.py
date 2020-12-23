import random
from enum import Enum
from . import modelset,postsend,var
from threading import Thread, Event
import time

night_event = Event()
 
state = -2
daystate=0   #遊戲步驟
ppl_role = []
original_role=[]
center_ids = []
wolf_ids=[]
number = 0
main=""
clock=False
nightnubmer=0
totalnightnumber=0
nicknames=[]
vote={}
save=""
votenum=0
kill_list=[]

nightgodteam=["預言家","女巫","守衛"]#"白痴","守衛","騎士"]
wolfteam=["狼人","狼王","白狼王","狼美人","雪狼"]

def test():
    global number,nicknames,center_ids,state,wolfteam,wolf_ids,nightgodteam,totalnightnumber,original_role
    center_ids = ['1','2','3']#,'4','5']
    nicknames=['大蹦蹦','小蹦蹦','阿嬤救我']#,'叫什麼阿姨，叫姊姊','吉為服飾定']
    number=3
    state=2
    reply="狼人X1 平民X1 預言家X1"
    tmprole=reply.split()
    for tmp in tmprole:
        data =tmp.split('X')
        num=int(data[1])
        for _ in range(0,num):
            ppl_role.append(data[0])
    random.shuffle(ppl_role)
    print(ppl_role)
    print(nicknames)
    original_role=ppl_role.copy()
    for i in range(0, number):
        if ppl_role[i] in wolfteam:
            wolf_ids.append(center_ids[i])
        elif ppl_role[i] in nightgodteam:
            totalnightnumber+=1
        # postsend.user_post("userid", "text", ppl_role[i])
# test()

def reset():
    global state,daystate,ppl_role,original_role,center_ids,wolf_ids,number,main,clock,nightnubmer,totalnightnumber,\
        nicknames,vote,save,votenum,kill_list
    var.Gameset=None
    state = -2
    daystate=0   #daystate
    ppl_role = []
    original_role=[]
    center_ids = []
    wolf_ids=[]
    number = 0
    main=""
    clock=False
    nightnubmer=0
    totalnightnumber=0
    nicknames=[]
    vote={}
    save=""
    votenum=0
    kill_list=[]

def process(userid, reply):
    
    global state, ppl_role, number, center_ids,main
    if state == -2:
        state += 1
        main=userid #set the 管理員
        return ["請管理員隨便打個字", False]
    elif state == -1:
        state += 1
        return ["請輸入遊玩人數", False]
    elif state == 0:
        number = int(reply)   
        if isinstance(number, int):
            state += 1
            return ["請要遊玩的人說HI，第一個say HI的是管理員", False]
        else:
            return["請輸入正確數字",False]
    elif len(center_ids) < number:
        if userid in center_ids:
            return["您已加入了，還剩"+str(number-len(center_ids))+"位", False]
        else:
            center_ids.append(userid)
            if len(center_ids)== number:
                return["管理員請輸入角色數量\n ex:[狼人X1 平民X3 預言家X1]", False]
            else:
                return["收到，還剩"+str(number-len(center_ids))+"位", False]   
    elif state == 1:
        state+=1
        namelist=""
        tmprole=reply.split()
        for tmp in tmprole:
            data =tmp.split('X')
            num=int(data[1])
            for i in range(0,num):
                ppl_role.append(data[0])
        random.shuffle(ppl_role)
        for i in range(0, number):
            nickname = modelset.getnickname(center_ids[i])
            namelist+=nickname+"\n"
            postsend.user_post(userid, "text", ppl_role[i])
        return["角色已送出可開始發言，請各位確認自己的角色\n人物有:\n"+namelist, False]
    elif state==2:#test code
        print("into state")
        namelist=""
        state+=1
        for i in range(0, number):
            namelist+="\n"+nicknames[i]
        return["角色已送出可開始發言\n請各位確認\n-----------\n公民名字:"+namelist, False]
    return False
# def firstcard(number):

def gamesection(userid,reply):
    global daystate,nightnubmer,clock,wolfteam,wolf_ids,votenum,vote,nightgodteam,kill_list,original_role,totalnightnumber,\
        number
    index = center_ids.index(userid)
    role=ppl_role[index]
    if daystate==0:
        if not clock:
            clock=True
            action_thread = Thread(target=dayandnight)
            action_thread.start()
        if role=="kill":
            ppl_role[index]="die"
            postsend.multi_post(center_ids, ["text"], [nicknames[index]+"遺言:"+reply])
        else:
            postsend.multi_post(center_ids, ["text"], [nicknames[index]+": "+reply])
    elif daystate ==1:
        if "==" in reply:
            reply=reply.replace("==","")
            if reply not in nicknames:
                postsend.user_post(userid, "text", "沒有此人喔") 
            else:
                votenum+=1
                if reply not in vote:
                    vote[reply]=1
                else:
                    vote[reply]+=1
                if votenum==number:
                    die = max(vote, key=vote.get)
                    daystate=2
                    nightnubmer=0
                    votenum=0
                    vote={}
                    index =nicknames.index(die)
                    if ppl_role[index] in nightgodteam:
                        totalnightnumber-=1
                    elif ppl_role[index] in wolfteam:
                        wolf_ids.remove(center_ids[index])
                    ppl_role[index]="kill"
                    number-=1
                    if not checkwin(die+"已被放逐"):
                        postsend.user_post(center_ids[index], "text", askquestion('kill'))
                        postsend.multi_post(center_ids, ["text","text"], [die+"已被放逐","夜晚降臨，狼人請討論"])
                else:
                    postsend.multi_post(center_ids, ["text"], [reply+"多一票"])
    elif daystate==2:
        if role not in wolfteam and role not in nightgodteam:
            postsend.user_post(userid, "text", "現在是夜晚，閉嘴")
        elif role in wolfteam:
            if "==" in reply:        
                reply =reply.replace("==","")
                if reply not in nicknames:
                    postsend.user_post(userid, "text", "沒有此人喔")
                    return
                votenum+=1
                if reply not in vote:
                    vote[reply]=1
                else:
                    vote[reply]+=1
                if votenum==len(wolf_ids):
                    die = max(vote, key=vote.get)
                    killresult(die,0)
                    daystate=3
                    nightnubmer=0
                    votenum=0
                    vote={}
                    postsend.multi_post(center_ids, ["text"], ["夜晚神職人員出動"])
                    for role in nightgodteam:
                        if role in ppl_role:
                            index =ppl_role.index(role)
                            if role =="女巫":
                                postsend.user_post(center_ids[index], "text", die+"即將被殺")     
                            postsend.user_post(center_ids[index], "text", askquestion(role))     
                else:
                    postsend.multi_post(wolf_ids, ["text"], [reply+"多一票"])
            else:      
                postsend.multi_post(wolf_ids, ["text"], [nicknames[index]+": "+reply])
    elif daystate==3 and "==" in reply:
        reply =reply.replace("==","")
        if role =="預言家":   
            if reply not in nicknames:
                postsend.user_post(userid, "text", "沒有此人喔")
                return
            nightnubmer+=1 
            index = nicknames.index(reply)
            postsend.user_post(userid, "text", reply+"是"+ppl_role[index])
        elif role =="守衛":
            if reply not in nicknames:
                postsend.user_post(userid, "text", "沒有此人喔")
                return
            nightnubmer+=1 
            index = nicknames.index(reply)
            postsend.user_post(userid, "text", "你拯救的是"+ppl_role[index])
            killresult(ppl_role[index],1)
        elif role =="女巫":
            nightnubmer+=1 
            if "毒殺_" in reply:
                killresult(ppl_role[index],0)
                postsend.user_post(userid, "text", "你毒殺了"+ppl_role[index])
            elif "救贖_" in reply:
                killresult(ppl_role[index],1)
                postsend.user_post(userid, "text", "你救贖了"+ppl_role[index])
        if nightnubmer==totalnightnumber:
            daystate=0
            nightnubmer=0
            if len(kill_list)==0:
                postsend.multi_post(center_ids, ["text","text"], ["無人死亡","進入白天"])
            else:
                for nn in kill_list:
                    index =nicknames.index(nn)
                    if ppl_role[index] in nightgodteam:
                        totalnightnumber-=1
                    elif ppl_role[index] in wolfteam:
                        wolf_ids.remove(center_ids[index])
                    ppl_role[index]="kill"
                    number-=1  
                    if not checkwin(nicknames[index]+"被殺了"):
                        postsend.multi_post(center_ids, ["text","text"], [nicknames[index]+"被殺了","進入白天"])
                        postsend.user_post(center_ids[index], "text", askquestion('kill'))                                                          
                kill_list=[]
        

def checkwin(line):
    global ppl_role,wolfteam,center_ids,nicknames,original_role
    haswolf=False
    hasgood=False
    mode=0
    for ppl in ppl_role:
        if ppl !="die" and ppl !='kill':
            print(ppl)
            if ppl in wolfteam:
                haswolf=True
            else:
                hasgood=True
    if haswolf and hasgood:
        mode=0
    elif hasgood:
        mode="好人陣隊贏了"
    else:
        mode="狼人陣隊贏了" 
    print(mode)
    if mode!=0:       #end of the game
        truth=""
        for i in range(0,len(center_ids)):
            truth+="\n"+nicknames[i]+":"+original_role[i]
        postsend.multi_post(center_ids, ["text"], [line])
        postsend.multi_post(center_ids, ["text","text","text"], [mode,"遊戲結束","真相公布:"+truth])
        reset()
        return True
    else:
        return False
    
def askquestion(role):
    question = {
        "ALL"   : "請討論要放逐的人，決定好請打上(==要放逐的名字)",
        "狼人" : "請討論你要殺的人，決定好請打上(==要殺的名字)",
        "kill" : "請在白天說出你的遺言",
        "預言家" :"選擇想查驗的人,打上(==發動的名字)",
        "女巫" : "毒殺or救贖誰(方式ex:==毒殺_發動的名字)",
        "獵人" : "是否要淘汰誰,,打上(==發動的名字)",
        "騎士" : "要跟誰決鬥,打上(==發動的名字)",
        "守衛" : "你要守護誰,打上(==發動的名字)",
        "黑狼王":"你想淘汰誰,打上(==發動的名字)",
        "白狼王":"你想自爆淘汰誰,打上(==發動的名字)",
        "狼美人":"你想魅惑誰,打上(==發動的名字)",
    }
    return question[role]



def killresult(person,mode):
    global save, kill_list
    if mode==0:
        kill_list.append(person)
    elif mode==1 and person in kill_list:
            save=""
            kill_list.remove(person)


def dayandnight():
    global center_ids,daystate,clock,ppl_role
    i = 0
    while True:
        i += 1
        time.sleep(1)
        if i==3:        #set the daystate  speak time
            night_event.set()
            daystate=1
            clock=False
            print("16546")
            # postsend.multi_post(center_ids, ["text"], ["夜晚降臨，狼人請討論"])
            postsend.multi_post(center_ids, ["text"], [askquestion("ALL")])
            break
 