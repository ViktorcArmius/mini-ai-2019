def is_inside(pos):
    if ((pos[0]>=0)and
        (pos[0]<31)and
        (pos[1]>=0)and
        (pos[1]<31)):
        return True
    return False

def move_to_str(turn):
    return { turn == (0,0):'None',
             turn == (0,1):'up',
             turn == (0,-1):'down',
             turn == (1,0):'right',
             turn == (-1,0):'left'}[True]

def str_to_move(turn):
    if turn == 'up':
        return (0,1)

    if turn == 'down':
        return (0,-1)

    if turn == 'left':
        return (-1,0)

    if turn == 'right':
        return (1,0)

    return (0,0)

def str_to_int(turn):
    if turn == 'up':
        return 1
    if turn == 'u':
        return 1
    
    if turn == 'down':
        return 3
    if turn == 'd':
        return 3
    
    if turn == 'left':
        return 4
    if turn == 'l':
        return 4
    
    if turn == 'right':
        return 2
    if turn == 'r':
        return 2
    
    return 0

def short_to_str(turn):
    return {'u':'up',
            'd':'down',
            'r':'right',
            'l':'left',
            '':'None'}[turn]

def reverse(turn):
    return { 'up':'down',
             'down':'up',
             'left':'right',
             'right':'left',
             None:'None',
             'None':'None'}[turn]

def valid_turns(pos, prev = 'None', way = '',way_l = [],wx = 31, wy = 31):
    turns = ['up','right','down','left']

    up =    (pos[0],pos[1]+1)
    down =  (pos[0],pos[1]-1)
    left =  (pos[0]-1,pos[1])
    right = (pos[0]+1,pos[1])

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
            adding = [(point[0]-1,point[1]-1),
                      (point[0]-1,point[1]  ),
                      (point[0]-1,point[1]+1),
                      (point[0]  ,point[1]+1),
                      (point[0]+1,point[1]+1),
                      (point[0]+1,point[1]  ),
                      (point[0]+1,point[1]-1),
                      (point[0]  ,point[1]-1)]
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

def last_fill(Ter,Shells,Way):
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

def new_fill(wx,wy,Ter,Shells,Way):
    way   = set(Way)
    
    W = last_fill(Ter,Shells,Way)
    F = set([])
    F.update(set(Way))

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
                another = [(cur[0]-1,cur[1]  ),
                           (cur[0]  ,cur[1]+1),
                           (cur[0]+1,cur[1]  ),
                           (cur[0]  ,cur[1]-1)]
                for point in another:
                    if ((point in W)and
                        (point not in removing)):
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
            another = [(cur[0]-1,cur[1]  ),
                       (cur[0]  ,cur[1]+1),
                       (cur[0]+1,cur[1]  ),
                       (cur[0]  ,cur[1]-1)]
            for point in another:
                if point in W:
                    if point not in removing:
                        removing.add(point)
                if point not in W:
                    if ((point not in F)and
                        (point not in Ter)):
                        W.add(point) #вот тут - если эта территория еще нигде не была, то добавляем
                        removing.add(point)

                        
    return F
