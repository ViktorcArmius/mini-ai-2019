import sys
import json
import random
import time


def reverse(turn):
    if turn == 'up':
        return 'down'
    if turn == 'down':
        return 'up'
    if turn == 'left':
        return 'right'
    if turn == 'right':
        return 'left'
    return None

def move_s(Move):
    if Move == [-1,0]:
        return 'left'
    if Move == [1 ,0]:
        return 'right'
    if Move == [0,-1]:
        return 'down'
    if Move == [0, 1]:
        return 'up'
    pass

def move_a(Move):
    if Move == 'left':
        return [-1,0]
    if Move == 'right':
        return [1 ,0]
    if Move == 'down':
        return [0,-1]
    if Move == 'up':
        return [0, 1]
    return [0,0]

def valid_turns(leaf):
    turns = ['up','down','left','right']
    if reverse(leaf['arr']) in turns:
        turns.remove(reverse(leaf['arr']))
    
    if ('up' in turns)and(leaf['pos'][1] == wy-1):
        turns.remove('up')
    if ('down' in turns)and(leaf['pos'][1] == 0):
        turns.remove('down')
    if ('right' in turns)and(leaf['pos'][0] == wx-1):
        turns.remove('right')
    if ('left' in turns)and(leaf['pos'][0] == 0):
        turns.remove('left')

    for child in leaf['chi']:
        if child['arr'] in turns:
            turns.remove(child['arr'])
            
    turns2 = turns
    for turn in turns2:
        pos = move_a(turn)
        pos_= [leaf['pos'][0]+pos[0],leaf['pos'][1]+pos[1]]
        if pos_ in Way['i']:
            turns.remove(turn)
    return turns

def Valid_turns():
    turns = ['up','down','left','right']
    if reverse(Tree['arr']) in turns:
        turns.remove(reverse(Tree['arr']))
    if ('up' in turns)and(Tree['pos'][1] == wy-1):
        turns.remove('up')
    if ('down' in turns)and(Tree['pos'][1] == 0):
        turns.remove('down')
    if ('right' in turns)and(Tree['pos'][0] == wx-1):
        turns.remove('right')
    if ('left' in turns)and(Tree['pos'][0] == 0):
        turns.remove('left')
    turns2 = turns
    for turn in turns2:
        pos = move_a(turn)
        pos_= [Tree['pos'][0]+pos[0],Tree['pos'][1]+pos[1]]
        if pos_ in Way['i']:
            turns.remove(turn)
    return turns
        

def nearest_points(seed):
    return [[seed[0]-1,seed[1]],
            [seed[0]+1,seed[1]],
            [seed[0],seed[1]-1],
            [seed[0],seed[1]+1]]

def fill_world(Territory, Way):
    W = []
    F = []
    x_min = wx
    x_max = 0
    y_min = wy
    y_max = 0
    
    for point in Territory:
        x_min = min(x_min,point[0])
        x_max = max(x_max,point[0])
        y_min = min(y_min,point[1])
        y_max = max(y_max,point[1])
    for point in Way:
        x_min = min(x_min,point[0])
        x_max = max(x_max,point[0])
        y_min = min(y_min,point[1])
        y_max = max(y_max,point[1])
    
    for x in range(x_min-1,x_max+1):
        for y in range(y_min-1,y_max+1):
            W.append([x,y])
    for point in Territory:
        W.remove(point)
        F.append(point)
    for point in Way:
        if point in W:
            W.remove(point)
            F.append(point)

    removing = [W[0]]
    while len(removing)>0:
        cur = removing[0]
        new = nearest_points(cur)
        for elem in new:
            if (elem not in removing)and(elem in W):
                removing.append(elem)
        W.remove(cur)
        removing.remove(cur)

    for point in W:
        if (point not in Territory)and(point not in F):
            F.append(point)

    return F

