import sys
import json
import random
import time
import math



def reverse(turn): #возвращает обратный данному ход. нужен для исключения его из возможных
    return { 'up':'down',
             'down':'up',
             'left':'right',
             'right':'left',
             None:'None',
             'None':'None'}[turn]

def is_inside(pos): #проверка на принадлежность клетки карте
    if ((pos[0]>=0)and
        (pos[0]<wx)and
        (pos[1]>=0)and
        (pos[1]<wy)):
        return True
    return False

def move_to_str(turn):
    return { turn == (0,0):'None',
             turn == (0,1):'up',
             turn == (0,-1):'down',
             turn == (1,0):'right',
             turn == (-1,0):'left'}[True]

def str_to_move(turn):
    return { 'None':(0,0),
             None:  (0,0),
             'up':  (0,1),
             'down':(0,-1),
             'left':(-1,0),
             'right':(1,0)}[turn]

def valid_turns(pos, prev = 'None', way = '',way_l = [],wx = 31, wy = 31): #выдаёт разрешенные ходы
    turns = ['up','right','down','left']

    up =    (pos[0],pos[1]+1)
    down =  (pos[0],pos[1]-1)
    left =  (pos[0]-1,pos[1])
    right = (pos[0]+1,pos[1])

    if reverse(prev) in turns:       #убираем обратный ход
        turns.remove(reverse(prev))

    t_w = []
    if way != []:                           #отсечение возможных ходов так, чтобы путь получался только прямоугольниками
        if ('u' in way)and(way[-1]!='u'):
            t_w.append('up')
        if ('r' in way)and(way[-1]!='r'):
            t_w.append('right')
        if ('d' in way)and(way[-1]!='d'):
            t_w.append('down')
        if ('l' in way)and(way[-1]!='l'):
            t_w.append('left')
      

    if ('up' in turns)and((pos[1] == wy-1)or(up in way_l)):     #убираем ходы, ведущие за пределы карты и на свой хвост
        turns.remove('up')
    if ('right' in turns)and((pos[0] == wx-1)or(right in way_l)):
        turns.remove('right')
    if ('down' in turns)and((pos[1] == 0)or(down in way_l)):
        turns.remove('down')
    if ('left' in turns)and((pos[0] == 0)or(left in way_l)):
        turns.remove('left')

    for turn in t_w:                   #убираем ходы, получаемые для отсечения
        if turn in turns: 
            turns.remove(turn)

    return turns

def connected(Shells,Way):          #проверка на то, что бот присоединён к своей территории
    if (len(Way)==0):
        return True
    check = False
    for Shell in Shells:
        for point in Way:
            if point in Shell:     #если хоть одна клетка пути находится в окружении территории - присоединён
                check = True
                break
        if check ==True:
            break
    return check


def shells(Ter):           #возвращает массив из связных окружений территории
    S = []

    T = set(Ter)
    i=-1
    while len(T)>0:         #пока вся территория не закончится
        i+=1
        S.append(set([]))   #добавим новый элемент в массив
        seed = T.pop()
        removing = set([seed])
        while len(removing)>0:  #и будем заполнять его связными клетками
            point = removing.pop()
            T.discard(point)
            adding = [(point[0]-1,point[1]-1),
                      (point[0]-1,point[1]  ),
                      (point[0]-1,point[1]+1),
                      (point[0]  ,point[1]+1),
                      (point[0]+1,point[1]+1),
                      (point[0]+1,point[1]  ),
                      (point[0]+1,point[1]-1),
                      (point[0]  ,point[1]-1)]
            for add in adding:      #проверяем все клетки в радиусе 1, добавляем их в очередь на удаление
                if ((add in T)and
                    (add not in removing)):
                    removing.add(add)

            adding = [(point[0]-1,point[1]-1),
                      (point[0]-1,point[1]  ),
                      (point[0]-1,point[1]+1),
                      (point[0]  ,point[1]+1),
                      (point[0]+1,point[1]+1),
                      (point[0]+1,point[1]  ),
                      (point[0]+1,point[1]-1),
                      (point[0]  ,point[1]-1)]   #(да, этот кусок кода полностью повторяет предыдущий. раньше они отличались,)
                                                 #(а когда поправил баг не заметил, что они дублируют друг-друга)
            for a in adding:
                if ((a not in S[i])and
                    (a not in Ter)and
                    (a not in removing)):
                    S[i].add(a)             #и если это не клетки территории а соседние клетки, то добавляем их в компоненту связности
    return S
    

def debug_view(Ter,Shells,Way,lists = []):   #выдает рисунок в консоли
    
    N=len(lists)+1
    line = ''
    for k in range(N):
        line += '++'
        for i in range(wx):
            line += str(i%10)
        line += '++ '
    print(line)

    for j in range(wy):
        y=wy-j-1
        line = ''
        for k in range(N):
            line += str(y).zfill(2)
            for i in range(wx):
                if k==0:
                    s = ' '
                    if (i,y) in Ter:
                        s = 't'
                    for Shell in Shells:
                        if (i,y) in Shell:
                            s = '+'
                    if (i,y) in Way:
                        s = 'o'
                    line += s
                if (k>0):
                    m = k-1
                    s = ' '
                    if (i,y) in lists[m]:
                        s = 'X'
                    line += s
            line += str(y).zfill(2)+' '
        print(line)
        
    line = ''
    for k in range(N):
        line += '++'
        for i in range(wx):
            line += str(i%10)
        line += '++ '
    print(line)
    print('')

