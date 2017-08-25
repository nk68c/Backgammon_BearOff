#db building bearing off


def main():

    db = {}
    with open("Bearing_Data.txt") as f: #read in data from file to dictionary
        for line in f:
            
            partit = line.split('\t')
            
            key = partit[0]
            exp = partit[1]
            _max = partit[2].strip("\n")
            
            tup = (float(exp),float(_max))
            db[key] = tup
                
            

    def chk_legal_move(position,index,roll):    #checks if move is legal (position <= roll, no stones higher)
        start = index+1
        if start < roll:        #index + 1 or just index here?
        
            for idx in range(start,6):
                if position[idx] > 0:
                    return False
            return True   
        elif(start == roll):
            return True
        else:
            return False

    def get_pip(position):
        pip = 0
        for i in range (0,6):
            pip += position[i] * (i + 1)
        return pip

    def stone_count(position):
        total = 0
        for i in range (0,6):
            total += position[i]
        return total
            

    def gen_moves(position, roll):
        movelist = []                   #given position and roll
        origin = [0, 0, 0, 0, 0, 0]
        d1 = roll[0]                    
        d2 = roll[1]                    #uses chk_legal_move
        new_pos = position[:]
        v1, v2, v3, v4  = False, False, False, False
        t1, t2, t3, t4  = False, False, False, False
        high = max(d1,d2)
        low = min(d1,d2)
        pip = get_pip(position)
        
        if d1 == d2:        #if doubles
            if d1*4 >= pip:
                movelist.append(origin)
                return movelist
            
            for i in range(5,-1,-1):
                #print("Iteration I: " + str(i))
                if position[i] > 0:
                    if i - high >= 0:
                        new_pos[i-high] +=1
                        new_pos[i] -= 1
                        t1 = True
                    else:
                        if (chk_legal_move(new_pos,i,high)):
                            new_pos[i] -= 1
                            v1 = True
                            
                sec_pos = new_pos[:]


                for j in range(5,-1,-1):
                    #print("Iteration J: " + str(j))
                    if new_pos[j] > 0:
                        if j - low >= 0:
                            sec_pos[j-low] +=1
                            sec_pos[j] -= 1
                            t2 = True
                        else:
                            if (chk_legal_move(sec_pos,j,low)):
                                sec_pos[j] -= 1
                                v2 = True

                    thd_pos = sec_pos[:]
                    
                    for k in range(5,-1,-1):
                    #print("Iteration J: " + str(j))
                        if sec_pos[k] > 0:
                            if k - low >= 0:
                                thd_pos[k-low] +=1
                                thd_pos[k] -= 1
                                t3 = True
                            else:
                                if (chk_legal_move(thd_pos,k,low)):
                                    thd_pos[k] -= 1
                                    v3 = True

                        frt_pos = thd_pos[:]

                        for l in range(5,-1,-1):
                        #print("Iteration J: " + str(j))
                            if thd_pos[l] > 0:
                                if l - low >= 0:
                                    frt_pos[l-low] +=1
                                    frt_pos[l] -= 1
                                    t4 = True
                                else:
                                    if (chk_legal_move(frt_pos,l,low)):
                                        frt_pos[l] -= 1
                                        v4 = True

                        

                    
                                        
                            if frt_pos not in movelist and ((t2 == True or v2 == True) and (t1 == True or v1 == True) and (t3 == True or v3 == True) and (t4 == True or v4 == True)):
                                
                                movelist.append(frt_pos)

                            

                            frt_pos = thd_pos[:]
                            v4 = False
                            t4 = False
                        
                        thd_pos = sec_pos[:]
                        v3= False
                        t3 = False
                        
                    sec_pos = new_pos[:]
                    v2 = False
                    t2 = False
                    
                
                new_pos = position[:]
                v1 = False
                t1 = False
                                        
            return movelist 

        else:               ###not doubles
            if d1 + d2 > pip:
                movelist.append(origin)
                return movelist
            
            for i in range(5,-1,-1):
                #print("Iteration I: " + str(i))
                if position[i] > 0:
                    if i - high >= 0:
                        new_pos[i-high] +=1
                        new_pos[i] -= 1
                        t1 = True
                    else:
                        if (chk_legal_move(new_pos,i,high)):
                            new_pos[i] -= 1
                            v1 = True
                            
                sec_pos = new_pos[:]


                for j in range(5,-1,-1):
                    #print("Iteration J: " + str(j))
                    if new_pos[j] > 0:
                        if j - low >= 0:
                            sec_pos[j-low] +=1
                            sec_pos[j] -= 1
                            t2 = True
                        else:
                            if (chk_legal_move(sec_pos,j,low)):
                                sec_pos[j] -= 1
                                v2 = True

                    
                                        
                    if sec_pos not in movelist and ((t2 == True or v2 == True) and (t1 == True or v1 == True)):
                        #print("Iteration I: " + str(i))
                        #print("Iteration J: " + str(j))
                        
                        #print("appending" + str(sec_pos))
                        movelist.append(sec_pos)

                            
                        
                    
                    sec_pos = new_pos[:]
                    v2 = False
                    t2 = False
                    
                
                new_pos = position[:]
                v1 = False
                t1 = False
                                        
            return movelist


    
######################eval function#####################################
    
    def eval(position):             #recursive
        p = position[:]             #uses gen_moves
        #lookup, else
       
        if str(p) in db:
            
            e = db[str(p)][0]
            return e
        else:
            total = 0
            MAX = 0
            tmax = 0
            for d1 in range(1,7):
                for d2 in range(1,7):
                    roll = (d1,d2)
                    movelist = gen_moves(p,roll)
                    #print("Generated moves" + str(d1) + " " + str(d2))
                    best_move = [0,0,0,0,0,0]
                    best_score = 10000000000
                    
                    for move in movelist:
                        p2 = move[:]
                        v = eval(p2) + 1
                        w = v
                        
                        
                        if v < best_score:
                            best_move = p2[:]
                            best_score = v
                            
                        if w >= best_score and w > MAX:
                            MAX = w

                    

                    total += best_score
                    tmax += MAX

            E = total / 36
            M = tmax / 36

            #store E
            db[str(position)] = (round(E,2),int(round(M)))
            
            return E
        

        
        return

#############################################################
    
    def db_builder():       #auto generate database
        pos =[]
        for a in range(0,7):
            for b in range(0,7):  
                for c in range(0,7):
                    for d in range(0,7): 
                        for e in range(0,7): 
                            for f in range(0,7):
                                pos = [a,b,c,d,e,f]
                                if stone_count(pos) > 6:
                                    continue
                                else:
                                    eval(pos)

        return

    db_builder()        #auto database builder

    
    
    
    upos= []            #prompt user for position to exam (manual db builder)
    user = input("Please enter a position: ")
    for i in range(0,6):
        upos.append(int(user[i]))
        
        
    exp = eval(upos)    #find expected value of given position
    print("Expected Value: " + str(exp) + "\n")
    
    
    fout = open("Bearing_Data.txt", "w")        #view Bearing_Data.txt to see learned positions
    for k,v in db.items():
        
        fout.write(k +'\t' + str(v[0]) + "\t" + str(v[1]) + "\n")
        
        
    fout.close()
    
    return



if __name__ == "__main__":
    main()
