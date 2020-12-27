import random
from enum import Enum
from . import modelset, postsend, var
from threading import Thread, Event
import time

night_event = Event()

state = 1
gamestate = 0
center_ids = {}
wolf_ids = []
role_data = {}
canvote = 0
votenum = 0
nightskillnum = 0
t_nightskillnum = 0
main = ""
kill = ""
witchkill = ""
shouldkill = False
dayclock = False
vote = {}
skillactive=False
endgame=False
halt=False

def initial_role(role):
    rolelist = {
        "平民": {
            "userid": "",
            "role": "平民",
            "die": 0,
            "nightskill": False,
            "lastspeak": True,
            "vote": False
        },
        "預言家": {
            "userid": "",
            "role": "預言家",
            "die": 0,
            "nightskill": True,
            "lastspeak": True,
            "vote": False
        },
        "女巫": {
            "userid": "",
            "role": "女巫",
            "die": 0,
            "nightskill": True,
            "onetimeskill": {
                "poison": True,
                "save": True,
            },
            "lastspeak": True,
            "vote": False
        },
        "獵人": {
            "userid": "",
            "role": "獵人",
            "die": 0,
            "nightskill": False,
            "onetimeskill": True,
            "lastspeak": True,
            "vote": False
        },
        "白痴": {
            "userid": "",
            "role": "白痴",
            "die": 0,
            "nightskill": False,
            "onetimeskill": True,
            "lastspeak": True,
            "canvote": True,
        },
        "守衛": {
            "userid": "",
            "role": "守衛",
            "die": 0,
            "nightskill": True,
            "lastspeak": True,
            "people": "",
            "vote": False
        },
        "騎士": {
            "nightskill": False,
            "userid": "",
            "role": "騎士",
            "die": 0,
            "lastspeak": True,
            "people": "",
            "vote": False
        },
        "狼人": {
            "nightskill": False,
            "userid": "",
            "role": "狼人",
            "die": 0,
            "lastspeak": True,
            "vote": False
        },
    }
    return rolelist[role]


def test():
    global center_ids, canvote, role_data, state, t_nightskillnum, wolf_ids
    wolf_ids = ["1"]
    t_nightskillnum = 2
    state = 2
    canvote = 4
    center_ids = {"1": "我是阿罵", "2": "2", "3": "3","4": "pp"}
    role_data = {
       "吉到底": {
            "userid": "1",
            "role": "平民",
            "die": 0,
            "nightskill": False,
            "lastspeak": True,
            "vote": False
        },
        "covid-19": {
            "userid": "2",
            "role": "預言家",
            "die": 0,
            "nightskill": True,
            "lastspeak": True,
            "vote": False
        },
        "阿姨不努力了": {
            "userid": "3",
            "role": "女巫",
            "die": 0,
            "nightskill": True,
            "onetimeskill": {
                "poison": True,
                "save": True,
            },
            "lastspeak": True,
            "vote": False
        },
        "你瘋了": {
            "userid": "4",
            "role": "獵人",
            "die": 0,
            "nightskill": False,
            "onetimeskill": True,
            "lastspeak": True,
            "vote": False
        },
        "我是白痴": {
            "userid": "5",
            "role": "白痴",
            "die": 0,
            "nightskill": False,
            "onetimeskill": True,
            "lastspeak": True,
            "canvote": True,
        },
        "David": {
            "userid": "6",
            "role": "守衛",
            "die": 0,
            "nightskill": True,
            "lastspeak": True,
            "people": "",
            "vote": False
        },
        "騎士": {
            "nightskill": False,
            "userid": "7",
            "role": "騎士",
            "die": 0,
            "lastspeak": True,
            "people": "",
            "vote": False
        },
        "wolf": {
            "nightskill": False,
            "userid": "8",
            "role": "狼人",
            "die": 0,
            "lastspeak": True,
            "vote": False
        },
    }
    # truth = ""
    # for key, value in role_data.items():
    #     truth += "\n"+key+":"+value["role"]
    # print(truth)