def last_fill(Ter,Shells,Way):   #возвращает все клетки, соседние с компонентой "территория и путь"
    wayshell = shells(Way)[0]
    I = []
    supershell = set([])
    
    for point in wayshell:
        for shell in Shells:
            if point in shell:
                supershell.update(shell)
    supershell.update(wayshell)
    supershell = supershell - set(Way) - set(Ter)
    return supershell
        
    
        
    
    

def new_fill(Ter,Shells,Way):     #закраска
    #tim = time.perf_counter_ns()
    #app = 0
    #rem = 0
    way   = set(Way)
    
    W = last_fill(Ter,Shells,Way)
    F = set([])
    F.update(set(Way))

##    for point in way:
##        if (point not in Ter)and(point not in F):
##            F.add(point)
##            #app+=1
##            adding = [(point[0]-1,point[1]-1),
##                      (point[0]-1,point[1]  ),
##                      (point[0]-1,point[1]+1),
##                      (point[0]  ,point[1]+1),
##                      (point[0]+1,point[1]+1),
##                      (point[0]+1,point[1]  ),
##                      (point[0]+1,point[1]-1),
##                      (point[0]  ,point[1]-1)]
##            for add in adding:
##                if ((add not in W)and
##                    (add not in way)and
##                    (add not in Ter)):
##                    W.add(add)
##                    #app+=1

    #убираем внешнюю оболочку
    if len(W)>0:        #В W сейчас находится все точки окрестные нужной нам территории, 
        minx = wx       #так что можно выбрать любую из них с минимальной координатой, например по х
        
        for point in W:
            minx = min(minx,point[0])
        seed = (-2,-2)
        for point in W:
            if (point[0] == minx):
                seed = point
                break
        if seed != (-2,-2):
            removing = set([seed])
            while len(removing)>0:
                cur = removing.pop()
                W.remove(cur)
                #app+=1
                #rem+=1
                another = [(cur[0]-1,cur[1]  ),
                           (cur[0]  ,cur[1]+1),
                           (cur[0]+1,cur[1]  ),
                           (cur[0]  ,cur[1]-1)]
                for point in another:
                    if ((point in W)and
                        (point not in removing)):
                        #rem+=1
                        removing.add(point)
                        
    #осталась внутренняя оболочка, но возможно это не вся внутренность
    #нужно еще и расширять эту область
    if (len(W)>0)and(seed != (-2,-2)):
        removing = set([])
        removing.add(W.pop())
        while len(removing)>0:
            cur = removing.pop()
            W.discard(cur)
            F.add(cur)
            #app+=1
            #rem+=1
            another = [(cur[0]-1,cur[1]  ),
                       (cur[0]  ,cur[1]+1),
                       (cur[0]+1,cur[1]  ),
                       (cur[0]  ,cur[1]-1)]
            for point in another:
                if point in W:
                    if point not in removing:
                        #rem+=1
                        removing.add(point)
                if point not in W:
                    if ((point not in F)and
                        (point not in Ter)):
                        #app+=2
                        W.add(point) #вот тут - если эта территория еще нигде не была, то добавляем
                        removing.add(point)
    #tom = time.perf_counter_ns()
    #Time[0] +=(tom-tim)
                        
    return F#,str(Way),str(Ter),app,rem,tom-tim]

def update(state,Players,Bonuses,Tick):    #обновляет всю информацию об игроках
    if state['type'] == 'tick':
        is_tick = True
        Tick = state['params']['tick_num']
        Bonuses = state['params']['bonuses']
        players = state['params']['players']
        for p in Players:
            Players[p]['updat'] = False    #если окажется, что игрок не обновился - значит он умер
        for p in players:
            if p not in list(Players.keys()):
                Players.update(dict.fromkeys([p],{}))
                Players[p].update(dict.fromkeys(['score'],players[p]['score']))
                Players[p].update(dict.fromkeys(['direc'],players[p]['direction']))
                Players[p].update(dict.fromkeys(['bonus'],players[p]['bonuses']))
                Players[p].update(dict.fromkeys(['updat'],True))
                posit = []
                modul = []
                for pos in players[p]['position']:
                    posit.append(int((pos)/30))
                    modul.append(int((pos)%30-15))
                    
                Players[p].update(dict.fromkeys(['posit'],tuple(posit)))
                Players[p].update(dict.fromkeys(['modul'],tuple(modul)))
                
                Players[p].update(dict.fromkeys(['lines'],[]))
                for point in players[p]['lines']:
                    Players[p]['lines'].append((int(point[0]/30),int(point[1]/30)))

                Players[p].update(dict.fromkeys(['terri'],set([])))
                for point in players[p]['territory']:
                    Players[p]['terri'].add((int(point[0]/30),int(point[1]/30)))
                
                    
            else:
                Players[p]['score'] = players[p]['score']
                Players[p]['direc'] = players[p]['direction']
                Players[p]['bonus'] = players[p]['bonuses']
                Players[p]['updat'] = True

                pos = players[p]['position']
                Players[p]['posit'] = (int((pos[0])/30),int((pos[1])/30))
                Players[p]['modul'] = (int((pos[0])%30-15),int((pos[1])%30-15))

                Players[p]['lines'] = []
                for point in players[p]['lines']:
                    Players[p]['lines'].append((int(point[0]/30),int(point[1]/30)))

                Players[p]['terri'] = set([])
                for point in players[p]['territory']:
                    Players[p]['terri'].add((int(point[0]/30),int(point[1]/30)))
        to_del = []
        for p in Players:
            if Players[p]['updat'] == False:
                to_del.append(p)
        for el in to_del:
            Players.pop(el)
    else:
        is_tick = False
        Players = []
        Bonuses = []
        Tick = 2500
    return [is_tick,Players,Bonuses,Tick]

