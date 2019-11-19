import sys
import json
import random
import time
import math
import zakras

def connected(Ter,Way,Pos):
    if len(Way)==0:
        return True
    ter = set(Ter)
    ter.update(set(Way))
    start = Way.pop()
    removing = {start}
    while len(removing)>0:
        point = removing.pop()
        ter.discard(point)
        
        adding = [(point[0]-1,point[1]  ),
                  (point[0]  ,point[1]-1),
                  (point[0]+1,point[1]  ),
                  (point[0]  ,point[1]+1)]
        for add in adding:
            if ((add in ter)and
                (add not in removing)):
                removing.add(add)
    if len(ter)>0:
        return False
    else:
        return True

def shell(Ter,Way,Pos):
    adjastend = set([])
    if len(Way)>0:
        seed = Way[0]
    else:
        seed = Pos
    TTT = set(Ter)
    TTT.update(set(Way))
    removing = set([seed])
    while len(removing)>0:
        point = removing.pop()
        adjastend.add(point)
        
        TTT.discard(point)
        
        adding = [(point[0]-1,point[1]  ),
                  (point[0]  ,point[1]-1),
                  (point[0]+1,point[1]  ),
                  (point[0]  ,point[1]+1)]
        for add in adding:
            if ((add in TTT)and
                (add not in removing)):
                removing.add(add)
    
    S = set([])
    for point in adjastend:
        adding = [(point[0]-1,point[1]-1),
                  (point[0]-1,point[1]  ),
                  (point[0]-1,point[1]+1),
                  (point[0]  ,point[1]+1),
                  (point[0]+1,point[1]+1),
                  (point[0]+1,point[1]  ),
                  (point[0]+1,point[1]-1),
                  (point[0]  ,point[1]-1)]
        for add in adding:
            if ((add not in S)and
                (add not in adjastend)):
                S.add(add)
    return S

def shells(Ter):
    S = []

    T = set(Ter)
    i=-1
    while len(T)>0:
        i+=1
        S.append(set([]))
        seed = T.pop()
        removing = set([seed])
        while len(removing)>0:
            point = removing.pop()
            T.discard(point)
            adding = [(point[0]-1,point[1]  ),
                      (point[0]  ,point[1]-1),
                      (point[0]+1,point[1]  ),
                      (point[0]  ,point[1]+1)]
            for add in adding:
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
                      (point[0]  ,point[1]-1)]
            for a in adding:
                if ((a not in S[i])and
                    (a not in Ter)and
                    (a not in removing)):
                    S[i].add(a)
    return S
    

def debug_view(Ter,Shell,Way,lists = []):
    
    N=len(lists)+1
    line = ''
    for k in range(N):
        line += '+'
        for i in range(wx):
            line += str(i%10)
        line += '+ '
    print(line)

    for j in range(wy):
        line = ''
        for k in range(N):
            line += str(j%10)
            for i in range(wx):
                if k==0:
                    s = ' '
                    if (i,j) in Ter:
                        s = 't'
                    if (i,j) in Shell:
                        s = '+'
                    if (i,j) in Way:
                        s = 'o'
                    line += s
                if (k>0):
                    m = k-1
                    s = ' '
                    if (i,j) in lists[m]:
                        s = 'X'
                    line += s
            line += '| '
        print(line)
        
    line = ''
    for k in range(N):
        line += '+'
        for i in range(wx):
            line += str(i%10)
        line += '+ '
    print(line)
    print('')

def last_fill(Ter,Shells,Way):
    wayshell = shells(Way)[0]
    I = []
    supershell = set([])
    
    for point in wayshell:
        for shell in Shells:
            if point in shell:
                supershell.update(shell)
                
    return supershell
        
    
        
    
    

def new_fill(Ter,Shells,Way):
    pr = False
