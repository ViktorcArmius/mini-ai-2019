import sys
import json
import random
import time
import math



def reverse(turn):
    return { 'up':'down',
             'down':'up',
             'left':'right',
             'right':'left',
             None:'None',
             'None':'None'}[turn]

def is_inside(pos):
    if ((pos[0]>=0)and
        (pos[0]<wx)and
        (pos[1]>=0)and
        (pos[1]<wy)):
        return True
    return False

def move_to_str(turn):
    return { turn == [0,0]:'None',
             turn == [0,1]:'up',
             turn == [0,-1]:'down',
             turn == [1,0]:'right',
             turn == [-1,0]:'left'}[True]

def str_to_move(turn):
    return { 'None':[0,0],
             None:[0,0],
             'up':[0,1],
             'down':[0,-1],
             'left':[-1,0],
             'right':[1,0]}[turn]

def valid_turns(pos, prev = 'None', way = '',way_l = []):
    turns = ['up','right','down','left']

    up = [pos[0],pos[1]+1]
    down = [pos[0],pos[1]-1]
    left = [pos[0]-1,pos[1]]
    right = [pos[0]+1,pos[1]]

    if reverse(prev) in turns:
        turns.remove(reverse(prev))

    t_w = []
    if way != []:
        if ('u' in way)and(way[-1]!='u'):
            t_w.append('up')
        if ('r' in way)and(way[-1]!='r'):
            t_w.append('right')
        if ('d' in way)and(way[-1]!='d'):
            t_w.append('down')
        if ('l' in way)and(way[-1]!='l'):
            t_w.append('left')
      

    if ('up' in turns)and((pos[1] == wy-1)or(up in way_l)):
        turns.remove('up')
    if ('right' in turns)and((pos[0] == wx-1)or(right in way_l)):
        turns.remove('right')
    if ('down' in turns)and((pos[1] == 0)or(down in way_l)):
        turns.remove('down')
    if ('left' in turns)and((pos[0] == 0)or(left in way_l)):
        turns.remove('left')

    for turn in t_w:
        if turn in turns:
            turns.remove(turn)

    return turns

def shell(Ter,Way,Pos):
    adjastend = []
    if len(Way)>0:
        seed = Way[0]
    else:
        seed = Pos
    TTT = Ter[:]
    TTT.extend(Way)
    removing = [seed]
    while len(removing)>0:
        point = removing[0]
        adjastend.append(point)
        
        TTT.remove(point)
        removing.remove(point)
        
        adding = [[point[0]-1,point[1]  ],
                  [point[0]  ,point[1]-1],
                  [point[0]+1,point[1]  ],
                  [point[0]  ,point[1]+1]]
        for add in adding:
            if ((add in TTT)and
                (add not in removing)):
                removing.append(add)
    
    S = []
    for point in adjastend:
        adding = [[point[0]-1,point[1]-1],
                  [point[0]-1,point[1]  ],
                  [point[0]-1,point[1]+1],
                  [point[0]  ,point[1]+1],
                  [point[0]+1,point[1]+1],
                  [point[0]+1,point[1]  ],
                  [point[0]+1,point[1]-1],
                  [point[0]  ,point[1]-1]]
        for add in adding:
            if ((add not in S)and
                (add not in adjastend)):
                S.append(add)
    return S
        