def str_to_int(turn):    #эта и следующая функция нужны для переосознания пути в число
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

def astar(Player,wx,wy):
    #на самом деле от астара тут давно уже только само начальное заполнение
    #это массив достижимости, включая направление движения
    #и что более важно - скорости движения

    A = []
    for x in range(wx):
        A.append([])
        for y in range(wy):
            A[x].append(-1)

    lin = Player['lines']
    pos = Player['posit']
    mod = Player['modul']

    bon = Player['bonus']

    seed = (-2,-2)
    prev = (-2,-2)

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

        prev= str_to_move(reverse(Player['direc']))
        prev= (pos[0]+prev[0],pos[1]+prev[1])

    if mod != [0,0]:
        nex = str_to_move(Player['direc'])
        modul = abs(mod[0])+abs(mod[0])
        if ((mod[0]*nex[0]<0)or
            (mod[1]*nex[1]<0)): #движемся к центру клетки
            prev= str_to_move(reverse(Player['direc']))
            prev= (pos[0]+prev[0],pos[1]+prev[1])

            cells = modul
            A[pos[0]][pos[1]] = cells / Speed[0] / 6
        if ((mod[0]*nex[0]>0)or
            (mod[1]*nex[1]>0)): #движемся от центра клетки
            prev = pos
            pos = (pos[0]+nex[0],pos[1]+nex[1])

            cells = modul + 15
            A[pos[0]][pos[1]] = cells / Speed[0] / 6
        Speed.pop(0)
        A[prev[0]][prev[1]] = 0
    
    seed = pos
    add =    [(seed[0]-1,seed[1]  ),
              (seed[0]  ,seed[1]-1),
              (seed[0]+1,seed[1]  ),
              (seed[0]  ,seed[1]+1)]
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
            add = [(seed[0]-1,seed[1]  ),
                   (seed[0]  ,seed[1]-1),
                   (seed[0]+1,seed[1]  ),
                   (seed[0]  ,seed[1]+1)]
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

def Construct_Enemy(Players,wx,wy):   #массив с временем достижимости врага
    E = []
    for p in list(Players.keys()):
        if p != 'i':
            E.append(astar(Players[p],wx,wy))
            
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
            

