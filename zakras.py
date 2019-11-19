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

import zakras
