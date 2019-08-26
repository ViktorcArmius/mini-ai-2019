import random
import time

def team(n):
    if n == 0:
        return ' '
    if n == 1:
        return 'r'
    if n == 2:
        return 'R'
    if n == 3:
        return 'g'
    if n == 4:
        return 'G'
    if n == 5:
        return 'b'
    if n == 6:
        return 'B'
    if n == 7:
        return 'm'
    if n == 8:
        return 'M'

def worldinit(d=0):
    W = []
    for i in range(wx):
        W.append([])
        for j in range(wy):
            W[i].append(d)    
    return W

def setplayers(W,N):
    if N>4:
        N=4
    P=[]
    poses=[[4,4],[15,15],[4,15],[15,4]]
    for n in range(N):
        p = {'pos':[-1,-1],'ter':[],'way':[],'poi':0}
        px = poses[n][0]#random.randrange(wx)
        py = poses[n][1]#random.randrange(wy)
        p['pos']=[px,py]
        for i in range(3):
            for j in range(3):
                if (px-1+i >= 0)and(px-1+i < wx)and(py-1+j >= 0)and(py-1+j < wy):
                    W[px-1+i][py-1+j]=n*2+1
                    p['ter'].append([px-1+i,py-1+j])
                    
        W[px][py]=n*2+2
        P.append(p)
    return P

def nums(i):
    if (i>=0)and(i<=9):
        return str(int(i))
    return ' '

def debug_view(arrays=[],lists=[],numbers=[]):
    n=len(arrays)
    l=len(arrays)+len(lists)
    N=len(arrays)+len(lists)+len(numbers)
    line = ''
    for k in range(N):
        line += '+'
        for i in range(wx):
            line += '-'
        line += '+ '
    print(line)

    for j in range(wy):
        line = ''
        for k in range(N):
            line += '|'
            for i in range(wx):
                if k<n:
                    line += team(arrays[k][i][j])
                if (k>=n)and(k<l):
                    m = k-n
                    s = ' '
                    if [i,j] in lists[m]:
                        s = 'X'
                    line += s
                if (k>=l):
                    m = k-l
                    line += nums(numbers[m][i][j])
            line += '| '
        print(line)
        
    line = ''
    for k in range(N):
        line += '+'
        for i in range(wx):
            line += '-'
        line += '+ '
    print(line)

def filling(W,player):
    seed1 = []
    for i in range(wx+2):
        for j in range(wy+2):
            seed1.append([i-1,j-1])
    seedw = []
    seed2 = []
    for elem in Players[player]['ter']:
        seed1.remove(elem)
    for elem in Players[player]['way']:
        seed1.remove(elem)
        seedw.append(elem)
    
    seed = seed1[0]
    point = seed
    stack = []
    adding = [[point[0],point[1]+1],
              [point[0],point[1]-1],
              [point[0]+1,point[1]],
              [point[0]-1,point[1]]]
    for i in range(4):
        if (adding[i] in seed1)and(adding[i] not in stack):
            stack.append(adding[i])
    seed1.remove(point)
    seed2.append(point)
    while len(stack)>0:
        point = stack[0]
        adding = [[point[0],point[1]+1],
                  [point[0],point[1]-1],
                  [point[0]+1,point[1]],
                  [point[0]-1,point[1]]]
        for i in range(4):
            if (adding[i] in seed1)and(adding[i] not in stack):
                stack.append(adding[i])
                
        seed1.remove(point)
        stack.remove(point)
        seed2.append(point)
        #debug_view(W,seed1,seedw,seed2)
    #как проверить на соприкосновение с территорией?
    #надо построить границу территории и проверять для неё

    if len(seed1)>=len(seed2):
        seedw.extend(seed2)
    else:
        seedw.extend(seed1)

    for el in seedw:
        if (el[0]==-1)or(el[0]==wx+1)or(el[1]==-1)or(el[1]==wy+1):
            seedw.remove(el)
    return seedw

def worldprint(W):
    line = '+'
    for j in range(wx):
        line += '-'
    line += '+'

    print(line)
    for j in range(wy):
        line = '|'
        for i in range(wx):
            line += team(W[i][j])
        line += '|'
        print(line)
        
    line = '+'
    for j in range(wx):
        line += '-'
    line += '+'
    print(line)