def new_fill(Territory, Way):
    #json.dump({'Territory':Territory,'Way':Way}, outfile)
    W = []
    F = []
    for waypoint in Way:
        if waypoint not in Territory:
            F.append(waypoint)
            adding = [[waypoint[0]-1,waypoint[1]-1],
                      [waypoint[0]-1,waypoint[1]  ],
                      [waypoint[0]-1,waypoint[1]+1],
                      [waypoint[0]  ,waypoint[1]+1],
                      [waypoint[0]+1,waypoint[1]+1],
                      [waypoint[0]+1,waypoint[1]  ],
                      [waypoint[0]+1,waypoint[1]-1],
                      [waypoint[0]  ,waypoint[1]-1]]
            for add in adding:
                if ((add not in W)and
                    (add not in Way)and
                    (add not in Territory)):
                    W.append(add)
    if len(W)>0:
        minx = wx
        for point in W:
            minx = min(minx,point[0])
        seed = [-2,-2]
        for point in W:
            if point[0] == minx:
                seed = point
                break
        removing = [seed]
        while len(removing)>0:
            #json.dump({'W':W,'removing':removing}, outfile)
            cur = removing[0]
            removing.remove(cur)
            W.remove(cur)
            another = [[cur[0]-1,cur[1]  ],
                       [cur[0]  ,cur[1]+1],
                       [cur[0]+1,cur[1]  ],
                       [cur[0]  ,cur[1]-1]]
            for point in another:
                if ((point in W)and
                    (point not in removing)):
                    removing.append(point)

    #осталось только граница внутренней части. нужно её расширить внутрь и добавить в W
    if len(W)>0:
        removing = [W[0]]
        while len(removing)>0:
            #json.dump({'W':W,'F':F,'removing':removing}, outfile)
            cur = removing[0]
            removing.remove(cur)
            W.remove(cur)
            F.append(cur)
            another = [[cur[0]-1,cur[1]  ],
                       [cur[0]  ,cur[1]+1],
                       [cur[0]+1,cur[1]  ],
                       [cur[0]  ,cur[1]-1]]
            for point in another:
                if point in W:
                    if point not in removing:
                        removing.append(point)
                if point not in W:
                    if ((point not in F)and
                        (point not in Territory)):
                        W.append(point)
                        removing.append(point)
        
    return F
    

def Simulate(Ter,   #массив данных о всех территориях
             Way,   #массив пути игрока
             leaf,  #текущий лист
             turn   #управляющий ход
             ):
    #json.dump(['simulated',turn], outfile)
    #print('simulating from '+str(leaf['pos'])+' with '+turn)
    #ticks=time.time()
    way = []
    for el in Way:
        way.append(el)
    if leaf['pos'] not in Ter['i']:
        way.append(leaf['pos'])
    if leaf['pos'] in Ter['i']:
        leaf['p_w'] = Way
    #tocks=time.time()
    #T[0]+=tocks-ticks
    #ticks=time.time()
    new_pos = [leaf['pos'][0]+move_a(turn)[0],
               leaf['pos'][1]+move_a(turn)[1]]
    new_leaf = {'poi': leaf['poi'],           #points
                'pos': new_pos,      #position
                'arr': turn,        #arrow = direction
                'cha': [],          #world change
                'p_w': 0,          #previous way
        
                'chi': [],          #children
                'par': leaf,        #parent
                'tik': leaf['tik']+5,           #world tick
                'com': False        #completed leaf
        }
    for enemy in list(Ter.keys()):
        killing = False
        if enemy != 'i':
            if new_pos in Players[enemy]['lines']:
                killing = True
        if killing == True:
            new_leaf['poi']+=50
    #tocks=time.time()
    #T[1]+=tocks-ticks
    #ticks=time.time()

    if (len(way)>0)and(new_pos in Ter['i']):
        Filling = []
        #Filling = fill_world(Ter['i'],way)
        Filling = new_fill(Ter['i'],way)

        for point in Filling:
            if point not in Ter['i']:
                cost = 1
                owner = None
                for enemy in list(Ter.keys()):
                    if enemy != 'i':
                        if point in Ter[enemy]:
                            cost = 5
                            owner = enemy
                new_leaf['poi']+=cost
                new_leaf['cha'].append([point,owner,'i'])

    #tocks=time.time()
    #T[2]+=tocks-ticks
    #ticks=time.time()
    leaf['chi'].append(new_leaf)
    #tocks=time.time()
    #T[3]+=tocks-ticks

    

def turn_in(Ter,
            Way,
            base,
            leaf):
    
    for point in leaf['cha']:
        if point[1] != None:
            Ter[point[1]].remove(point[0])
        if point[2] != None:
            Ter[point[2]].append(point[0])
            
    if leaf['pos'] not in Ter['i']:
        Way.append(leaf['pos'])
        
    if leaf['pos'] in Ter['i']:
        base['p_w'] = Way
        Way = []
    
    return leaf