def new_fill(Ter,Shell,Way):
    #tim = time.perf_counter_ns()
    #app = 0
    #rem = 0
    W = []
    F = []
    for point in Shell:
        if (point not in Way):
            W.append(point)

    for point in Way:
        if (point not in Ter)and(point not in F):
            F.append(point)
            #app+=1
            adding = [[point[0]-1,point[1]-1],
                      [point[0]-1,point[1]  ],
                      [point[0]-1,point[1]+1],
                      [point[0]  ,point[1]+1],
                      [point[0]+1,point[1]+1],
                      [point[0]+1,point[1]  ],
                      [point[0]+1,point[1]-1],
                      [point[0]  ,point[1]-1]]
            for add in adding:
                if ((add not in W)and
                    (add not in Way)and
                    (add not in Ter)):
                    W.append(add)
                    #app+=1

    #убираем внешнюю оболочку
    if len(W)>0:
        minx = wx
        maxx = -1
        miny = wy
        maxy = -1
        
        for point in W:
            minx = min(minx,point[0])
        seed = [-2,-2]
        for point in W:
            if (point[0] == minx):
                seed = point
                break
        if seed != [-2,-2]:
            removing = [seed]
            while len(removing)>0:
                cur = removing[0]
                removing.remove(cur)
                W.remove(cur)
                #app+=1
                #rem+=1
                another = [[cur[0]-1,cur[1]  ],
                           [cur[0]  ,cur[1]+1],
                           [cur[0]+1,cur[1]  ],
                           [cur[0]  ,cur[1]-1]]
                for point in another:
                    if ((point in W)and
                        (point not in removing)):
                        #rem+=1
                        removing.append(point)
    #осталась внутренняя оболочка, но возможно это не вся внутренность
    #нужно еще и расширять эту область
    
    if (len(W)>0)and(seed != [-2,-2]):
        removing = [W[0]]
        while len(removing)>0:
            cur = removing[0]
            removing.remove(cur)
            W.remove(cur)
            F.append(cur)
            #app+=1
            #rem+=1
            another = [[cur[0]-1,cur[1]  ],
                       [cur[0]  ,cur[1]+1],
                       [cur[0]+1,cur[1]  ],
                       [cur[0]  ,cur[1]-1]]
            for point in another:
                if point in W:
                    if point not in removing:
                        #rem+=1
                        removing.append(point)
                if point not in W:
                    if ((point not in F)and
                        (point not in Ter)):
                        #app+=2
                        W.append(point) #вот тут - если эта территория еще нигде не была, то добавляем
                        removing.append(point)
    #tom = time.perf_counter_ns()
    #Time[0] +=(tom-tim)
    return [F]#,str(Way),str(Ter),app,rem,tom-tim]

def update(state):
    if state['type'] == 'tick':
        tick[0] = state['params']['tick_num']
        Bonuses = state['params']['bonuses']
        players = state['params']['players']
        for p in Players:
            Players[p]['updat'] = False
        for p in players:
            if p not in list(Players.keys()):
                Players.update(dict.fromkeys([p],{}))
                Players[p].update(dict.fromkeys(['score'],players[p]['score']))
                Players[p].update(dict.fromkeys(['direc'],players[p]['direction']))
                Players[p].update(dict.fromkeys(['bonus'],players[p]['bonuses']))
                Players[p].update(dict.fromkeys(['updat'],True))
                    
                Players[p].update(dict.fromkeys(['posit'],[]))
                Players[p].update(dict.fromkeys(['modul'],[]))
                for pos in players[p]['position']:
                    Players[p]['posit'].append(int((pos)/30))
                    Players[p]['modul'].append(int((pos)%30-15))
                
                Players[p].update(dict.fromkeys(['lines'],[]))
                for point in players[p]['lines']:
                    Players[p]['lines'].append([int(point[0]/30),int(point[1]/30)])

                Players[p].update(dict.fromkeys(['terri'],[]))
                for point in players[p]['territory']:
                    Players[p]['terri'].append([int(point[0]/30),int(point[1]/30)])
                
                    
            else:
                Players[p]['score'] = players[p]['score']
                Players[p]['direc'] = players[p]['direction']
                Players[p]['bonus'] = players[p]['bonuses']
                Players[p]['updat'] = True

                pos = players[p]['position']
                Players[p]['posit'] = [int((pos[0])/30),int((pos[1])/30)]
                Players[p]['modul'] = [int((pos[0])%30-15),int((pos[1])%30-15)]

                Players[p]['lines'] = []
                for point in players[p]['lines']:
                    Players[p]['lines'].append([int(point[0]/30),int(point[1]/30)])

                Players[p]['terri'] = []
                for point in players[p]['territory']:
                    Players[p]['terri'].append([int(point[0]/30),int(point[1]/30)])
        to_del = []
        for p in Players:
            if Players[p]['updat'] == False:
                to_del.append(p)
        for el in to_del:
            Players.pop(el)
        pass