TIME = [0,0,0,0,0,0]
Stat = []
def Construct_Tree(Pos,
                   Prev,
                   Ter,
                   Way,
                   enemy,
                   dist,
                   Bonuses,
                   Ter1,
                   Ter5,
                   secret,
                   Tick):
    tim = time.time()
    Shells = shells(Ter)
    is_connected = connected(Shells,Way)
    
    pos_c = (Pos[0],Pos[1]) #позиция в симуляции
    prev  = Prev
    last  = '' #последний путь при спуске вниз

    #if prev != None:
    #    way_s = prev[0] #путь вкратце в виде uuuuuuurrd
    #else:
    way_s = ''
    
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
    T = Tick

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
    slow = []
    for bon in Bonuses:
        if bon['type'] == 'n':
            nitro.append(tuple(bon['position']))
        if bon['type'] == 's':
            slow.append(tuple(bon['position']))

    

    TimeNeed = 0
    c=0
    tom = time.time()
    TIME[0] += tom-tim
    points = 0
    while (uslovie): #пока не ясно что конкретно. пока есть возможность строить пути
        c+=1
        tim = time.time()
        turnout = False  #условие на насильное завершение этой ветви
        
        if len(way_s)>0:
            check = True
            for point in way_l:
                if point not in Ter:
                    if ((enemy[point[0]][point[1]] < TimeNeed+1)):
                        check = False #проверка пути на безопасность
                        break
            #tom = time.perf_counter_ns()
            #Time[0]+=tom-tim
            #tim = time.perf_counter_ns()
            if ((check == True)and
                #('0' in way_i)and  #тут была проверка на то, что путь выходит за свою территорию, но я вынес её отдельно
                #('1' in way_i)):   #а это оказалось не нужно. тем более, что можно отрезать от территории
                (way_i[-1] == '1')): 
                counter +=1
                turnout = True
                fill = set([])
                newpoints = points
                if ('0' in way_i):  #а вот и проверка на выход из своей земли. тут же будет и закраска и подсчёт очков
                    fill = new_fill(Ter,Shells,way_l)
                    onlyfill = fill - set(way_l)
                    of1 = onlyfill & ter1
                    of5 = onlyfill & ter5
                    wa5 = set(way_l) & ter5
                    fill1 = fill&ter1
                    fill5 = fill&ter5
                    for poi in way_l:
                        for p in list(Players.keys()):
                            if p != 'i':
                                if poi in Players[p]['lines']:
                                    newpoints += 50 #выдаём награды за убийства
                    newpoints += 1*len(fill1)+5*len(fill5)
                    #points += 1*(len(of5)+len(wa5))
                    for nit in nitro:
                        if nit in fill:
                            newpoints += 30 #если ускорение будет на захваченной территории то даем бонусные очки 10%
                        
                            
                

                for nit in nitro:
                    if nit in way_l:
                        newpoints += 70 #если ускорение будет прямо в шлейфе то увеличиваем бонус до ~50%

                        
                for slo in slow:
                    if (slo in fill)or(slo in way_l):
                        points = 0 #если попадётся замедление на закрашиваемой территории, то снижаем награду до минимума
                newpoints = newpoints/(len(way_l)+1)
                if is_connected == False:  #если я отделён от своей территории, то мне нужно возвращаться и не важны очки
                    newpoints = 5
                if (newpoints > gain):  #если очков получу больше
                    gain = newpoints
                    gainway = []
                    ssss = way_s
                    iiii = way_i
                    for point in way_l:
                        gainway.append(point)
                    #tom = time.perf_counter_ns()
                    #Time[1]+=tom-tim
                    #tim = time.perf_counter_ns()
                if (newpoints == gain)and(is_connected == True):
                    if len(ssss)>=len(way_s):  #если путь короче при равном числе очков
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

        
        
 
        
        tom = time.time()
        TIME[1] += tom-tim
        tim = time.time()
        valid = valid_turns(pos_c, prev, way_s, way_l, wx, wy)  #разрешенные ходы в этом узле
        turn = ''
        
        try:                    #попытка вытащить прошлое действие на этой же глубине
            lastt = last[depth]
        except:
            lastt = ''
            
        while (len(valid)>0):
            turn = valid.pop(0)
            if str_to_int(turn)>str_to_int(lastt):  #вот тут происходит восприятие пути как числа и разрешается только следующее число
                if turn[0] != lastt:
                    break
        if turn != '':
            if turn[0] == lastt:
                turn = ''
            
        if (depth>= dist)or(T>2493): #если уже подходим к пределу симуляции, то дальше не опускаемся
            turn = ''
        
        tom = time.time()
        TIME[2]+=tom-tim
        tim = time.time() 
        if turn != '': #turn in  - погружение на уровень глубже
            TimeNeed += (30/Speed[depth]/6) #требуемое время. между прочим, только что понял что я не учитываю возможности самому подобрать бонус скорости
            T += int (30/Speed[depth])
            depth +=1
            
            way_l.append(pos_c)
            turn_p = str_to_move(turn)
            
            pos_c = (pos_c[0]+turn_p[0], pos_c[1]+turn_p[1])
            
            prev  = turn
            way_s+=turn[0]
            points += secret[pos_c[0]][pos_c[1]]  #тут отдельно считаются очки от потенциального поля
            if pos_c in Ter:
                way_i+='1'
            else:
                way_i+='0'
        
        tom = time.time()
        TIME[3]+=tom-tim
        tim = time.time() 
                
        if (turn == '')or(turnout == True): #turn out - возвращение на уровень вверх
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
            points -= secret[pos_c[0]][pos_c[1]]

            pos_c = (pos_c[0]-turn_p[0], pos_c[1]-turn_p[1])
            last = way_s
            #if prev != None:
            #    way_s = way_s[0:depth+1]
            #else:
            way_s = way_s[0:depth]
            way_i = way_i[0:depth+1]
            try:
                prev  = short_to_str(way_s[depth-1])
            except:
                prev  = Prev
        
        tom = time.time()
        TIME[4]+=tom-tim
        


    

    #debug_view(Ter,Shells,gainway,[Ter5])
    return [len(gainway),gainway,ssss,gain,[counter,c],iiii]

