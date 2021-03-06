import csp
#mathomata me rergastirio h sto 1o slot h sto 2o slot
#tha prepei na desmeysoyme to epomeno slot an 1o ------> 2o
#otan  vlepo lab na ftiaxno ekstra mathima poy prepei na bei meta toi theoria
class BigProblem( csp.CSP):
    



    # A CSP is specified by the following inputs:
    #         variables   A list of variables; each is atomic (e.g. int or string).
    #         domains     A dict of {var:[possible_value, ...]} entries.
    #         neighbors   A dict of {var:[var,...]} that for each variable lists
    #                     the other variables that participate in constraints.
    #         constraints A function f(A, a, B, b) that returns true if neighbors
    #                     A, B satisfy the constraint when they have values A=a, B=b
    
    def __init__( self, HalfYear, Name_Lessons, names_teachers, Hard, Lab):
        
        self.variables = []
        self.domains = dict()
        self.neighbors = dict()

        self.HalfYear = HalfYear
        self.NameLessons = Name_Lessons
        self.NameTeachers = names_teachers
        self.Hard = Hard
        self.Lab = Lab

        self.size = len( Name_Lessons)

        for i in range(self.size):
            lesson = Name_Lessons[i]
            self.variables.append( lesson)
        
        #exoume 21 meres
        #me 3 slot kathe mera
        #
        #px 1h mera -> 9-12, 12-3, 3-6
        #ara ena tuple (1, 9-12) (1, 12-3), (1, 3-6)
        #to proto stoixeio toy tuple dhlonei poia mera tis eksetastikis kai to 2o poio slot
        #ara 1...21 meres * 3 = 63 tuple synolika 
        SlotList = []
        for i in range( 21):
            t1 = ( i+1, "9-12")
            t2 = ( i+1, "12-3")
            t3 = ( i+1, "3-6")
            SlotList.append( t1)
            SlotList.append( t2)
            SlotList.append( t3)
            
        #ftiaxno to domain
        for i in range(self.size):
            lesson = Name_Lessons[i]

            Slot = []
            j = 0 
            while(j < 63):
                
                t = SlotList[j]                
                Slot.append( t)

                t = SlotList[j+1]
                Slot.append( t)
                
                if Lab[i] != "TRUE":
                    t = SlotList[j+2]
                    Slot.append( t)

                j = j + 3

            self.domains[ lesson] = Slot

        #pame na ftiaksoume kai to neig
        for i in range(self.size):
            
            lesson = Name_Lessons[i]
            neig = []
            
            
            for j in range(self.size):

                #an einai to idio mathima
                #continue
                if i == j:
                    continue
                
                lesson_neig = Name_Lessons[j]

                neig.append(lesson_neig)
            
            self.neighbors[lesson] = neig


        super().__init__(self.variables, self.domains, self.neighbors, self.variables_constraits)
    
    #constraints A function f(A, a, B, b) that returns true if neighbors
    #            A, B satisfy the constraint when they have values A=a, B=b
    def variables_constraits( self, A, a, B, b):

        #an einai to idio variable tote return false
        if A == B:
            return False
        
        day_a = a[0]
        day_b = b[0]
        slot_a = a[1]
        slot_b = b[1]
        if (day_a == day_b) and (slot_a == slot_b):
            return False

        index_a = -1
        index_b = -1
        for i in range( self.size):
            lesson = self.NameLessons[i]
            if lesson == A:
                index_a = i
            elif lesson == B:
                index_b = i
        
        if index_a == -1 or index_b == -1:
            return False
        
        #for halfyear
        if self.HalfYear[index_a] == self.HalfYear[index_b]:
            if day_a == day_b:
                return False

        #for hards lessons 2 days
        if self.Hard[index_a] == "TRUE" and self.Hard[index_b] == "TRUE":
            days = abs( day_a - day_b)
            if days < 2:
                return False
        
        #for teacheres
        if self.NameTeachers[index_a] == self.NameTeachers[index_b]:
            if day_a == day_b:
                return False
        
        #for slot_a
        s_a = 0
        if slot_a == "9-12":
            s_a = 1
        elif slot_a == "12-3":
                s_a = 2
        elif slot_a == "3-6":
            s_a = 3
        
        #for slot_b
        s_b = 0
        if slot_b == "9-12":
            s_b = 1
        elif slot_b == "12-3":
                s_b = 2
        elif slot_b == "3-6":
            s_b = 3    
        
        #tsekaro an exei lab to a kai meta to b eksetazetai
        if self.Lab[index_a] == "TRUE":
            if day_a == day_b:
                if s_a + 1 == s_b:
                    return False

        #tsekaro an exei lab to b kai meta to a eksetazetai
        if self.Lab[index_b] == "TRUE":
            if day_a == day_b:
                if s_b + 1 == s_a:
                    return False

        return True


    def display(self, assignment):
        print("The result is:\n\n")
        
        if assignment == None:
            print("We havn't result for exam timetabling")
        else:
            if(len(assignment) == 0):
                print("We havn't result for exam timetabling")
            else:
                for i in assignment:
                    day, slot = assignment.get(i)
                    print(i," Day: ", day, " and Slot: ", slot)
                    
                
        

#############################################################################
##                                                                         ##
##                                                                         ##
##                                kodikas                                  ##    
##                                                                         ##
##                                                                         ##
#############################################################################
if __name__ == '__main__':
    with open("Files/" + "mathimata.csv") as file:
        lines = file.readlines()

    Number_lessons = len(lines) - 1  # beacause the first is information
    Name_Lessons = []
    names_teachers = []
    Eksamino = []
    Duskolo = []
    Lab = []
    is_the_first = True
    for line in lines:

        #beacause the first is information
        if is_the_first == True:
            is_the_first = False
            continue

        line = line.strip()
        length = len(line)
        num_for_other = 0
        previous_start = 0

        for i in range(length):
            if line[i] == ",":
                if num_for_other == 0:
                    if previous_start == i-1:
                        Eksamino.append(line[0])
                    else:
                        eksamino = int(line[previous_start:i-1])
                        Eksamino.append(eksamino)

                elif num_for_other == 1:

                    word = line[previous_start:i]
                    Name_Lessons.append(word)

                elif num_for_other == 2:

                    word = line[previous_start:i]
                    names_teachers.append(word)

                elif num_for_other == 3:

                    duskolo = line[previous_start:i]
                    Duskolo.append(duskolo)

                    lab = line[i+1:length]
                    Lab.append(lab)
                    break

                previous_start = i+1
                num_for_other += 1

    problem = BigProblem(Eksamino, Name_Lessons, names_teachers, Duskolo, Lab)

    csp.backtracking_search(problem)
    problem.display(problem.infer_assignment())
    