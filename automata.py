"""
    Class to model an automata
    initial state, final state, alphaber, transitions
"""
class Automata:
    def __init__(self, exp):
        self.id = exp
        self.states = []

"""
    Class to model an state 
    the class is used only in direct method 
"""
class State:
    def __init__(self, num, num2):
        self.id = num
        self.id2 = num2
        self.transitions = []
        self.accept = False
    pass