def move(player,command):
    if abs(command[0])+abs(command[1])==1:
        oldpos = [Players[player]['pos'][0],
                  Players[player]['pos'][1]]
        newpos = [Players[player]['pos'][0]+command[0],
                  Players[player]['pos'][1]+command[1]]

        if (newpos[0]>=0)and(newpos[0]<wx)and(newpos[1]>=0)and(newpos[1]<wy):

            Players[player]['pos']=newpos

            World[oldpos[0]][oldpos[1]]=player*2+1
            World[newpos[0]][newpos[1]]=player*2+2
        
            if (newpos not in Players[player]['ter'])and(newpos not in Players[player]['way']):
                Players[player]['way'].append(newpos)
                #Astar = astar(player)

            if (newpos in Players[player]['ter'])and(Players[player]['way']!=[]):
                #how to fill territory?
                fill = filling(World,player)
                for el in fill:
                    Players[player]['ter'].append(el)
                    World[el[0]][el[1]] = 2*player+1
                    for k in range(len(Players)):
                        if k != player:
                            if el in Players[k]['ter']:
                                Players[k]['ter'].remove(el)
                #adding points
                Players[player]['poi']+=len(fill)
                Players[player]['way']=[]
                return True
        else:
            #player will die
            return True

def turn(s):
    if s == 'w':
        move(0,[0,-1])
    if s == 's':
        move(0,[0,1])
    if s == 'a':
        move(0,[-1,0])
    if s == 'd':
        move(0,[1,0])
    return True

def randturn():
    n = random.randrange(4)
    if n == 0:
        return [0,-1]
    if n == 1:
        return [0,1]
    if n == 2:
        return [-1,0]
    if n == 3:
        return [1,0]
    return True

def print_points():
    line = ''
    for i in range(len(Players)):
        line += str(i)+': '+str(Players[i]['poi'])+' pts  '
    print(line)

def minrange(mine,enemy):
    enemypos = Players[enemy]['pos']
    way = Players[mine]['way']
    rng = wx+wy
    dangerpos = [-1,-1]

    for el in way:
        rng2 = abs(el[0]-enemypos[0])+abs(el[1]-enemypos[1])
        if rng2 <= rng:
            rng = rng2
            dangerpos = el
            
    return [rng,dangerpos]

def distance(mine,enemy):
    mp = Players[mine]['pos']
    ep = Players[enemy]['pos']

    return abs(mp[0]-ep[0])+abs(mp[1]-ep[1])

def astar(player, mode='t', hide_if_inside=False):
    A = worldinit(-1)
    W = []
    for i in range(wx):
        for j in range(wy):
            W.append([i,j])

    Pos  = Players[player]['pos']
    if mode == 't':
        Ter  = Players[player]['ter']
    if mode == 'p':
        Ter = [Pos]
    if (Pos not in Ter)or(hide_if_inside==False):
        stack = []
        for el in Ter:
            A[el[0]][el[1]]=0
            adding = [[el[0],el[1]+1],
                      [el[0],el[1]-1],
                      [el[0]+1,el[1]],
                      [el[0]-1,el[1]]]
            for i in range(4):
                if ((adding[i][0]>=0)and
                    (adding[i][0]<wx)and
                    (adding[i][1]>=0)and
                    (adding[i][1]<wy)and
                    (adding[i] not in stack)and
                    (adding[i] not in Ter)):
                    if (A[adding[i][0]][adding[i][1]]==-1):
                        stack.append(adding[i])
                        
        counter = 0
        #debug_view([World],[],[A])
        #print(stack)
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
                    if ((adding[i][0]>=0)and
                        (adding[i][0]<wx)and
                        (adding[i][1]>=0)and
                        (adding[i][1]<wy)and
                        (adding[i] not in stack)):
                        if (A[adding[i][0]][adding[i][1]]==-1):
                            stack.append(adding[i])
            #debug_view([World],[],[A])
            
    return A