def str_to_int(turn):
    return { 'None':0,
             '':0,
             'N':0,
             'up':1,
             'u':1,
             'down':3,
             'd':3,
             'left':4,
             'l':4,
             'right':2,
             'r':2}[turn]

def short_to_str(turn):
    return {'u':'up',
            'd':'down',
            'r':'right',
            'l':'left',
            '':'None'}[turn]

def astar(p):
    #на самом деле от астара тут давно уже только само начальное заполнение
    #это массив достижимости, включая направление движения
    #и что более важно - скорости движения

    A = []
    for x in range(wx):
        A.append([])
        for y in range(wy):
            A[x].append(-1)

    lin = Players[p]['lines']
    pos = Players[p]['posit']
    mod = Players[p]['modul']

    bon = Players[p]['bonus']

    seed = [-2,-2]
    prev = [-2,-2]

    Speed = []
    for i in range(64):
        Speed.append(5)
    for b in bon:
        if b['type']== 'n': #ускорение
            for i in range(b['ticks']):
                Speed[i] = 6
        if b['type']== 's': #замедление
            for i in range(b['ticks']):
                Speed[i] -=1
                if Speed[i] == 4:
                    Speed[i] -=1

    if mod == [0,0]:
        A[pos[0]][pos[1]] = 0

        prev= str_to_move(reverse(Players[p]['direc']))
        prev= [pos[0]+prev[0],pos[1]+prev[1]]

    if mod != [0,0]:
        nex = str_to_move(Players[p]['direc'])
        modul = abs(mod[0])+abs(mod[0])
        if ((mod[0]*nex[0]<0)or
            (mod[1]*nex[1]<0)): #движемся к центру клетки
            prev= str_to_move(reverse(Players[p]['direc']))
            prev= [pos[0]+prev[0],pos[1]+prev[1]]

            cells = modul
            A[pos[0]][pos[1]] = cells / Speed[0] / 6
        if ((mod[0]*nex[0]>0)or
            (mod[1]*nex[1]>0)): #движемся от центра клетки
            prev = pos
            pos = [pos[0]+nex[0],pos[1]+nex[1]]

            cells = modul + 15
            A[pos[0]][pos[1]] = cells / Speed[0] / 6
        Speed.pop(0)
    
    seed = pos
    add =    [[seed[0]-1,seed[1]  ],
              [seed[0]  ,seed[1]-1],
              [seed[0]+1,seed[1]  ],
              [seed[0]  ,seed[1]+1]]
    adding = []
    for a in add:
        if ((a != prev)and
            (is_inside(a) == True)):
            adding.append(a)
    prevtime = A[pos[0]][pos[1]]
    while len(adding)>0:
        speed = 0
        if len(Speed)>0:
            speed = Speed[0]
        else:
            speed = 5
        nexttime = prevtime + 30/speed/6
        prevtime = nexttime
        
        spread = adding
        adding = []

        for seed in spread:
            A[seed[0]][seed[1]] = nexttime
            add = [[seed[0]-1,seed[1]  ],
                   [seed[0]  ,seed[1]-1],
                   [seed[0]+1,seed[1]  ],
                   [seed[0]  ,seed[1]+1]]
            for a in add:
                if is_inside(a)==True:
                    if ((a not in adding)and
                        (A[a[0]][a[1]] == -1)and
                        (a not in lin)):
                        adding.append(a)


        try:
            Speed.pop(0)
        except:
            Speed = [5]

    return A

def Construct_Enemy():
    E = []
    for p in list(Players.keys()):
        if p != 'i':
            E.append(astar(p))
            
    En = []
    for x in range(wx):
        En.append([])
        for y in range(wy):
            En[x].append(wx+wy)
            All = []
            for el in E:
                All.append(el[x][y])
            if All != []:
                En[x][y] = min(All)
    return En
            

