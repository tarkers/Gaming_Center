import random
from enum import Enum
from . import modelset, postsend, var
from threading import Thread, Event
import time

night_event = Event()


# nightskill = ["女巫", "守衛", "預言家"]
state = -2
gamestate = 0
center_ids = {}
wolf_ids = []
role_data = {}
number = 0
votenum = 0
nightskillnum = 0
t_nightskillnum = 0
main = ""
kill = ""
witchkill = ""
shouldkill = False
dayclock = False
vote = {}


def initial_role(role):
    rolelist={
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
            "vote": False
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
            "nightskill": True,
            "userid": "",
            "role": "狼人",
            "die": 0,
            "lastspeak": True,
            "vote": False
        },
    }
    return rolelist[role]

def test():
    global center_ids, number, role_data, state,t_nightskillnum,wolf_ids
    wolf_ids=["1"]
    t_nightskillnum=1
    state = 2
    number=3
    center_ids = {"1": "1", "2": "2", "3": "3"}
    role_data = {
        "1": {
            "nightskill": True,
            "userid": "1",
            "role": "狼人",
            "die": 0,
            "lastspeak": True,
            "vote": False
        },
        "2": {
            "userid": "2",
            "role": "平民",
            "die": 0,
            "nightskill": False,
            "lastspeak": True,
            "vote": False
        },
        "3": {
            "userid": "3",
            "role": "預言家",
            "die": 0,
            "nightskill": True,
            "lastspeak": True,
            "vote": False
        },
    }
test()

def process(userid, reply):
    global state, role_data, number, center_ids, main, wolf_ids, nightskill, t_nightskillnum
    if state == -2:
        state += 1
        main = userid  # set the 管理員
        return ["請管理員隨便打個字", False]
    elif state == -1:
        state += 1
        return ["請輸入遊玩人數", False]
    elif state == 0:
        number = int(reply)
        if isinstance(number, int):
            state += 1
            return ["請要遊玩的人說HI", False]
        else:
            return["請輸入正確數字", False]
    elif len(center_ids) < number:
        if userid in center_ids:
            return["您已加入了，還剩"+str(number-len(center_ids))+"位", False]
        else:
            center_ids[userid] = modelset.getnickname(userid)
            if len(center_ids) == number:
                return["管理員請輸入角色數量\n ex:[狼人X1 平民X3 預言家X1]", False]
            else:
                return["收到，還剩"+str(number-len(center_ids))+"位", False]
    elif state == 1:
        if userid != main:
            return["請管理員輸入角色", False]
        else:
            state += 1
            namelist = ""
            tmprole = reply.split()
            idlist = list(center_ids.keys())
            random.shuffle(idlist)
            for tmp in tmprole:
                data = tmp.split('X')
                role = data[0]
                num = int(data[1])
                for _ in range(0, num):
                    tmpid = idlist.pop()
                    nickname = center_ids[tmpid]
                    if role == "狼人":
                        wolf_ids.append(tmpid)
                    elif role in nightskill:
                        t_nightskillnum += 1
                    namelist += nickname+"\n"
                    role_data[nickname] = initial_role(role)
                    role_data[nickname]['userid'] = tmpid
                    postsend.user_post(userid, "text", role)
            return["角色已送出可開始發言，請各位確認自己的角色\n人物有:\n"+namelist, False]
    return False


def gamesection(userid, reply):
    global gamestate
    if gamestate == 0:
        discuss(userid, reply)
    elif gamestate == 1:
        if dayvote(userid, reply):
            gamestate += 1
    elif gamestate == 2:
        if wolfdiscuss(userid, reply):
            gamestate += 1
    elif gamestate == 3 and "==" in reply:
        reply = reply.replace("==", "")
        if nightskill(userid, reply):
            gamestate = 0


def discuss(userid, reply):
    global dayclock, role_data, center_ids
    nickname = center_ids[userid]
    if not dayclock:    # set the discuss time
        dayclock = True
        action_thread = Thread(target=dayandnight)
        action_thread.start()
    if role_data[nickname]["die"] == 1:
        role_data[nickname]["die"] = 2
        postsend.multi_post(center_ids.keys(), ["text"], [
                            nickname+"的遺言: "+reply])
    else:
        postsend.multi_post(center_ids.keys(), ["text"], [nickname+": "+reply])


def dayvote(userid, reply):
    global vote, votenum, center_ids, number, role_data, t_nightskillnum
    if "==" in reply:
        reply = reply.replace("==", "")
        if reply not in list(center_ids.values()):
            postsend.user_post(userid, "text", "沒有此人喔")
        else:
            votenum += 1
            if reply not in vote:
                vote[reply] = 1
            else:
                vote[reply] += 1
            if votenum == number:
                die = max(vote, key=vote.get)
                votenum = 0
                vote = {}
                if role_data[die]["nightskill"]:
                    t_nightskillnum -= 1
                elif role_data[die] == "狼人":
                    wolf_ids.remove(role_data[die]["userid"])
                number -= 1
                role_data[die]["die"] = 1
                if not checkwin(die+"已被放逐"):
                    postsend.user_post(
                        role_data[die]["userid"], "text", askquestion('kill'))
                    postsend.multi_post(center_ids.keys(), ["text", "text"], [
                                        die+"已被放逐", "夜晚降臨，狼人請討論"])
                return True
            else:
                postsend.multi_post(center_ids.keys(), ["text"], [reply+"多一票"])
    return False


