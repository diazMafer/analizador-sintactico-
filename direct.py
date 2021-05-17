from tree import *
from transition import *
from automata import *
import collections

OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']
EPSILON = "ε"



def check(dfa, new_state):
    for state in dfa.states:
        if collections.Counter(state.id) == collections.Counter(new_state):
            return False
    return True

def select(states, id):
    for state in states.states:
        if collections.Counter(state.id) == collections.Counter(id):
            return state
    return False

def estados_importantes(tree):
    nodes = []
    if tree.symbol not in OPERATORS and tree.symbol != EPSILON and tree.left == None and tree.right == None:
        nodes.append(tree)
    if tree.left != None:
        resp = estados_importantes(tree.left)
        for i in resp:
            nodes.append(i)
    if tree.right != None:
        resp = estados_importantes(tree.right)
        for i in resp:
            nodes.append(i)
    return nodes

def nullable(tree):
    if tree.symbol == EPSILON:
        return True
    elif tree.symbol == "ξ":
        if nullable(tree.left) and nullable(tree.right):
            return True
    elif tree.symbol == "*":
        return True
    elif tree.symbol == "|":
        if nullable(tree.left) or nullable(tree.right):
            return True
        else:
            return False
    elif tree.symbol == "ψ":
        if nullable(tree.left):
            return True
        else:
            return False
    elif tree.symbol == "?":
        return True
    return False

def first_pos(tree):
    pos = []
    if tree.symbol in OPERATORS:
        if tree.symbol == "|":
            temp1 = first_pos(tree.left)
            temp2 = first_pos(tree.right)
            for num in temp1:
                pos.append(num)
            for num in temp2:
                pos.append(num)
        elif tree.symbol == "*":
            temp1 = first_pos(tree.left)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == "ξ":
            temp1 = first_pos(tree.left)
            for num in temp1:
                pos.append(num)
            if nullable(tree.left):
                temp2 = first_pos(tree.right)
                for num in temp2:
                    pos.append(num)
        elif tree.symbol == "ψ":
            temp1 = first_pos(tree.left)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == "?":
            temp1 = first_pos(tree.left)
            for num in temp1:
                pos.append(num)
    elif tree.symbol != EPSILON:
        pos.append(tree)
    return pos

def last_pos(tree):
    pos = []
    if tree.symbol in OPERATORS:
        if tree.symbol == "|":
            temp1 = last_pos(tree.left)
            temp2 = last_pos(tree.right)
            for num in temp1:
                pos.append(num)
            for num in temp2:
                pos.append(num)
        elif tree.symbol == "*":
            temp1 = last_pos(tree.left)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == "ξ":
            temp1 = last_pos(tree.right)
            if nullable(tree.right):
                temp2 = last_pos(tree.left)
                for num in temp2:
                    pos.append(num)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == "ψ":
            temp1 = last_pos(tree.left)
            for num in temp1:
                pos.append(num)
        elif tree.symbol == "?":
            temp1 = last_pos(tree.left)
            for num in temp1:
                pos.append(num)
    elif tree.symbol != EPSILON:
        pos.append(tree)
    return pos


def followpos(tree, table):
    if tree.symbol == "ξ": #concatenacion .
        temp1 = last_pos(tree.left)
        temp2 = first_pos(tree.right)
        for i in temp1:
            for num in temp2:
                table[i].append(num)
    elif tree.symbol == "*":
        temp1 = last_pos(tree)
        temp2 = first_pos(tree)
        for i in temp1:
            for num in temp2:
                table[i].append(num)
    elif tree.symbol == "ψ": #suma +
        temp1 = last_pos(tree.left)
        temp2 = first_pos(tree.left)
        for i in temp1:
            for num in temp2:
                table[i].append(num)

    if tree.left != None:
        followpos(tree.left, table)
    if tree.right != None:
        followpos(tree.right, table)

def directo(tree, exp):
    new_tree = Tree()
    new_tree.symbol = "ξ"
    right_t = Tree()
    right_t.symbol = "#"
    new_tree.right = right_t
    new_tree.left = tree

    importantes = estados_importantes(new_tree)
    first = first_pos(new_tree)
    last = last_pos(new_tree)
    table = {}
    for pos in importantes:
        table[pos] = []
    followpos(new_tree, table)

    inicial = first_pos(new_tree)
    final = last_pos(new_tree)
    afd_direct = create(inicial, final, table, exp)
    return afd_direct

def create(inicial, final, table, exp):
    afd_direct = Automata(exp)
    first = State(inicial, len(afd_direct.states))
    afd_direct.states.append(first)
    if final[-1] in first.id:
        first.accept = True
    symbols = []
    for symbol in exp:
        if symbol not in OPERATORS and symbol not in symbols and symbol != EPSILON:
            symbols.append(symbol)
    
    for state in afd_direct.states:
        for symbol in symbols:
            temp = []
            for pos in state.id:
                if pos.symbol == symbol:
                    tos = table[pos]
                    for t in tos:
                        if t not in temp:
                            temp.append(t)
            if check(afd_direct, temp) and temp != []:
                new_state = State(temp, len(afd_direct.states))
                if final[-1] in temp:
                    new_state.accept = True
                afd_direct.states.append(new_state)
                transition1 = Transition(start=state.id,transition=symbol,end=afd_direct.states[-1].id2)
                state.transitions.append(transition1)
            elif temp != []:
                selected = select(afd_direct, temp)
                if selected:
                    transition2 = Transition(start=state.id, transition=symbol, end=selected.id2)
                    state.transitions.append(transition2)
                else:
                    print("No existe nodo con ", temp, " de id")
    return afd_direct