# ************************test code **************************
# test()


def process(userid, reply):
    global state, role_data, canvote, center_ids, main, wolf_ids, nightskill, t_nightskillnum
    if state == -2:
        state += 1
        main = userid  # set the 管理員
        return ["請管理員隨便打個字", False]
    elif state == -1:
        state += 1
        return ["請輸入遊玩人數", False]
    elif state == 0:
        canvote = int(reply)
        if isinstance(canvote, int):
            state += 1
            return ["請要遊玩的人說HI", False]
        else:
            return["請輸入正確數字", False]
    elif len(center_ids) < canvote:
        if userid in center_ids:
            return["您已加入了，還剩"+str(canvote-len(center_ids))+"位", False]
        else:
            center_ids[userid] = modelset.getnickname(userid)
            if len(center_ids) == canvote:
                return["管理員請輸入角色數量\n ex:狼人x1 平民x3 預言家x1\n(以空格分開)", False]
            else:
                return["收到，還剩"+str(canvote-len(center_ids))+"位", False]
    elif state == 1:
        # if userid != main:
        #     return["請管理員輸入角色", False]
        # else:
        state += 1
        namelist = ""
        tmprole = reply.split()
        idlist = list(center_ids.keys())
        random.shuffle(idlist)
        for tmp in tmprole:
            data = tmp.split('x')
            role = data[0]
            num = int(data[1])
            for _ in range(0, num):
                tmpid = idlist.pop()
                nickname = center_ids[tmpid]
                if role == "狼人":
                    wolf_ids.append(tmpid)                
                namelist += nickname+"\n"
                role_data[nickname] = initial_role(role)
                if role_data[nickname]["nightskill"]:
                    t_nightskillnum += 1
                role_data[nickname]['userid'] = tmpid
                postsend.user_post(userid, "text", "角色:"+role)
        return["角色已送出可開始發言，請各位確認自己的角色\n人物有:\n"+namelist, False]
    return False


def gamesection(userid, reply):
    global gamestate
    if gamestate == 0:
        if discuss(userid, reply):
            gamestate=2
    elif gamestate == 1:
        if "==" in reply:
            dayvote(userid, reply)          
    elif gamestate == 2:
        if wolfdiscuss(userid, reply):
            gamestate += 1
    elif gamestate == 3 and "==" in reply:
        reply = reply.replace("==", "")
        if nightskill(userid, reply):
            gamestate = 0


def discuss(userid, reply):
    global dayclock, role_data, center_ids,wolf_ids,canvote,skillactive,t_nightskillnum
    nickname = center_ids[userid]
    if role_data[nickname]["die"]>1:
        postsend.user_post(userid, "text", "你遺言交代完了，閉嘴")
    elif not dayclock:    # set the discuss time
        dayclock = True
        action_thread = Thread(target=dayandnight)
        action_thread.start()
    if role_data[nickname]["die"] == 1 and  "==" in reply:
        role_data[nickname]["die"] = 2
        if role_data[nickname]["role"]=="獵人" :
            canvote-=1         
            hunterskill(reply,nickname)  
        else:
            postsend.multi_post(center_ids.keys(), ["text"], [nickname+"的遺言: "+reply])
    elif "==" in reply:
        reply=reply.replace("==","")
        if role_data[nickname]["role"]=="騎士":      
            canvote-=1
            return knightskill(reply,nickname)
                
    else:
        postsend.multi_post(center_ids.keys(), ["text"], [nickname+": "+reply])
    return False