def wolfdiscuss(userid, reply):
    global votenum, vote, center_ids, role_data, kill, shouldkill
    nickname = center_ids[userid]
    if role_data[nickname]["role"] != "狼人":
        postsend.user_post(userid, "text", "現在是狼人夜晚，閉嘴")
    else:
        if "==" in reply:
            reply = reply.replace("==", "")
            if reply not in list(center_ids.values()):
                postsend.user_post(userid, "text", "沒有此人喔")
                return
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
                postsend.multi_post(center_ids, ["text"], ["夜晚神職人員出動"])
                for key, value in role_data:
                    if value["nightskill"]:
                        if value["role"] == "女巫":
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
        witchkill, number
    nickname = center_ids[userid]
    if role_data[nickname]["role"] == "預言家":
        if reply not in list(center_ids.values()):
            postsend.user_post(userid, "text", "沒有此人喔")
            return
        nightskillnum += 1
        postsend.user_post(userid, "text", reply+"是"+role_data[reply]["role"])
    elif role_data[nickname]["role"] == "守衛":
        if reply not in list(center_ids.values()):
            postsend.user_post(userid, "text", "沒有此人喔")
            return
        nightskillnum += 1
        if kill == nickname and shouldkill == True:
            shouldkill = False
        postsend.user_post(userid, "text", "你試圖保護"+reply)
    elif role_data[nickname]["role"] == "女巫":
        nightskillnum += 1
        if "毒殺_" in reply:
            if role_data[nickname]["onetimeskill"]["poison"]:
                witchkill = reply
                role_data[nickname]["onetimeskill"]["poison"] = False
                postsend.user_post(userid, "text", "你要毒殺"+reply)
            else:
                postsend.user_post(userid, "text", "你已使用過此技能")
        elif "救贖_" in reply:
            if role_data[nickname]["onetimeskill"]["save"]:
                role_data[nickname]["onetimeskill"]["save"] = False
                if kill == nickname and shouldkill == True:
                    shouldkill = False
                postsend.user_post(userid, "text", "你試圖救贖"+reply)
            else:
                postsend.user_post(userid, "text", "你已使用過此技能")
    if nightskillnum == t_nightskillnum:
        nightskillnum = 0
        if shouldkill == False and witchkill == "":
            postsend.multi_post(center_ids, ["text", "text"], ["無人死亡", "進入白天"])
        else:
            for ppl in [kill, witchkill]:
                if role_data[ppl]["role"] == "狼人":
                    wolf_ids.remove(role_data[ppl]["userid"])
                    number -= 1
                    if not checkwin(ppl+"被殺了"):
                        postsend.multi_post(center_ids.keys(), [
                                            "text"], [ppl+"被殺了"])
                        postsend.user_post(
                            role_data[ppl]["userid"], "text", askquestion('kill'))
                elif role_data[ppl]["nightskill"]:
                    t_nightskillnum -= 1
                    number -= 1
                    if not checkwin(ppl+"被殺了"):
                        postsend.multi_post(center_ids.keys(), [
                                            "text"], [ppl+"被殺了"])
                        postsend.user_post(
                            role_data[ppl]["userid"], "text", askquestion('kill'))
            shouldkill = False
            kill = ""
            witchkill = ""
        return True
    return False


def checkwin(line):
    global role_data
    haswolf = False
    hasgood = False
    mode = 0
    truth = ""
    for key, value in role_data:
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
        postsend.multi_post(center_ids, ["text"], [line])
        postsend.multi_post(center_ids, ["text", "text", "text"], [
                            mode, "遊戲結束", "真相公布:"+truth])
        return True
    else:
        return False


def askquestion(role):
    question = {
        "ALL": "請討論要放逐的人，決定好請打上(==要放逐的名字)",
        "狼人": "請討論你要殺的人，決定好請打上(==要殺的名字)",
        "kill": "請在白天說出你的遺言",
        "預言家": "選擇想查驗的人,打上(==發動的名字)",
        "女巫": "毒殺or救贖誰(方式ex:==毒殺_發動的名字)",
        "獵人": "是否要淘汰誰,,打上(==發動的名字)",
        "騎士": "要跟誰決鬥,打上(==發動的名字)",
        "守衛": "你要守護誰,打上(==發動的名字)",
        "黑狼王": "你想淘汰誰,打上(==發動的名字)",
        "白狼王": "你想自爆淘汰誰,打上(==發動的名字)",
        "狼美人": "你想魅惑誰,打上(==發動的名字)",
    }
    return question[role]


def dayandnight():
    global center_ids, gamestate, dayclock
    i = 0
    while True:
        i += 1
        time.sleep(1)
        if i == 3:  # set the daystate  speak time
            night_event.set()
            gamestate += 1
            dayclock = False
            print("16546")
            # postsend.multi_post(center_ids, ["text"], ["夜晚降臨，狼人請討論"])
            postsend.multi_post(center_ids, ["text"], [askquestion("ALL")])
            break