def Construct_Tree_Home(Pos,   #почти такая же функция, как и предыдущая, но тут нет проверки на опасность пути
                   Prev,        #и ищет только наикратчайший путь
                   Ter,         #смысл в том, что предыдущая функция не может найти ни 1 пути, если внезапно путь стал опасным
                   Way,         #(например, враг дошел до своей территории, у него исчез хвост и он может добраться до тебя быстрее)
                   enemy,
                   dist,
                   Bonuses,
                   Ter1,
                   Ter5,
                   secret,
                   Tick):
    tim = time.time()
    Shells = shells(Ter)
    is_connected = connected(Shells,Way)
    
    pos_c = (Pos[0],Pos[1]) #позиция в симуляции
    prev  = Prev
    last  = '' #последний путь при спуске вниз

    #if prev != None:
    #    way_s = prev[0] #путь вкратце в виде uuuuuuurrd
    #else:
    way_s = ''
    
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
    T = Tick

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
    slow = []
    for bon in Bonuses:
        if bon['type'] == 'n':
            nitro.append(tuple(bon['position']))
        if bon['type'] == 's':
            slow.append(tuple(bon['position']))

    

    TimeNeed = 0
    c=0
    tom = time.time()
    TIME[0] += tom-tim
    points = 0
    mintime = 0
    while (uslovie): #пока не ясно что конкретно. пока есть возможность строить пути
        c+=1
        tim = time.time()
        turnout = False
        
        if len(way_s)>0:
            mintimeenemy = 2500
            check = True
            for point in way_l:
                if point not in Ter:
                    mintimeenemy = min(enemy[point[0]][point[1]],mintimeenemy)
                    
            
            if ((check == True)and
                #('0' in way_i)and
                #('1' in way_i)):
                (way_i[-1] == '1')):
                counter +=1
                turnout = True

                if (len(gainway)==0)or((len(gainway) > len(way_l))or ((len(gainway) == len(way_l))and(mintimeenemy > mintime))):
                    mintime = mintimeenemy
                    gain = mintime
                    gainway = []
                    ssss = way_s
                    iiii = way_i
                    for point in way_l:
                        gainway.append(point)
        
        tom = time.time()
        TIME[1] += tom-tim
        tim = time.time()
        valid = valid_turns(pos_c, prev, way_s, way_l, wx, wy)
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
            
        if (depth>= dist)or(T>2493): #если уже подходим к пределу симуляции, то дальше не опускаемся
            turn = ''
        
        tom = time.time()
        TIME[2]+=tom-tim
        tim = time.time() 
        if turn != '': #turn in
            TimeNeed += (30/Speed[depth]/6)
            T += int (30/Speed[depth])
            depth +=1
            
            way_l.append(pos_c)
            turn_p = str_to_move(turn)
            
            pos_c = (pos_c[0]+turn_p[0], pos_c[1]+turn_p[1])
            
            prev  = turn
            way_s+=turn[0]
            if pos_c in Ter:
                way_i+='1'
            else:
                way_i+='0'
        
        tom = time.time()
        TIME[3]+=tom-tim
        tim = time.time() 
                
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

            pos_c = (pos_c[0]-turn_p[0], pos_c[1]-turn_p[1])
            last = way_s
            #if prev != None:
            #    way_s = way_s[0:depth+1]
            #else:
            way_s = way_s[0:depth]
            way_i = way_i[0:depth+1]
            try:
                prev  = short_to_str(way_s[depth-1])
            except:
                prev  = Prev
        
        tom = time.time()
        TIME[4]+=tom-tim
        


    

    #debug_view(Ter,Shells,gainway,[Ter5])
    return [len(gainway),gainway,ssss,gain,[counter,c],iiii]

def brain_turns(pos,prev,way,enemies):   #проверка "на дурака" - выкидываем из возможных те ходы, где враг может столкнуться с нами
    turns = {'up','right','down','left'}

    turns.discard(reverse(prev))

    u =    (pos[0],pos[1]+1)
    d =    (pos[0],pos[1]-1)
    l =    (pos[0]-1,pos[1])
    r =    (pos[0]+1,pos[1])

    ur = (pos[0]+1,pos[1]+1)
    rd = (pos[0]+1,pos[1]-1)
    dl = (pos[0]-1,pos[1]-1)
    lu = (pos[0]-1,pos[1]+1)

    if (is_inside(u) == False)or(u in way)or(u in enemies):
        turns.discard('up')
    if (is_inside(d) == False)or(d in way)or(d in enemies):
        turns.discard('down')
    if (is_inside(r) == False)or(r in way)or(r in enemies):
        turns.discard('right')
    if (is_inside(l) == False)or(l in way)or(l in enemies):
        turns.discard('left')

    if ur in enemies:
        turns.discard('up')
        turns.discard('right')
    if rd in enemies:
        turns.discard('down')
        turns.discard('right')
    if dl in enemies:
        turns.discard('down')
        turns.discard('left')
    if lu in enemies:
        turns.discard('up')
        turns.discard('left')

    return list(turns)
        
def holy_grail(Ter5): #священный грааль, который поможет мне есть цветные клетки, а не белые

    # нужно заполнить потенциальное поле по увеличению к полям "пятёрок"
    if len(Ter5) == 0:
        Ter5 = [(0,0),(0,wy),(wx,0),(wx,wy)]
    
    Field = []
    T = set([])
    for x in range(wx):
        Field.append([])
        for y in range(wy):
            score = wx+wy
            T.add((x,y))
            if (x,y) in Ter5:
                score = 0
            Field[x].append(score)

    T5 = set(Ter5)
    spread = set([])
    for point in T5:
        T.discard(point)
        adj = [(point[0]+1,point[1]  ),
               (point[0]  ,point[1]+1),
               (point[0]-1,point[1]  ),
               (point[0]  ,point[1]-1)]
        for a in adj:
            if (a in T)and(a not in Ter5)and(a not in spread):
                spread.add(a)
    score = 0
    i = 0
    while len(spread)>0:
        
        
        #for y in range(wy):
        #    line = ''
        #    for x in range(wx):
        #        line +=str(Field[x][y]).zfill(2).replace('0',' ')+' '
        #    print(line)
        #print('')


        i+=1
        score = i
        spr = set([])
        for point in spread:
            T.discard(point)
        for point in spread:
            Field[point[0]][point[1]] = -score

            
            adj = [(point[0]+1,point[1]  ),
                   (point[0]  ,point[1]+1),
                   (point[0]-1,point[1]  ),
                   (point[0]  ,point[1]-1)]
            for a in adj:
                if (a in T)and(a not in spr):
                    spr.add(a)
        spread = set(spr)

    maxi = 0
    for x in range(wx):
        for y in range(wy):
            Field[x][y] -= score
            maxi = max(maxi,-Field[x][y])
    for x in range(wx):
        for y in range(wy):
            Field[x][y] /= maxi
            Field[x][y] +=1
            Field[x][y] /= 4
    return Field
        
    
    
    

random.seed()
wx = 31
wy = 31
tick = 0
saved_way = ''
saved_Way = []
saved_points = 0

