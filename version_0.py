import json
import random
import time


def worldinit(d=0):
    W = []
    for i in range(wx):
        W.append([])
        for j in range(wy):
            W[i].append(d)    
    return W

def update(state):
    if state['type'] == 'tick':
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

def in_world(pos):
    if ((pos[0]>=0)and
        (pos[0]<wx)and
        (pos[1]>=0)and
        (pos[1]<wy)):
        return True
    return False

def distance(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def dist_p(p1,p2):
    pos1 = Players[p1]['posit']
    pos2 = Players[p2]['posit']
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

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

def astar_pos(pos,direct):
    A = worldinit(-1)
    prev = direct
        
    not_prev = [pos[0]-move_a(prev)[0],pos[1]-move_a(prev)[1]]

    A[pos[0]][pos[1]] = 0
    stack = []
    adding = [[pos[0],pos[1]+1],
              [pos[0],pos[1]-1],
              [pos[0]+1,pos[1]],
              [pos[0]-1,pos[1]]]
    for i in range(4):
        if ((in_world(adding[i])==True)and
           (adding[i] != not_prev)):
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
                    (adding[i] not in stack)):
                    if (A[adding[i][0]][adding[i][1]]==-1):
                        stack.append(adding[i])
    return A

def astar_ter(p):
    #astar from territory including lines
    A = worldinit(-1)
    #pos = Players[p]['posit']
    #prev = Players[p]['direc'] #string
        
    #not_prev = [pos[0]-move_a(prev)[0],pos[1]-move_a(prev)[1]]

    ter = Players[p]['terri']
    lin = Players[p]['lines']

    
    for pos in ter:
        A[pos[0]][pos[1]] = 0

    Shell = shell(p)
    adding = []
    stack = []
    for pos in Shell:
        adding.extend([[pos[0],pos[1]+1],
              [pos[0],pos[1]-1],
              [pos[0]+1,pos[1]],
              [pos[0]-1,pos[1]]])
    for i in range(len(adding)):
        if ((in_world(adding[i])==True)and
           (adding[i] not in ter)and
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
                    (adding[i] not in ter)and
                    (adding[i] not in lin)):
                    if (A[adding[i][0]][adding[i][1]]==-1):
                        stack.append(adding[i])
    return A

def get_direct_from_astar(astar,point):
    Last = astar[point[0]][point[1]]

    Moves = []
    Values = []
    if point[0]>0:
        Moves.append('right')
        Values.append(astar[point[0]-1][point[1]])
    if point[0]<wx-1:
        Moves.append('left')
        Values.append(astar[point[0]+1][point[1]])
    if point[1]>0:
        Moves.append('up')
        Values.append(astar[point[0]][point[1]-1])
    if point[1]<wy-1:
        Moves.append('down')
        Values.append(astar[point[0]][point[1]+1])

    return Moves[Values.index(min(Values))]

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

def shell(p):
    #returning shell of player`s territory
    terr = Players[p]['terri']
    shell = Players[p]['terri']

    for p in terr:
        up = [p[0],p[1]+1]
        do = [p[0],p[1]-1]
        le = [p[0]-1,p[1]]
        ri = [p[0]+1,p[1]]
        if ((up in terr)and
            (do in terr)and
            (le in terr)and
            (ri in terr)):
            shell.remove(p)
            
    return shell
        
    
def find_interests(p):
    res = []
    P1 = astar(p)
    P2 = astar_ter(p)
    E = []
    I = []
    for pl in Players:
        if pl != 'i':
            E.append(astar(pl))
    
#    W = []
#    for i in range(wx):
#        for j in range(wy):
#            W.append([i,j])

    for i in range(wx):
        for j in range(wy):
            check = True
            for e in E:
                if (P1[i][j]+P2[i][j]<e[i][j])and([i,j] not in Players[p]['terri']):
                    pass #check = True
                else:
                    check = False
            if check == True:
                I.append([i,j])

    Shell = shell(p)

    maxi = 0
    for i in I:
        maxi = max(maxi, P2[i[0]][i[1]])
    mini = wx+wy
    for i in I:
        if P2[i[0]][i[1]] == maxi:
                mini = min(mini,P1[i[0]][i[1]])
    for i in I:
        if P2[i[0]][i[1]] == maxi:
            if mini == P1[i[0]][i[1]]:
                res.append(i)
    return [maxi, res]
           