def dayvote(userid, reply):
    global vote, votenum, center_ids, canvote, role_data, t_nightskillnum,kill,halt
    nickname=center_ids[userid]
    reply = reply.replace("==", "")
    if halt and role_data[nickname]["role"]=="獵人" and kill==nickname:
        kill=""
        role_data[nickname]["die"]=2
        hunterskill(reply,nickname) 
    elif not  halt: 
        if role_data[nickname]["die"]!=0:
            postsend.user_post(userid, "text", "你已經沒用處了，閉嘴")
        elif reply not in list(center_ids.values()):
            postsend.user_post(userid, "text", "沒有此人喔")
        elif role_data[nickname]["vote"]:
            postsend.user_post(userid, "text", "你已經投過票了，別想騙我")    
        else:
            role_data[nickname]["vote"]=True
            votenum += 1
            if reply not in vote:
                vote[reply] = 1
            else:
                vote[reply] += 1
            if votenum == canvote:
                kill = max(vote, key=vote.get)
                votenum = 0
                vote = {}
                if role_data[kill]["nightskill"]:
                    t_nightskillnum -= 1
                elif role_data[kill] == "狼人":
                    wolf_ids.remove(role_data[kill]["userid"])
                canvote -= 1
                role_data[kill]["die"] = 1
                if not checkwin(kill+"已被放逐"):  
                    postsend.multi_post(center_ids.keys(), ["text","text"], [kill+"即將被放逐","請公民禁聲，10秒後夜晚來臨"])    
                    if role_data[kill]["role"]=="獵人":
                        role_data[kill]['onetimeskill']=False
                        postsend.user_post(role_data[kill]["userid"], "text", askquestion('獵人'))
                    elif role_data[kill]["role"]=="白痴" and role_data[kill]['onetimeskill']==True:
                        canvote-=1
                        role_data[kill]["onetimeskill"]=False
                        postsend.multi_post(center_ids.keys(), ["text"], ["公告: "+kill+"是白痴，免除這次放逐，但失去投票權"])
                    else:                      
                        postsend.user_post(role_data[kill]["userid"], "text", askquestion('kill'))
                        kill=""
                    tovote(2)
                    action_thread = Thread(target=halt_state(10,"夜晚降臨，狼人請討論"))
                    action_thread.start()        
            else:
                postsend.multi_post(center_ids.keys(), ["text"], [reply+"多一票"])

def tovote(mode):
    global role_data
    for key,value in role_data.items():
        if value["die"]==1 and mode==1:
            value["die"]=2
        elif value["role"]=="白痴" and value["onetimeskill"]==False:
            value["vote"]=True
        else:
            value["vote"]=False

def wolfdiscuss(userid, reply):
    global votenum, vote, center_ids, role_data, kill, shouldkill
    nickname = center_ids[userid]
    if role_data[nickname]["die"]!=0:
        postsend.user_post(userid, "text", "你已經沒用處了，閉嘴")
    elif role_data[nickname]["role"] != "狼人":
        postsend.user_post(userid, "text", "現在是狼人夜晚，閉嘴")
    else:
        if "==" in reply:
            reply = reply.replace("==", "")
            if reply not in list(center_ids.values()) or role_data[reply]["die"]>0:
                postsend.user_post(userid, "text", "沒有此人喔")
            elif role_data[nickname]["vote"]:
                postsend.user_post(userid, "text", "你已經投過票了，別想騙我")    
            else:
                role_data[nickname]["vote"]=True
                votenum += 1
                if reply not in vote:
                    vote[reply] = 1
                else:
                    vote[reply] += 1
                if votenum == len(wolf_ids):
                    die = max(vote, key=vote.get)
                    kill = die
                    shouldkill = True
                    votenum = 0
                    vote = {}
                    postsend.multi_post(wolf_ids, ["text"], ["討論結束，"+die+"被殺"])
                    postsend.multi_post(center_ids.keys(), ["text"], ["夜晚神職人員出動"])
                    for key, value in role_data.items():
                        if value["nightskill"]:
                            print(value)
                            if value["role"] == "女巫" and value["onetimeskill"]["save"]:
                                postsend.user_post(
                                    value["userid"], "text", die+"即將被殺")
                            postsend.user_post(
                                value["userid"], "text", askquestion(value["role"]))
                    return True
                else:
                    postsend.multi_post(wolf_ids, ["text"], [reply+"多一票"])
        else:
            postsend.multi_post(wolf_ids, ["text"], [nickname+": "+reply])
    return False


