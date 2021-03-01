# KONSTANTINOS NIKOLETOS
# 1115201700104
# priorityQueue.py


# ------------------ Class Stack ------------------ #

class Stack:

    def __init__(self):

        self._count=0       # Counter for items inside the stack
        self._list=[]       # Using a list for implementing the stack
                            # Using _ makes tha data private


    def Pop(self):

        if self._count==0:
            return None     # If stack Empty

        self._count -= 1
        return self._list.pop(0)


    def Push(self,item):

        self._count += 1
        self._list.insert(0,item)

        return None

    def Empty(self):

        return (self._count == 0)


# ------------------ Body of the programm ------------------ #



def Match(a,b):         # Function to match opened and closed parenthesis

    if (a=='(' and b==')') or (a=='{' and b=='}') or (a=='[' and b==']') :
        return True
    else :
        return False



def WeightedBrackets():

    stack = Stack()
    brackets= raw_input("Enter brackets: " )    # raw because I wanted the whole string
    for b in brackets:

        if (b == '(' or b== '[' or b=='{'):
            stack.Push(b)
        elif ( b == ')' or b == ']' or b == '}' ):
            if stack.Empty() == 0:
                char = stack.Pop()
                flag= Match(char,b)
                if flag == 0:
                    print "Mismached parenthesis %c and %c " %(char,b)
                    return None
            else:
                print "More closed than opened parenthesis!"
                return None
        else :
            print "Only brackets!"
            return None

    if stack.Empty() :
        print "Weighted!"
    else:
        print "More opened than closed parenthesis!"



    return None

#--------------- Call of the function ---------------------#

WeightedBrackets()