def mindturn(Target):
    [intr,intter] = find_interests('i')
    debug = ''
    A = []
    
    Pos = Players['i']['posit']
    Move = [0,0]
    MindWay = []
    if ((Target == [-1,-1])
        or((Target == [-2,-2])and(Pos in Players['i']['terri']))):
        #search target
        if intter != []:
            Target = random.choice(intter)
        else:
            Target = [-1,-1]
        debug += '[-1]'
        pass
    if Target == [-2,-2]:
        Shell = shell('i')

        A = astar('i')
        mini = wx+wy

        danger_dist = wx+wy
        for p in Players:
            if p != 'i':
                [dist,dang] = danger('i',p)
                danger_dist = min(danger_dist, dist, dist_p('i',p))

        maxi = 0
        for point in Shell:
            if A[point[0]][point[1]] > 0:
                mini = min(mini, A[point[0]][point[1]])
                maxi = max(maxi, A[point[0]][point[1]])

        if maxi < danger_dist:
            danger_dist = maxi
        for point in Shell:
            if A[point[0]][point[1]] == danger_dist:
                Target = point
        if Target == [-2,-2]:
            mini = wx+wy
            for point in Shell:
                mini = min(mini,A[point[0]][point[1]])
            for point in Shell:
                if mini == A[point[0]][point[1]]:
                    Target = point
        #searching way to home
        debug +='[-2 mini='+str(mini)+']'
        pass
    if (Target != [-1,-1])and(Target != [-2,-2]):
        #just moving
        #Current_Danger = danger('i',e) - lately i will append checking danger of the next turn.
        #now it will be chosen randomly.
        
        danger_dist = wx+wy
        for p in Players:
            if p != 'i':
                [dist,dang] = danger('i',p)
                danger_dist = min(danger_dist, dist, dist_p('i',p))
        
        
        
        A = astar('i')
        MindWay = [Target]
        Last = Target

        while A[Last[0]][Last[1]]>1:
            check = [[Last[0]-1,Last[1]],
                     [Last[0]+1,Last[1]],
                     [Last[0],Last[1]-1],
                     [Last[0],Last[1]+1]]
            check2 = []
            vals   = []
            for el in check:
                if in_world(el) == True:
                    if A[el[0]][el[1]]>0:
                        check2.append(el)
                        vals.append(A[el[0]][el[1]])
            Last = check2[vals.index(min(vals))]
            MindWay.append(Last)
        Move = [Last[0]-Pos[0],Last[1]-Pos[1]]

        Shell = shell('i')
        dire = get_direct_from_astar(A,Last)
        A = astar_pos(Last,dire)
        mini = wx+wy
        for point in Shell:
            if A[point[0]][point[1]] > 0:
                mini = min(mini, A[point[0]][point[1]])
        if mini-2 > danger_dist:
            Target = [-2,-2]
        
        
        if len(MindWay)==1:
            Target = [-2,-2]
        debug +='[0  danger='+str(danger_dist)+']'
        pass
    


    return [Move, Target, MindWay, debug]



random.seed()


with open('mylog.txt', 'w') as outfile:
    config = json.loads(input()) # получение конфигурации игры
    wx = config['params']['x_cells_count']
    wy = config['params']['y_cells_count']
    Players = {}
    Bonuses = []
    Astar = []
    Bstar = []

    Target = [-1,-1]

    while True:
        state = input()  # получение тика
        tick = time.time()
        update(json.loads(state))
        [move,Target,way,debug] = mindturn(Target)
        commands = ['left', 'right', 'up', 'down']  # доступные команды
        cmd = random.choice(commands)  # случайный выбор действия
        cmd = move_s(move)
        log = []
        tock = time.time()
        log.extend([cmd,tock-tick,Players['i']['posit'],Target,debug])#,way,debug])
        print(json.dumps({"command": cmd, 'debug': cmd}))  # отправка результата

            
        json.dump(log, outfile)
        