def turn_out(Ter,
             Way,
             base,
             leaf):
    

    for point in leaf['cha']:
        if point[1] != None:
            Ter[point[1]].append(point[0])
        if point[2] != None:
            Ter[point[2]].remove(point[0])
            
    if leaf['pos'] not in Ter['i']:
        Way.pop()
        
    if leaf['pos'] in Ter['i']:
        Way = base['p_w']
    return base

def turn_(Ter,
         Way,
         base,
         leaf,
         typ):
    #json.dump(['turn '+typ], outfile)
    #print('making turn '+typ+' with base'+str(base['pos'])+' direction '+str(leaf['arr'])+' and leaf'+str(leaf['pos']))
    if typ == 'in':
        return turn_in(Ter,Way,base,leaf)
    if typ == 'out':
        return turn_out(Ter,Way,base,leaf)

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
                for pos in players[p]['position']:
                    Players[p]['posit'].append(int(pos/30))
                
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
                Players[p]['posit'] = [int(pos[0]/30),int(pos[1]/30)]

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
    
def in_world(pos):
    if ((pos[0]>=0)and
        (pos[0]<wx)and
        (pos[1]>=0)and
        (pos[1]<wy)):
        return True
    return False

def worldinit(d=0):
    W = []
    for i in range(wx):
        W.append([])
        for j in range(wy):
            W[i].append(d)    
    return W

def astar(p):
    #astar from position including moving direction
    A = worldinit(-1)
    lin = Players[p]['lines']
    
    pos = Players[p]['posit']
    prev = Players[p]['direc'] #string
        
    not_prev = [pos[0]-move_a(prev)[0],pos[1]-move_a(prev)[1]]

    A[pos[0]][pos[1]] = 0
    stack = []
    adding = [[pos[0],pos[1]+1],
              [pos[0],pos[1]-1],
              [pos[0]+1,pos[1]],
              [pos[0]-1,pos[1]]]
    for i in range(4):
        if ((in_world(adding[i])==True)and
           (adding[i] != not_prev)and
            (adding[i] not in lin)):
               stack.append(adding[i])

    counter = 0
    while len(stack)>0:
        counter += 1
        stack2 = stack
        stack = []
        
        for el in stack2:
            if A[el[0]][el[1]] == -1:
                A[el[0]][el[1]]=counter
            adding = [[el[0],el[1]+1],
                      [el[0],el[1]-1],
                      [el[0]+1,el[1]],
                      [el[0]-1,el[1]]]
            for i in range(4):
                if ((in_world(adding[i])==True)and
                    (adding[i] not in stack)and
                    (adding[i] not in lin)):
                    if (A[adding[i][0]][adding[i][1]]==-1):
                        stack.append(adding[i])
    return A

def Construct_Tree(Ter,
                   Way,
                   Seed,
                   Enemy,
                   deep):
    #print('starting to construct')
    depth = 0
    Current = Seed
    max_points = Current['poi']   #
    max_way    = []               # кусок, отвечающий за сохранение максимально полученных очков за симуляцию
    cur_way    = []               #

    while Seed['com'] == False:
        #print('current pos is '+str(Current['pos'])+' with depth '+str(depth))
        #print('way is '+str(Way['i']))
        #print('way is '+str(cur_way)+' with '+str(Current['poi'])+' pts')
        #tick = time.time()
        if max_points < Current['poi']:
            max_way = []
            for el in cur_way:
                max_way.append(el)
            max_points = Current['poi']
        if (max_points == Current['poi'])and(len(cur_way)<len(max_way)):
            max_way = []
            for el in cur_way:
                max_way.append(el)
            #print('MAX_WAY '+str(max_way))
            #json.dump(max_way, outfile)
        #tock = time.time()
        #Time[0]+=tock-tick
        #tick = time.time()
        p = Current['pos']
        if ((depth < Enemy[p[0]][p[1]]-1)and   #не симулируем на территорию где может быть враг
            (depth < deep)and                    #не симулируем больше 20-ти ходов вглубь
            (Current['tik']<1500-6)):            #и не симулируем за конец игры

            Turns = valid_turns(Current)
            for turn in Turns:
                Simulate(Ter,Way['i'],Current,turn)
        #tock = time.time()
        #Time[1]+=tock-tick
        #tick = time.time()

        Valid_Childrens = []
        for ch in Current['chi']:
            if ch['com'] == False:
                Valid_Childrens.append(ch)
        #print('valid_children`s count: '+str(len(Valid_Childrens)))
        typ = ''
        #tock = time.time()
        #Time[2]+=tock-tick
        #tick = time.time()
        if Valid_Childrens != []:
            base = Current
            leaf = Valid_Childrens[0]
            typ  = 'in'
            cur_way.append(leaf['arr'])
            depth +=1

            
        if (Valid_Childrens == []):
            base = Current['par']
            leaf = Current
            if (Current['par']!=None):
                typ  = 'out'
                cur_way.pop()
                depth -=1

            Current['com'] = True
        #tock = time.time()
        #Time[3]+=tock-tick
        #tick = time.time()
        if typ != '':
            Current = turn_(Ter,Way['i'],base,leaf,typ)
        #tock = time.time()
        #Time[4]+=tock-tick
    #print('max_way: '+str(max_way)+' and max_points: '+str(max_points))
    return [max_way,max_points]