Time = [0,0,0,0,0,0]
Stat = []
def Construct_Tree(Pos,
                   Prev,
                   Ter,
                   Way,
                   enemy,
                   dist):
    Shell = shell(Ter,Way,Pos)
    
    pos_c = [Pos[0],Pos[1]] #позиция в симуляции
    prev  = Prev
    last  = '' #последний путь при спуске вниз
    
    way_s = '' #путь вкратце в виде uuuuuuurrd
    way_i = '' #принадлежность клетки своей территории в виде 111111000000001
    if pos_c in Ter:
        way_i = '1'
    else:
        way_i = '0'

    way_l = [] #путь в виде листа
    for el in Way:
        way_l.append(el)

    depth = 0
    counter = 0

    uslovie = True
    gain = 0
    gainway = []
    iiii = way_i
    ssss = ''
    T = tick[0]

    Speed = []
    for i in range(64):
        Speed.append(5)
    for b in Players['i']['bonus']:
        if b['type']== 'n': #ускорение
            for i in range(b['ticks']):
                Speed[i] = 6
        if b['type']== 's': #замедление
            for i in range(b['ticks']):
                Speed[i] -=1
                if Speed[i] == 4:
                    Speed[i] -=1

    nitro = []
    for bon in Bonuses:
        if bon['type'] == 'n':
            nitro.append(bon['position'])

    TimeNeed = 0
    c=0
    while (uslovie): #пока не ясно что конкретно. пока есть возможность строить пути
        c+=1
        #tim = time.perf_counter_ns()
        turnout = False
        
        if len(way_s)>0:
            check = True
            for point in way_l:
                if point not in Ter:
                    if ((enemy[point[0]][point[1]] < TimeNeed+1)):
                        check = False
                        break
            #tom = time.perf_counter_ns()
            #Time[0]+=tom-tim
            #tim = time.perf_counter_ns()
            if ((check == True)and
                ('0' in way_i)and
                (way_i[-1] == '1')):
                counter +=1
                turnout = True
                fill = new_fill(Ter,Shell,way_l)
                points = 0
                for poi in fill[0]:
                    chk = False
                    for p in list(Players.keys()):
                        if p != 'i':
                            if poi in Players[p]['terri']:
                                chk = True
                                break
                    if chk == True:
                        points +=5
                    else:
                        points +=1
                for nit in nitro:
                    if nit in fill[0]:
                        points *= 1.1
                points = points/math.sqrt(len(way_l))
                if points > gain:
                    gain = points
                    gainway = []
                    ssss = way_s
                    iiii = way_i
                    for point in way_l:
                        gainway.append(point)
                    #tom = time.perf_counter_ns()
                    #Time[1]+=tom-tim
                    #tim = time.perf_counter_ns()
                if points == gain:
                    if len(ssss)>=len(way_s):
                        iks = random.randint(0,10)
                        if (len(ssss)>len(way_s) or (iks == 10)):#попытка слегка срандомизировать поиски путей
                            gainway = []
                            ssss = way_s
                            iiii = way_i
                            for point in way_l:
                                gainway.append(point)
                            #tom = time.perf_counter_ns()
                            #Time[2]+=tom-tim
                            #tim = time.perf_counter_ns()

        
        
 
        #tim = time.perf_counter_ns()
        valid = valid_turns(pos_c, prev, way_s, way_l)
        turn = ''
        
        try:                    #попытка вытащить прошлое действие на этой же глубине
            lastt = last[depth]
        except:
            lastt = ''
            
        while (len(valid)>0):
            turn = valid.pop(0)
            if str_to_int(turn)>str_to_int(lastt):
                if turn[0] != lastt:
                    break
        if turn != '':
            if turn[0] == lastt:
                turn = ''
            
        if (depth>= dist)or(T>1493): #если уже подходим к пределу симуляции, то дальше не опускаемся
            turn = ''
        
        #tom = time.perf_counter_ns()
        #Time[3]+=tom-tim
        #tim = time.perf_counter_ns() 
        if turn != '': #turn in
            TimeNeed += (30/Speed[depth]/6)
            T += int (30/Speed[depth])
            depth +=1
            
            way_l.append(pos_c)
            turn_p = str_to_move(turn)
            
            pos_c = [pos_c[0]+turn_p[0], pos_c[1]+turn_p[1]]
            
            prev  = turn
            way_s+=turn[0]
            if pos_c in Ter:
                way_i+='1'
            else:
                way_i+='0'
        
        #tom = time.perf_counter_ns()
        #Time[4]+=tom-tim
        #tim = time.perf_counter_ns() 
                
        if (turn == '')or(turnout == True): #turn out
            depth -=1
            if depth == -1:
                uslovie = False
            TimeNeed -= (30/Speed[depth]/6)
            T -= int(30/Speed[depth])
            try:
                way_l.pop()
            except:
                uslovie = False
            turn_p = str_to_move(prev)

            pos_c = [pos_c[0]-turn_p[0], pos_c[1]-turn_p[1]]
            last = way_s
            way_s = way_s[0:depth]
            way_i = way_i[0:depth+1]
            try:
                prev  = short_to_str(way_s[depth-1])
            except:
                prev  = Prev
        
        #tom = time.perf_counter_ns()
        #Time[5]+=tom-tim
        



    return [len(gainway),gainway,ssss,gain,[counter,c],iiii]        