tick_time = 0.07
full_time = 0
depth_time = 12

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
ter1 = set([])
ter5 = set([])

last4points = []

while True:
    state = input()  # получение тика
    #json.dump(state, outfile)
    #print("state got", file=sys.stderr)
    #state = '{"type": "tick", "params": {"bonuses": [{"type": "saw", "position": [825, 285], "active_ticks": 10}, {"type": "s", "position": [255, 255], "active_ticks": 50}, {"type": "saw", "position": [105, 915], "active_ticks": 50}], "tick_num": 1141, "players": {"2": {"score": 422, "direction": "down", "territory": [[405, 825], [585, 705], [465, 525], [435, 555], [405, 795], [435, 465], [405, 555], [495, 735], [465, 675], [465, 495], [495, 675], [405, 765], [465, 705], [435, 495], [315, 555], [435, 705], [345, 555], [465, 615], [465, 765], [405, 705], [375, 555], [405, 735], [465, 465], [345, 585], [465, 645], [615, 675], [405, 675], [435, 645], [375, 585], [555, 705], [375, 615], [345, 765], [525, 705], [375, 735], [585, 675], [495, 705], [435, 675], [405, 645], [315, 585], [435, 735], [435, 585], [375, 645], [525, 675], [375, 765], [465, 555], [465, 735], [375, 675], [405, 585], [375, 795], [405, 615], [465, 585], [435, 765], [615, 705], [435, 615], [555, 675], [435, 525], [375, 825]], "lines": [[345, 615], [315, 615], [285, 615]], "position": [285, 615], "bonuses": []}, "3": {"score": 188, "direction": "right", "territory": [[465, 915], [315, 795], [285, 915], [315, 885], [405, 855], [435, 795], [375, 855], [495, 765], [525, 765], [555, 885], [465, 795], [255, 885], [345, 855], [285, 795], [315, 855], [525, 855], [585, 795], [435, 915], [225, 825], [495, 885], [555, 765], [375, 885], [435, 825], [465, 825], [255, 855], [465, 855], [255, 825], [345, 885], [285, 825], [225, 915], [555, 915], [585, 825], [405, 915], [225, 885], [375, 915], [495, 855], [495, 825], [525, 825], [585, 885], [225, 795], [465, 885], [255, 795], [345, 795], [285, 855], [555, 795], [525, 915], [435, 855], [495, 795], [555, 825], [405, 885], [225, 855], [255, 915], [345, 915], [315, 825], [345, 825], [285, 885], [315, 915], [525, 795], [555, 855], [585, 855], [495, 915], [525, 885], [435, 885]], "lines": [], "position": [345, 825], "bonuses": []}, "4": {"score": 383, "direction": "left", "territory": [[75, 615], [375, 255], [225, 375], [255, 435], [345, 135], [285, 75], [165, 345], [135, 285], [15, 645], [105, 315], [105, 705], [135, 315], [195, 375], [75, 735], [15, 675], [15, 225], [195, 105], [135, 465], [15, 585], [225, 75], [165, 195], [135, 195], [105, 525], [285, 135], [135, 495], [165, 435], [315, 105], [45, 735], [315, 195], [195, 495], [75, 465], [75, 195], [45, 315], [105, 375], [345, 225], [285, 45], [195, 435], [15, 615], [105, 735], [225, 225], [75, 435], [195, 165], [165, 255], [135, 405], [105, 225], [165, 555], [105, 675], [105, 585], [135, 435], [75, 495], [225, 255], [15, 465], [135, 585], [45, 675], [165, 465], [135, 615], [195, 555], [75, 285], [195, 285], [255, 405], [45, 255], [45, 705], [315, 225], [255, 135], [255, 105], [195, 225], [75, 225], [225, 435], [45, 285], [225, 135], [105, 255], [345, 195], [165, 285], [15, 495], [225, 405], [165, 585], [75, 645], [105, 195], [135, 525], [405, 285], [45, 615], [105, 555], [135, 555], [15, 435], [195, 345], [15, 195], [105, 405], [165, 135], [195, 75], [45, 645], [285, 225], [225, 105], [75, 315], [165, 225], [165, 375], [45, 225], [255, 165], [75, 705], [105, 615], [15, 735], [75, 675], [195, 405], [15, 285], [165, 495], [105, 465], [195, 135], [45, 585], [15, 315], [135, 225], [105, 285], [135, 255], [165, 405], [285, 195], [225, 285], [75, 525], [45, 195], [195, 525], [45, 495], [315, 135], [195, 255], [195, 465], [225, 195], [195, 195], [45, 525], [105, 495], [345, 165], [285, 105], [225, 465], [15, 255], [165, 525], [225, 165], [135, 165], [165, 315], [105, 435], [105, 345], [405, 315], [75, 255], [75, 585], [135, 345], [225, 495], [15, 705], [195, 585], [255, 375], [45, 435], [105, 645], [345, 105], [285, 165], [135, 375], [195, 315], [165, 165], [75, 555], [165, 615], [255, 465], [45, 465], [315, 165]], "lines": [], "position": [175, 495], "bonuses": []}, "5": {"score": 669, "direction": "left", "territory": [[885, 345], [555, 135], [735, 285], [705, 195], [615, 15], [495, 45], [675, 45], [795, 405], [795, 15], [765, 615], [855, 285], [885, 795], [735, 15], [915, 315], [855, 105], [915, 15], [735, 315], [405, 255], [465, 195], [795, 615], [795, 735], [615, 105], [855, 825], [585, 255], [735, 765], [525, 45], [735, 495], [465, 255], [405, 195], [885, 255], [585, 75], [705, 105], [495, 135], [645, 225], [915, 405], [915, 255], [525, 225], [855, 165], [585, 315], [465, 105], [465, 285], [675, 375], [705, 15], [495, 225], [585, 285], [825, 615], [825, 315], [675, 105], [795, 75], [855, 495], [765, 195], [825, 15], [735, 195], [705, 285], [885, 135], [375, 225], [885, 45], [435, 45], [795, 675], [825, 585], [825, 285], [765, 645], [885, 405], [555, 75], [885, 315], [885, 525], [765, 255], [615, 45], [855, 585], [795, 135], [915, 345], [855, 15], [915, 45], [795, 255], [405, 135], [585, 135], [495, 315], [645, 165], [735, 585], [855, 555], [855, 375], [525, 165], [525, 315], [765, 345], [405, 75], [705, 75], [495, 165], [645, 195], [645, 105], [855, 645], [735, 135], [915, 435], [855, 465], [705, 345], [915, 135], [465, 75], [675, 255], [825, 795], [555, 315], [825, 495], [825, 195], [765, 15], [795, 195], [375, 45], [435, 225], [555, 45], [855, 435], [585, 45], [885, 15], [825, 765], [765, 285], [795, 315], [825, 465], [435, 285], [765, 105], [825, 165], [375, 75], [435, 135], [885, 285], [585, 195], [555, 195], [885, 705], [795, 525], [765, 735], [765, 375], [765, 555], [735, 525], [915, 375], [855, 45], [915, 75], [795, 375], [465, 165], [735, 555], [735, 105], [555, 255], [645, 135], [645, 45], [465, 315], [885, 615], [735, 735], [525, 75], [645, 75], [405, 225], [915, 465], [705, 315], [585, 105], [915, 165], [855, 195], [795, 585], [825, 675], [825, 375], [735, 705], [615, 195], [435, 255], [765, 135], [825, 75], [855, 255], [375, 165], [435, 105], [555, 165], [885, 225], [705, 375], [825, 645], [765, 585], [825, 345], [795, 435], [795, 45], [885, 675], [765, 225], [825, 45], [735, 45], [375, 195], [495, 285], [885, 585], [795, 645], [765, 675], [675, 135], [645, 375], [855, 525], [855, 345], [795, 765], [915, 105], [465, 135], [615, 315], [705, 165], [495, 75], [645, 15], [405, 165], [645, 315], [855, 315], [585, 165], [735, 255], [765, 165], [885, 495], [525, 195], [735, 645], [615, 135], [885, 765], [915, 495], [825, 105], [855, 405], [405, 105], [915, 195], [645, 345], [855, 225], [465, 45], [735, 675], [795, 105], [735, 225], [795, 705], [825, 555], [675, 195], [855, 735], [825, 255], [615, 225], [555, 105], [825, 825], [885, 195], [555, 285], [885, 105], [375, 135], [825, 525], [765, 705], [825, 225], [765, 45], [795, 165], [615, 255], [885, 465], [675, 285], [435, 195], [885, 645], [705, 225], [885, 555], [795, 285], [765, 315], [675, 15], [675, 165], [645, 255], [435, 75], [585, 225], [885, 825], [915, 285], [765, 765], [855, 75], [795, 495], [465, 225], [795, 465], [525, 135], [765, 495], [525, 285], [705, 135], [495, 105], [615, 75], [735, 345], [855, 795], [645, 285], [405, 45], [705, 255], [855, 615], [735, 75], [735, 165], [885, 375], [495, 255], [615, 165], [885, 735], [855, 705], [855, 765], [525, 105], [915, 225], [525, 255], [855, 135], [735, 615], [795, 225], [675, 345], [825, 735], [705, 45], [495, 195], [825, 435], [795, 345], [675, 225], [675, 75], [825, 135], [765, 75], [435, 315], [375, 105], [435, 165], [555, 225], [885, 165], [735, 375], [885, 75], [855, 675], [825, 405], [795, 555], [615, 285], [825, 705], [675, 315], [765, 525], [885, 435]], "lines": [[705, 765], [675, 765], [675, 735], [645, 735], [645, 705], [645, 675], [645, 645], [645, 615], [645, 585], [645, 555], [645, 525], [615, 525], [585, 525], [555, 525]], "position": [555, 525], "bonuses": []}, "i": {"score": 489, "direction": "down", "territory": [[225, 675], [645, 615], [225, 645], [495, 585], [615, 555], [345, 405], [525, 405], [405, 525], [195, 645], [555, 615], [645, 645], [645, 555], [345, 615], [615, 645], [525, 585], [405, 465], [705, 555], [525, 735], [645, 585], [525, 375], [165, 645], [675, 705], [705, 615], [585, 735], [315, 645], [615, 765], [375, 525], [435, 405], [555, 525], [495, 525], [795, 795], [675, 675], [675, 525], [615, 495], [495, 375], [465, 435], [375, 375], [195, 705], [645, 495], [615, 585], [525, 525], [405, 405], [555, 735], [645, 525], [225, 555], [255, 615], [225, 525], [525, 495], [615, 435], [345, 525], [675, 585], [435, 375], [255, 705], [555, 465], [585, 495], [555, 645], [375, 465], [615, 525], [675, 555], [345, 435], [765, 825], [255, 675], [585, 435], [645, 765], [225, 705], [285, 615], [345, 465], [525, 645], [705, 495], [705, 645], [315, 615], [525, 435], [705, 765], [195, 615], [495, 645], [495, 495], [345, 375], [555, 405], [135, 705], [645, 465], [675, 735], [585, 555], [525, 615], [615, 465], [675, 615], [495, 435], [555, 435], [165, 675], [585, 525], [255, 585], [555, 585], [585, 765], [585, 465], [375, 495], [225, 615], [705, 705], [255, 555], [645, 735], [405, 495], [195, 675], [285, 585], [345, 645], [135, 645], [705, 735], [585, 615], [525, 555], [405, 435], [135, 675], [765, 795], [585, 585], [225, 585], [675, 765], [165, 705], [675, 465], [285, 645], [495, 465], [675, 495], [555, 555], [435, 435], [705, 525], [795, 825], [255, 645], [375, 405], [495, 615], [465, 375], [345, 495], [375, 435], [705, 675], [405, 375], [285, 555], [495, 555], [465, 405], [585, 645], [555, 495], [645, 675], [495, 405], [615, 615], [525, 465], [705, 585], [645, 705], [255, 525], [615, 735], [675, 645]], "lines": [[135, 735], [105, 735], [75, 735], [75, 705], [75, 675], [75, 645], [75, 615], [75, 585]], "position": [75, 585], "bonuses": []}}}}'

    
    
    Tick = time.time()
    [is_tick,Players,Bonuses,tick] = update(json.loads(state),Players,Bonuses,tick)
    if full_time > tick_time*tick:  #маленький грааль на динамическую глубину просчёта, в зависимости от затрат времени
        depth_time -=1
    else:
        depth_time +=1

    if depth_time <8:
        depth_time = 8
    if depth_time >20:
        depth_time = 20
        
    enemy = Construct_Enemy(Players,wx,wy)   #заполняем карту достижимости
    
    ter1 = set([])  #делим территории по стоимости
    ter5 = set([])
    for x in range(wx):
        for y in range(wy):
            ter1.add((x,y))
    for p in list(Players.keys()):
        for point in Players[p]['terri']:
            ter1.discard(point)
            if p != 'i':
                ter5.add(point)

    try:
        secret= holy_grail(ter5)  #заполняем потенциальное поле
    except:
        secret = []
        for x in range(wx):
            secret.append([])
            for y in range(wy):
                secret[x].append(1)

    last4points.append(Players['i']['posit'])  #снижаем награду за последние 4 клетки, где был бот - борюсь со стоянием "на месте"
    if len(last4points)>3:                      # иногда бот просто бегал по квадрату 2х2 и думал, что набирает очки
        last4points.pop(0)

    for point in last4points:
        secret[point[0]][point[1]] = 0
    
    S = Construct_Tree(Players['i']['posit'],   #генерируем путь
                       Players['i']['direc'],
                       Players['i']['terri'],
                       Players['i']['lines'],
                       enemy,
                       depth_time,
                       Bonuses,
                       ter1,
                       ter5,
                       secret,
                       tick)
    
    ii = ''
    mode = ''
    if S[2]!= '': #если ход не пустой, то всё хорошо
        cmd = short_to_str(S[2][0])
        points = S[3]
        ii = S[5]
        mode = 'construct'
        
    if S[2] == '': #если ход пустой
        try:        #попробуем сделать небезопасный путь домой
            S = Construct_Tree_Home(Players['i']['posit'],  
                       Players['i']['direc'],
                       Players['i']['terri'],
                       Players['i']['lines'],
                       enemy,
                       int(depth_time/2),
                       Bonuses,
                       ter1,
                       ter5,
                       secret,
                       tick)
            cmd = short_to_str(S[2][0])
            points = S[3]
            ii = S[5]
            mode = 'home'
        except: #если и тут не вышло, то идём по случайным доступным ходам
            try:
                en = []
                for p in list(Players.keys()):
                    if p != 'i':
                        en.append(Players[p]['posit'])
                        
                cmd = random.choice(brain_turns(Players['i']['posit'],Players['i']['direc'],Players['i']['lines'],en))
                mode = 'brained' #безопасный случайный ход
            except:
                cmd = random.choice(valid_turns(Players['i']['posit'],Players['i']['direc'],'',Players['i']['lines'],wx,wy))
                mode = 'random'  #совсем случайный
            points = 0

    en = []
    for p in list(Players.keys()):
        if p != 'i':
            en.append(Players[p]['posit'])
    
    brain = brain_turns(Players['i']['posit'],Players['i']['direc'],Players['i']['lines'],en)
    if cmd not in brain:
        cmd = random.choice(brain)
        mode = 'ultrabrain'
        points = 0  #если выданный ход не безопасный, то меняем его
        
        
    Tock = time.time()
    full_time += Tock-Tick
    
    log = [tick,
           mode,
           Tock-Tick,
           depth_time,
           S[2],
           cmd,
           points,
           S[4]]
    #Time = [0,0,0,0,0,0]
    
    #json.dump(log, outfile)
    #print(log, file=sys.stderr)

    print(json.dumps({"command": cmd, 'debug': str(log)}))  # отправка результата
    #print("step done", file=sys.stderr)

            
        