def nightskill(userid, reply):
    global nightskillnum, t_nightskillnum, center_ids, role_data, kill, shouldkill,\
        witchkill, canvote
    nickname = center_ids[userid]
    if role_data[nickname]["die"]!=0:
            postsend.user_post(userid, "text", "你已經沒用處了，閉嘴")
    elif role_data[nickname]["role"] == "預言家":
        if reply not in list(center_ids.values())or role_data[reply]["die"]>0:
            postsend.user_post(userid, "text", "沒有此人喔")
            return False
        nightskillnum += 1
        postsend.user_post(userid, "text", reply+"是"+role_data[reply]["role"])
    elif role_data[nickname]["role"] == "守衛":
        if reply not in list(center_ids.values())or role_data[reply]["die"]>0:
            postsend.user_post(userid, "text", "沒有此人喔")
            return False
        nightskillnum += 1
        if kill == reply and shouldkill == True:
            shouldkill = False
        elif kill==reply and not shouldkill:
                shouldkill=True
        print(kill,nickname,shouldkill,witchkill)
        postsend.user_post(userid, "text", "你試圖保護"+reply)
    elif role_data[nickname]["role"] == "女巫":   
        if "毒殺_" in reply:      
            reply=reply.replace("毒殺_","")
            if reply not in list(center_ids.values())or role_data[reply]["die"]>0:
                postsend.user_post(userid, "text", "沒有此人喔")
                return False
            if role_data[nickname]["onetimeskill"]["poison"]:
                nightskillnum += 1
                witchkill = reply
                role_data[nickname]["onetimeskill"]["poison"] = False
                if role_data[nickname]["onetimeskill"]["save"]==False:
                    role_data[nickname]["nightskill"]=False
                postsend.user_post(userid, "text", "你要毒殺"+reply)
            else:
                postsend.user_post(userid, "text", "你已使用過此技能")
        elif "救贖_" in reply:
            reply=reply.replace("救贖_","")
            if reply not in list(center_ids.values())or role_data[reply]["die"]>0:
                postsend.user_post(userid, "text", "沒有此人喔")
                return False
            if role_data[nickname]["onetimeskill"]["save"]:
                nightskillnum += 1
                role_data[nickname]["onetimeskill"]["save"] = False
                if role_data[nickname]["onetimeskill"]["poison"]==False:
                    role_data[nickname]["nightskill"]=False
                if kill == reply and shouldkill :
                    shouldkill = False
                elif kill==reply and not shouldkill:
                    shouldkill=True
                postsend.user_post(userid, "text", "你試圖救贖"+reply)
            else:
                postsend.user_post(userid, "text", "你已使用過此技能")
        else:
            postsend.user_post(userid, "text", "請打上你要的動作(救贖_/毒殺_)")
    if nightskillnum == t_nightskillnum:
        print(kill,witchkill)
        nightskillnum = 0
        if shouldkill == False and witchkill == "":
            postsend.multi_post(center_ids, ["text", "text"], ["無人死亡", "進入白天"])
        else:
            for ppl in [kill, witchkill]:
                if ppl!="":
                    print(ppl)
                    role_data[ppl]["die"] = 1
                    if role_data[ppl]["role"] == "狼人":
                        wolf_ids.remove(role_data[ppl]["userid"])
                    elif role_data[ppl]["nightskill"]:
                        t_nightskillnum -= 1
                    canvote -= 1
                    if not checkwin(ppl+"被殺了"):
                        postsend.multi_post(center_ids.keys(), ["text","text"], [ppl+"被殺了","進入白天"])
                        postsend.user_post(role_data[ppl]["userid"], "text", askquestion('kill'))
                    if role_data[kill]["role"]=="獵人":
                        role_data[kill]['onetimeskill']=False
                        postsend.user_post(role_data[kill]["userid"], "text", askquestion('獵人'))
                
            shouldkill = False
            kill = ""
            witchkill = ""
        return True
    return False