def find_interests(player,maxi=True):
    res = []
    P1 = astar(player,'p')
    P2 = astar(player,'t')
    E = []
    for i in range(len(Players)):
        if player != i:
            E.append(astar(i,'p'))
                 
    for i in range(wx):
        for j in range(wy):
            cond = True
            for k in range(len(E)):
                if (2*P1[i][j]) > E[k][i][j]:
                     cond = False
            if cond == True:
                res.append([i,j])
    if maxi == True:
        maxi = 0
        for el in res:
            maxi = max(maxi,P2[el[0]][el[1]])
        resf=[]
        for el in res:
            if P2[el[0]][el[1]] == maxi:
                resf.append(el)
        return resf
    else:
        return res


def mindturn(Target):
    Int = find_interests(1,True)
    Pos = Players[1]['pos']
            
    if Target == [-1,-1]:
        for el in Int:
            if el in Players[1]['ter']:
                Int.remove(el)
        Target = Int[random.randrange(len(Int))]
        [rng,target] = minrange(0,1)        
        Int = find_interests(1,False)
        if target in Int:
            Target = target

    if (Target != [-1,-1])and(Target != [-2,-2]):
        [rng,target] = minrange(0,1)        
        Int = find_interests(1,False)
        if target in Int:
            Target = target
        if Pos[1] != Target[1]:
            Move = [0, int((Target[1]-Pos[1])/abs(Target[1]-Pos[1]))]
        else:
            if Pos[0] != Target[0]:
                Move = [int((Target[0]-Pos[0])/abs(Target[0]-Pos[0])),0]
            else:
                Target = [-2,-2]
    if Target == [-2,-2]:
        Bstar = astar(1)
        moves = [[Pos[0],Pos[1]+1],
                 [Pos[0],Pos[1]-1],
                 [Pos[0]+1,Pos[1]],
                 [Pos[0]-1,Pos[1]]]
        m = []
        for i in range(4):
            if ((moves[i][0]>=0)and
                (moves[i][0]<wx)and
                (moves[i][1]>=0)and
                (moves[i][1]<wy)):
                if ((Bstar[moves[i][0]][moves[i][1]]<Bstar[Pos[0]][Pos[1]])and
                    (moves[i] not in Players[1]['way'])):
                    m.append(moves[i])
        if m==[]:
            for i in range(4):
                if ((moves[i][0]>=0)and
                    (moves[i][0]<wx)and
                    (moves[i][1]>=0)and
                    (moves[i][1]<wy)):
                    if ((Bstar[moves[i][0]][moves[i][1]]<=Bstar[Pos[0]][Pos[1]])and
                        (moves[i] not in Players[1]['way'])):
                        m.append(moves[i])
        Move = [-Pos[0]+m[0][0],-Pos[1]+m[0][1]]
        if m[0] in Players[1]['ter']:
            Target = [-1,-1]
    
    Ter = Players[1]['ter']
    if Pos in Ter:
        [rng,target] = minrange(0,1)        
        Int = find_interests(1,False)
        if target in Int:
            Target = target
            
    return [Move, Target]
    
    



random.seed()
World = []
Astar = []
Bstar = []
Interesting = []
Players = []
N = 20
wx = N
wy = N
tick = -1
tock = -1
Target = [-1,-1]



World = worldinit()
Astar = worldinit(-1)
Bstar = worldinit(-1)
Players = setplayers(World,2)
Interesting = find_interests(0)
Interesting2 = find_interests(1)
print_points()
debug_view([World],[Interesting],[Astar,Bstar])
s = ' '
while (s != 'q'):
    s = input('command: ')
    tick = time.time()
    turn(s)
    [aiturn, Target] = mindturn(Target)
    move(1,aiturn)
    tock = time.time()
    print('time is needed: '+str(tock-tick))
    print_points()
    if Players[0]['way']!=[]:
        print('danger: '+str(minrange(0,1)))
    if Players[1]['way']!=[]:
        print('target: '+str(minrange(1,0)))
    print('AI made a turn '+str(aiturn)+' with a target '+str(Target))
    Astar = astar(0,'p',True)
    Bstar = astar(1,'p')
    Interesting = find_interests(0)
    Interesting2 = find_interests(1)
    debug_view([World],[Interesting,Interesting2],[Astar,Bstar])
    print('s="'+s+'"')
