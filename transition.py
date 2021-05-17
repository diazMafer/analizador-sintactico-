"""
    Class transition to model each transition of an automata
    the class consists of the initial state, the label of the transition and the final states
    it conects. 

    The setters and getters are used just for the subsets algorithm to change the subsets to letters
"""
class Transition:
    def __init__(self, start = None, transition = None, end = None):
        self.start = start
        self.transition = transition
        self.end = end
    
    def set_start(self, start):
        self.start = start
    
    def set_end(self, end):
        self.end = end