def danger(ways_p,p):
    #way`s_owner & enemy_player
    pos = Players[p]['posit']
    way = Players[ways_p]['lines']

    rng = wx+wy
    dangerpos = []

    for el in way:
        rn2 = abs(el[0]-pos[0])+abs(el[1]-pos[1])
        if rn2 <= rng:
            rng = rn2
    for el in way:
        rn = abs(el[0]-pos[0])+abs(el[1]-pos[1])
        if rng == rn:
            dangerpos.append(el)
            
    return [rng,dangerpos]

random.seed()
tick = [1]
null = None
Time = [0,0,0,0,0]
T =    [0,0,0,0]
Te =   [0,0,0,0,0,0]
TT =   [0,0,0,0,0,0]

with open('mylog2.txt', 'w') as outfile:
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
        #state = json.dumps({"type": "tick", "params": {"players": {"2": {"score": 0, "direction": null, "territory": [[555, 465], [615, 405], [555, 405], [585, 405], [615, 435], [585, 465], [615, 465], [585, 435], [555, 435]], "lines": [], "position": [585, 435], "bonuses": []}, "i": {"score": 0, "direction": null, "territory": [[285, 465], [285, 435], [315, 405], [255, 435], [315, 435], [285, 405], [255, 465], [315, 465], [255, 405]], "lines": [], "position": [285, 435], "bonuses": []}}, "bonuses": [], "tick_num": 1}})
        
        Tick = time.time()
        update(json.loads(state))
        #json.dump(json.loads(state), outfile)

        Tree = {'poi': Players['i']['score'],      #points
                'pos': Players['i']['posit'],      #position
                'arr': Players['i']['direc'],      #arrow = direction
                'cha': [],          #world change
                'p_w': [],          #previous way
        
                'chi': [],          #children
                'par': None,        #parent
                'tik': tick[0],        #world tick  
                'com': False        #completed leaf
                }
        Ter = {}
        Way = {}
        for player in list(Players.keys()):
            Ter.update(dict.fromkeys([player],Players[player]['terri']))
            Way.update(dict.fromkeys([player],Players[player]['lines']))
            
        Enemy2 = []
        for p in list(Players.keys()):
            if p != 'i':
                Enemy2.append(astar(p))

        Enemy = []
        for x in range(wx):
            Enemy.append([])
            for y in range(wy):
                All = []
                for enemy in Enemy2:
                    All.append(enemy[x][y])
                if All != []:
                    Enemy[x].append(min(All))
                else:
                    Enemy[x].append(wx+wy)
        Enemy2 = []
        danger_range = wx+wy
        dist = wx+wy
        for p in Players:
            if p != 'i':
                danger_range = min(danger_range,danger('i',p)[0])
                dist = min(dist,(abs(Players['i']['posit'][0]-Players[p]['posit'][0])+abs(Players['i']['posit'][1]-Players[p]['posit'][1])))
        #json.dump('ready to construct the tree', outfile)
        [way,points] = Construct_Tree(Ter,Way,Tree,Enemy,8)

        
        Tock = time.time()
        #print([way,points,Time,T,Te,TT,Tock-Tick])
        log = {'time':Tock-Tick,'danger':danger_range-1,'lines':len(Players['i']['lines']),'way':way,'pts':Tree['poi'],'pred pts':points,'players':len(list(Players.keys()))}#,way,debug])
        json.dump(log, outfile)
        if way != []:
            cmd = way[0]
        else:
            cmd = random.choice(Valid_turns())
        #json.dump({'tick':tick[0],'pos':Players['i']['posit'],'direction':Players['i']['direc'],'cmd':cmd}, outfile)
        print(json.dumps({"command": cmd, 'debug': cmd}))  # отправка результата
        
            
        