##    if Way == [(17, 23), (17, 24), (17, 25), (17, 26), (17, 27), (17, 28), (16, 28), (15, 28), (15, 27)]:
##        pr = True
##    if pr == True:
##        SS = last_fill(Ter,shells(Ter),Way)
##        debug_view([],list(SS),[],[])
##        debug_view(list(Ter),list(SS),list(Way),[])
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
    if pr == True:
        debug_view(list(Ter),list(Shell),list(Way),[list(W),list(F)])

    #убираем внешнюю оболочку
    if len(W)>0:
        minx = wx
        
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
                        
    if pr == True:
        debug_view(list(Ter),list(Shell),list(Way),[list(W),list(F)])
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
                        
    if pr == True:
        debug_view(list(Ter),list(Shell),list(Way),[list(W),list(F)])
    return F#,str(Way),str(Ter),app,rem,tom-tim]

def update(state,Players,Bonuses,Tick):
    if state['type'] == 'tick':
        is_tick = True
        Tick = state['tick_num']
        Bonuses = state['bonuses']
        players = state['players']
        for p in Players:
            Players[p]['updat'] = False
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
        nex = zakras.str_to_move(Player['direc'])
        modul = abs(mod[0])+abs(mod[0])
        if ((mod[0]*nex[0]<0)or
            (mod[1]*nex[1]<0)): #движемся к центру клетки
            prev= zakras.str_to_move(reverse(Player['direc']))
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
    
    seed = pos
    add =    [(seed[0]-1,seed[1]  ),
              (seed[0]  ,seed[1]-1),
              (seed[0]+1,seed[1]  ),
              (seed[0]  ,seed[1]+1)]
    adding = []
    for a in add:
        if ((a != prev)and
            (zakras.is_inside(a) == True)):
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
                if zakras.is_inside(a)==True:
                    if ((a not in adding)and
                        (A[a[0]][a[1]] == -1)and
                        (a not in lin)):
                        adding.append(a)


        try:
            Speed.pop(0)
        except:
            Speed = [5]

    return A

def Construct_Enemy(Players,wx,wy):
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
                   Tick):
    tim = time.time()
    Shells = shells(Ter)
    is_connected = connected(Ter,Way,Pos)
    
    pos_c = (Pos[0],Pos[1]) #позиция в симуляции
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
    while (uslovie): #пока не ясно что конкретно. пока есть возможность строить пути
        c+=1
        tim = time.time()
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
                ('1' in way_i)):
                #(way_i[-1] == '1')):
                counter +=1
                #turnout = True
                fill = zakras.new_fill(wx,wy,Ter,Shells,way_l)
                fill1 = fill&ter1
                fill5 = fill&ter5
                #for poi in way_l:
                #    for p in list(Players.keys()):
                #        if p != 'i':
                #            if poi in Players[p]['lines']:
                #                points += 50 #выдаём награды за убийства
                points = 1*len(fill1)+5*len(fill5)
                if is_connected == False:
                    points = 5
                for nit in nitro:
                    if nit in fill:
                        points *= 1.1 #если ускорение будет на захваченной территории то даем бонусные очки 10%
                    if nit in way_l:
                        points *= 1.35 #если ускорение будет прямо в шлейфе то увеличиваем бонус до ~50%
                #for slo in slow:
                #    if slo in fill[0]:
                #        points = 0 #если попадётся замедление на закрашиваемой территории, то снижаем награду до минимума
                points = points/(len(way_l))
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

        
        
 
        
        tom = time.time()
        TIME[1] += tom-tim
        tim = time.time()
        valid = zakras.valid_turns(pos_c, prev, way_s, way_l, wx, wy)
        turn = ''
        
        try:                    #попытка вытащить прошлое действие на этой же глубине
            lastt = last[depth]
        except:
            lastt = ''
            
        while (len(valid)>0):
            turn = valid.pop(0)
            if zakras.str_to_int(turn)>zakras.str_to_int(lastt):
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
            turn_p = zakras.str_to_move(turn)
            
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
            turn_p = zakras.str_to_move(prev)

            pos_c = (pos_c[0]-turn_p[0], pos_c[1]-turn_p[1])
            last = way_s
            way_s = way_s[0:depth]
            way_i = way_i[0:depth+1]
            try:
                prev  = zakras.short_to_str(way_s[depth-1])
            except:
                prev  = Prev
        
        tom = time.time()
        TIME[4]+=tom-tim
        



    return [len(gainway),gainway,ssss,gain,[counter,c],iiii]        