def knightskill(reply,nickname):
    global role_data,center_ids,skillactive
    role_data[nickname]["onetimeskill"]=False
    if role_data[reply]["role"] =="狼人":
        role_data[reply]["die"]=2
        wolf_ids.remove(role_data[reply]["userid"])
        if not checkwin("公告: "+nickname+"是騎士，殺掉狼人"+reply):
            skillactive=True
            postsend.multi_post(center_ids.keys(), ["text","text"], ["公告: "+nickname+"是騎士，殺掉狼人"+reply,"進入黑夜"])              
        return True
    else:
        role_data[nickname]["onetimeskill"]=False
        role_data[nickname]["die"]=2
        postsend.multi_post(center_ids.keys(), ["text"], ["公告: "+nickname+"是騎士，殺到好人"+reply+"，以死謝罪"])
        return False

def hunterskill(reply,nickname):
    global role_data,center_ids,t_nightskillnum
    role_data[nickname]["onetimeskill"]=False
    role_data[reply]["die"]=1
    if role_data[reply]["role"] =="狼人":
        wolf_ids.remove(role_data[reply]["userid"])
    elif role_data[reply]["nightskill"]:
        t_nightskillnum-=1
    if not checkwin("公告: "+nickname+"是獵人，開槍帶走"+reply):
        postsend.multi_post(center_ids.keys(), ["text"], ["公告: "+nickname+"是獵人，開槍帶走"+reply])

def checkwin(line):
    global role_data,endgame
    haswolf = False
    hasgood = False
    mode = 0
    truth = ""
    for key, value in role_data.items():
        truth += "\n"+key+":"+value["role"]
        if value["die"] == 0:
            if value["role"] == "狼人":
                haswolf = True
            else:
                hasgood = True
    if haswolf and hasgood:
        mode = 0
    elif hasgood:
        mode = "好人陣隊贏了"
    else:
        mode = "狼人陣隊贏了"
    if mode != 0:  # end of the game
        postsend.multi_post(center_ids.keys(), ["text"], [line])
        postsend.multi_post(center_ids.keys(), ["text", "text", "text"], [
                            mode, "遊戲結束", "真相公布:"+truth])
        endgame=True
        return True
    else:
        return False


def askquestion(role):
    question = {
        "Vote": "請討論要放逐的人，決定好請打上(==要放逐的名字)",
        "狼人": "請討論你要殺的人，決定好請打上(==要殺的名字)",
        "kill": "請在白天說出你的遺言",
        "預言家": "選擇想查驗的人,打上(==發動的名字)",
        "女巫": "毒殺or救贖誰(方式ex:==毒殺_發動的名字)",
        "獵人": "是否開槍,打上(==發動的名字，若不要發動，則不需輸入)",
        "騎士": "要跟誰決鬥,打上(==發動的名字，若不要發動，則不需輸入)",
        "守衛": "你要守護誰,打上(==發動的名字)",
    }
    return question[role]


def halt_state(canvote,line):
    global center_ids, gamestate,halt,endgame
    halt=True
    time.sleep(canvote)
    gamestate += 1
    halt=False
    if not endgame:
        postsend.multi_post(center_ids.keys(), ["text"], [line])

def dayandnight():
    global center_ids, gamestate, dayclock,skillactive
    i = 0
    while True:
        i += 1
        if skillactive:
            dayclock = False
            skillactive=False
            night_event.set()
            return 
        time.sleep(1)
        if i == 3:  # set the daystate  speak time
            if skillactive:
                dayclock = False
                skillactive=False
                night_event.set()
                return 
            night_event.set()
            gamestate += 1
            dayclock = False
            tovote(1)
            postsend.multi_post(center_ids.keys(), ["text"], [askquestion("Vote")])
            break

