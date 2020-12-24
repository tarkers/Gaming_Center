import random
from . import modelset
bombnum = -1
minnum = -1
maxnum = -1
state = -1


def number_gen(n, x):
    global minnum, maxnum, bombnum
    minnum = int(n)
    if minnum < 0:
        minnum = 0
    maxnum = int(x)
    bombnum = random.randint(n, x)
    return "炸彈介於"+str(minnum)+"~"+str(maxnum)+"之間"


def check_number(guess, name):
    global minnum, maxnum, bombnum, state
    if guess < minnum or guess > maxnum:
        return "數字沒有在範圍內"
    elif guess == bombnum:
        state = -1
        return "炸彈爆炸 "+name+" 輸了!"
    elif guess > bombnum:
        maxnum = guess
    elif guess < bombnum:
        minnum = guess
    return name+"讓炸彈介於"+str(minnum)+"~"+str(maxnum)+"\n請輸入數字"


def process(id,reply):
    global state
   
    print(reply+"-----------")
    if reply == "退出":
        state = -1
        return ["退出遊戲", True]
    if state == -1:
        state += 1
        return ["請輸入min max值(以空格分開 min最小為0)", False]
    elif state == 0:
        state += 1
        return getrange(reply)
    else:
        return gamesection(reply)

def getrange(reply):
    rangenum = reply.split()
    print(rangenum)
    return [number_gen(int(rangenum[0]), int(rangenum[1]))+"\n請輸入數字", False]

def gamesection(reply):
    name = modelset.groupnickname(id)
    replystring = check_number(int(reply), name)
    if state == -1:
        return [replystring, True]
    else:
        return[replystring, False]