def brain_turns(pos,prev,way,enemies):
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

    if (is_inside(u) == False)or(u in way):
        turns.discard('up')
    if (is_inside(d) == False)or(d in way):
        turns.discard('down')
    if (is_inside(r) == False)or(r in way):
        turns.discard('right')
    if (is_inside(l) == False)or(l in way):
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
#config = json.loads(input()) # получение конфигурации игры
wx = 31#config['params']['x_cells_count']
wy = 31#config['params']['y_cells_count']
Players = {}
Bonuses = []
Ter = {}
Way = {}
ter1 = set([])
ter5 = set([])
#json.dump('initialisation complete/n', outfile)

if True:
    #state = input()  # получение тика
    #json.dump(state, outfile)
    #print("state got", file=sys.stderr)
    state = json.dumps({"type": "tick", "players": {"1": {"score": 452, "direction": "right", "territory": [[195, 345], [225, 675], [225, 375], [135, 705], [255, 435], [165, 135], [255, 495], [225, 645], [105, 765], [285, 525], [135, 735], [165, 795], [165, 225], [285, 345], [135, 285], [345, 405], [195, 645], [165, 675], [255, 285], [315, 315], [315, 405], [255, 585], [195, 375], [375, 285], [195, 735], [345, 315], [135, 465], [225, 615], [375, 315], [135, 765], [255, 255], [165, 195], [105, 525], [255, 555], [225, 345], [135, 495], [195, 675], [285, 585], [285, 255], [345, 345], [285, 405], [165, 435], [195, 405], [165, 495], [315, 555], [255, 345], [315, 645], [195, 765], [315, 255], [375, 345], [195, 495], [135, 675], [345, 555], [135, 225], [375, 555], [225, 315], [195, 705], [375, 375], [255, 315], [135, 255], [195, 435], [225, 585], [195, 615], [225, 285], [165, 705], [285, 495], [285, 645], [345, 585], [285, 315], [195, 795], [345, 285], [285, 465], [165, 255], [195, 525], [165, 555], [315, 495], [315, 345], [255, 645], [315, 435], [105, 585], [375, 585], [195, 255], [135, 435], [375, 405], [195, 465], [225, 555], [225, 255], [135, 585], [405, 345], [195, 825], [225, 735], [195, 195], [255, 615], [225, 825], [165, 465], [225, 525], [165, 525], [225, 465], [195, 555], [285, 555], [285, 375], [195, 285], [255, 405], [315, 585], [165, 765], [315, 285], [315, 375], [105, 795], [405, 315], [135, 795], [195, 225], [345, 435], [225, 795], [225, 495], [225, 435], [195, 585], [255, 375], [225, 765], [165, 285], [195, 315], [225, 405], [165, 585], [285, 615], [165, 735], [165, 165], [285, 285], [345, 465], [285, 435], [135, 525], [405, 285], [255, 465], [315, 525], [315, 615], [165, 825], [315, 465], [105, 555], [255, 525], [135, 555], [345, 375]], "lines": [], "position": [195, 765], "bonuses": []}, "2": {"score": 426, "direction": "left", "territory": [[15, 795], [255, 765], [345, 735], [15, 885], [105, 855], [45, 795], [345, 705], [285, 675], [315, 765], [285, 795], [315, 855], [315, 705], [105, 705], [15, 825], [405, 795], [15, 675], [75, 735], [495, 735], [345, 615], [135, 915], [75, 705], [255, 855], [255, 825], [105, 615], [225, 885], [165, 645], [345, 645], [75, 675], [15, 735], [405, 765], [465, 705], [135, 645], [285, 855], [165, 885], [105, 915], [45, 735], [105, 825], [45, 885], [435, 705], [225, 855], [465, 765], [405, 705], [15, 765], [405, 735], [75, 795], [105, 735], [45, 915], [165, 855], [135, 855], [285, 765], [315, 795], [315, 885], [285, 915], [105, 675], [75, 765], [405, 675], [75, 855], [495, 765], [15, 915], [255, 885], [255, 735], [375, 615], [345, 765], [135, 885], [375, 735], [45, 675], [105, 885], [45, 825], [135, 615], [495, 705], [285, 705], [375, 705], [435, 675], [285, 825], [315, 735], [315, 675], [255, 705], [45, 705], [435, 735], [45, 855], [375, 645], [195, 855], [375, 765], [15, 705], [465, 735], [255, 795], [375, 675], [345, 795], [255, 675], [375, 795], [75, 825], [105, 645], [225, 705], [75, 915], [15, 855], [435, 765], [285, 735], [165, 615], [285, 885], [315, 825], [135, 825], [195, 885], [315, 915], [45, 765], [75, 885], [345, 675]], "lines": [[315, 645]], "position": [315, 645], "bonuses": []}, "i": {"score": 292, "direction": "up", "territory": [[465, 645], [615, 675], [555, 555], [645, 615], [645, 525], [435, 645], [555, 705], [495, 615], [525, 765], [495, 585], [585, 555], [675, 615], [615, 555], [465, 795], [675, 645], [525, 705], [585, 525], [555, 615], [645, 645], [645, 555], [585, 675], [555, 585], [495, 555], [465, 675], [615, 645], [405, 645], [585, 645], [525, 585], [525, 735], [645, 585], [435, 585], [525, 675], [555, 645], [495, 675], [615, 525], [615, 615], [405, 585], [405, 615], [585, 615], [525, 555], [495, 795], [465, 585], [465, 615], [435, 615], [525, 645], [555, 675], [585, 585], [525, 615], [495, 645], [615, 585], [435, 885]], "lines": [], "position": [525, 705], "bonuses": []}, "4": {"score": 354, "direction": "down", "territory": [[555, 135], [885, 345], [735, 285], [705, 195], [795, 15], [765, 435], [705, 315], [795, 405], [855, 285], [855, 105], [915, 165], [735, 315], [855, 195], [915, 315], [825, 375], [765, 135], [855, 255], [705, 375], [885, 225], [825, 345], [795, 435], [465, 255], [765, 225], [885, 255], [675, 315], [675, 405], [645, 225], [915, 405], [855, 345], [915, 255], [915, 105], [855, 165], [675, 375], [675, 105], [825, 315], [765, 195], [825, 15], [645, 315], [735, 195], [885, 135], [705, 285], [735, 255], [855, 315], [825, 285], [885, 405], [885, 315], [765, 255], [795, 135], [915, 345], [855, 405], [855, 15], [915, 195], [705, 435], [855, 225], [795, 255], [585, 135], [735, 225], [645, 165], [675, 195], [825, 255], [855, 375], [885, 195], [885, 105], [825, 225], [675, 435], [795, 165], [675, 285], [735, 405], [705, 225], [795, 285], [645, 195], [645, 105], [675, 165], [765, 315], [645, 255], [705, 345], [915, 285], [855, 75], [915, 135], [735, 435], [675, 255], [735, 345], [825, 195], [795, 195], [645, 285], [705, 255], [855, 435], [705, 405], [795, 315], [765, 285], [825, 405], [825, 165], [495, 255], [885, 375], [885, 285], [765, 375], [915, 375], [525, 255], [855, 45], [915, 225], [915, 75], [855, 135], [795, 375], [795, 225], [675, 345], [795, 345], [675, 225], [825, 135], [765, 405], [825, 435], [885, 165], [735, 375], [885, 75], [765, 345], [765, 165]], "lines": [[645, 375], [615, 375], [615, 345], [615, 315], [615, 285], [585, 285], [555, 285], [555, 255], [555, 225], [525, 225], [525, 195], [525, 165]], "position": [525, 165], "bonuses": []}, "5": {"score": 541, "direction": "right", "territory": [[495, 45], [615, 15], [675, 45], [645, 75], [585, 105], [735, 15], [345, 135], [345, 45], [465, 195], [615, 105], [615, 195], [435, 105], [375, 165], [525, 45], [825, 75], [555, 165], [315, 15], [255, 165], [795, 45], [825, 45], [435, 15], [585, 75], [735, 45], [495, 135], [705, 105], [525, 225], [285, 135], [345, 75], [465, 105], [465, 135], [525, 15], [495, 225], [705, 15], [495, 75], [705, 165], [645, 15], [405, 165], [795, 75], [435, 45], [585, 165], [195, 135], [315, 105], [555, 75], [525, 195], [615, 45], [405, 105], [825, 105], [315, 165], [345, 15], [465, 45], [405, 135], [795, 105], [195, 165], [615, 225], [555, 105], [525, 165], [315, 45], [315, 135], [375, 135], [615, 255], [435, 195], [765, 45], [375, 15], [405, 75], [555, 15], [495, 165], [705, 75], [495, 15], [675, 15], [735, 135], [585, 225], [345, 165], [465, 75], [465, 225], [225, 165], [525, 135], [705, 135], [495, 105], [615, 75], [375, 45], [435, 225], [765, 15], [555, 45], [405, 45], [735, 75], [585, 45], [255, 135], [435, 135], [375, 75], [585, 195], [765, 105], [555, 195], [735, 165], [225, 135], [525, 105], [285, 165], [345, 105], [465, 15], [465, 165], [405, 15], [735, 105], [585, 15], [495, 195], [555, 255], [705, 45], [645, 45], [675, 75], [435, 165], [375, 105], [765, 75], [555, 225], [315, 75], [585, 255], [435, 75], [525, 75]], "lines": [[765, 135], [795, 135], [825, 135]], "position": [825, 135], "bonuses": []}}, "bonuses": [], "tick_num": 1009, "saw": []})
    
    Tick = time.time()
    [is_tick,Players,Bonuses,tick] = update(json.loads(state),Players,Bonuses,tick)
    if full_time > tick_time*tick:
        depth_time -=1
    else:
        depth_time +=1

    if depth_time <8:
        depth_time = 8
        
    enemy = Construct_Enemy(Players,wx,wy)
    
    ter1 = set([])
    ter5 = set([])
    for x in range(wx):
        for y in range(wy):
            ter1.add((x,y))
    for p in list(Players.keys()):
        for point in Players[p]['terri']:
            ter1.discard(point)
            if p != 'i':
                ter5.add(point)
    
    S = Construct_Tree(Players['i']['posit'],
                       Players['i']['direc'],
                       Players['i']['terri'],
                       Players['i']['lines'],
                       enemy,
                       depth_time,
                       Bonuses,
                       ter1,
                       ter5,
                       tick)
    
    ii = ''
    if S[2]!= '':
        saved_way = S[2]
        saved_Way = S[1]
        cmd = zakras.short_to_str(S[2][0])
        points = S[3]
        saved_points = points
        ii = S[5]
        
    if S[2] == '':
        saved_way = saved_way[1:]
        try:
            cmd = zakras.short_to_str(saved_way[0])
            points = saved_points
        except:
            try:
                en = []
                for p in list(Players.keys()):
                    if p != 'i':
                        en.append(Players[p]['posit'])
                        
                cmd = random.choice(brain_turns(Players['i']['posit'],Players['i']['direc'],Players['i']['lines'],en))
            except:
                cmd = random.choice(zakras.valid_turns(Players['i']['posit'],Players['i']['direc'],'',Players['i']['lines'],wx,wy))
            points = 0

        

    #print("commands got", file=sys.stderr)

    
    Tock = time.time()
    full_time += Tock-Tick
    
    log = [tick,
           'superr',
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

            
        





