#bearing off AI UI NKing 1/24/2017
#
import sys

def main():
    
    db = {}
    db['[0, 0, 0, 0, 0, 0]'] = (0,0)
    with open("Bearing_Data.txt") as f: #read in data from file to dictionary
        for line in f:
            
            partit = line.split('\t')
            
            key = partit[0]
            exp = partit[1]
            _max = partit[2].strip("\n")
            
            tup = (float(exp),float(_max))
            db[key] = tup
    

    

    class Controller():
        
        def __init__(self):
            self.suggested_pos = '' #position to analyze
            self.suggested_roll = '' #roll to analyze
            
        def ask(self):
            inp = input("Press 1 to analyze a position \nPress 2 for suggested move \nPress Q to quit \n")
            #Menu
            pos= []
            if inp == '1':      #analyze position
                valid = False
                while (valid == False):
                    self.suggested_pos = input("Enter a position to be analyzed: ")
                    
                    if(len(self.suggested_pos) != 6):   #checking input
                        print("Please enter a value with 6 positions \n")
                        valid = False
                    else:
                        valid = True
                        
                    sum_check = (sum(int(i) for i in self.suggested_pos.strip() if i.isdigit()))
                                 
                    if sum_check > 6:   #checking input
                                 
                        print("Please enter less than 6 stones n")
                        valid = False
                    else:
                        valid = True
                        
                                 
                          
                for i in range(0,6):
                    pos.append(int(self.suggested_pos[i]))
                print("Roll\t" + "Expected\t" + "Max")    
                ###################analyze position
                for j in range(1,7):
                    for k in range(1,7):
                        
                        
                            Max = 0
                            exp = 100000000000
                            t = (j,k)
                            e = gen_moves(pos,t)
                            for item in e:
                                #print(str(item))
                                v = db[str(item)][0] 
                                w = db[str(item)][1] 
                                if v < exp:
                                    exp = v
                                if w > Max and w >= exp:
                                    Max = w
                            print(str(j) +',' + str(k) + "\t" + str(exp) + "\t" + str(Max))


                            
            ################analyze roll                
            elif inp == '2':
                valid = False
                while (valid == False):
                    self.suggested_pos = input("Enter a position to be analyzed: ")
                    
                    if(len(self.suggested_pos) != 6):   #checking input
                        print("Please enter a value with 6 positions \n")
                        valid = False
                    else:
                        valid = True
                        
                    sum_check = (sum(int(i) for i in self.suggested_pos.strip() if i.isdigit()))
                                 
                    if sum_check > 6:   #checking input
                                 
                        print("Please enter less than 6 stones n")
                        valid = False
                    else:
                        valid = True          
            
                self.suggested_roll = input("Enter a dice roll (ex: '34' or '16'): ")
                for i in range(0,6):
                    pos.append(int(self.suggested_pos[i]))
                ###############################analyze roll    
                a = int(self.suggested_roll[0])
                b = int(self.suggested_roll[1])
                c = (a,b)
                e = gen_moves(pos,c)
                best_move = [0,0,0,0,0,0]
                Max = 0
                exp = 100000000000
                for item in e:
                    p = item[:]
                    v = db[str(item)][0] 
                    w = db[str(item)][1]
                    
                    if v < exp:
                        exp = v
                        best_move = p 
                    if w > Max and w >= exp:
                        Max = w
                print("Best move: " + str(p) + "\t" + str(exp) + "\t" + str(Max)) 
                    
                    
                 
            elif inp.upper() == ('Q' or 'q'):
                  sys.exit()

            return
        

        
            
##################################### END UI ####################################    
    
    def chk_legal_move(position,index,roll):    #checks if move is legal (position <= roll, no stones higher)
        start = index+1
        if start < roll:        
        
            for idx in range(start,6):
                if position[idx] > 0:
                    return False
            return True   
        elif(start == roll):
            return True
        else:
            return False
        
###########################################
        
    def get_pip(position):
        pip = 0
        for i in range (0,6):
            pip += position[i] * (i + 1)
        return pip

###########################################

    def stone_count(position):
        total = 0
        for i in range (0,6):
            total += position[i]
        return total

############################################
            

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


    
######################EVAL function#####################################
    
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

#############################################################################

    
    C = Controller()
    while(True):        #run
        C.ask()
    
    
    return


if __name__ == "__main__":
    main()