random.seed()
wx = 31
wy = 31
tick = [0]
saved_way = ''
saved_Way = []
saved_points = 0

null = None

Players = {}
Bonuses = []


#with open('mylogtree.txt', 'w') as outfile:
config = json.loads(input()) # получение конфигурации игры
wx = config['params']['x_cells_count']
wy = config['params']['y_cells_count']
Players = {}
Bonuses = []
Ter = {}
Way = {}
#json.dump('initialisation complete/n', outfile)

while True:
    state = input()  # получение тика
    #json.dump(state, outfile)
    #print("state got", file=sys.stderr)
    #state = json.dumps({"type": "tick", "params": {"players": {"2": {"score": 0, "direction": null, "territory": [[555, 465], [615, 405], [555, 405], [585, 405], [615, 435], [585, 465], [615, 465], [585, 435], [555, 435]], "lines": [], "position": [585, 435], "bonuses": []}, "i": {"score": 0, "direction": null, "territory": [[285, 465], [285, 435], [315, 405], [255, 435], [315, 435], [285, 405], [255, 465], [315, 465], [255, 405]], "lines": [], "position": [285, 435], "bonuses": []}}, "bonuses": [], "tick_num": 1}})
    
    Tick = time.perf_counter_ns()
    update(json.loads(state))
    
    #json.dump(json.loads(state), outfile)
    #print("started to construct enemy", file=sys.stderr)
    enemy = Construct_Enemy()
    #print("enemy constructed", file=sys.stderr)
    #print("started to construct tree", file=sys.stderr)
    S = Construct_Tree(Players['i']['posit'],
                       Players['i']['direc'],
                       Players['i']['terri'],
                       Players['i']['lines'],
                       enemy,
                       13)
    #print("tree constructed", file=sys.stderr)
    #print(S, file=sys.stderr)
    ii = ''
    if S[2]!= '':
        saved_way = S[2]
        saved_Way = S[1]
        cmd = short_to_str(S[2][0])
        points = S[3]
        saved_points = points
        ii = S[5]
        
    if S[2] == '':
        saved_way = saved_way[1:]
        try:
            cmd = short_to_str(saved_way[0])
            points = saved_points
        except:
            cmd = random.choice(valid_turns(Players['i']['posit'],Players['i']['direc']))
            points = 0

        

    #print("commands got", file=sys.stderr)

    
    Tock = time.perf_counter_ns()

    
    log = [tick[0],
           Tock-Tick,
           S[2],
           cmd,
           points,
           S[4]]
    #Time = [0,0,0,0,0,0]
    
    #json.dump(log, outfile)
    print('oldestd time: ', Tock-Tick, file=sys.stderr)
    print(json.dumps({"command": cmd, 'debug': str(log)}))  # отправка результата
    #print("step done", file=sys.stderr)

            
        





