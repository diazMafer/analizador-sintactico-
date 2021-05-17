
OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']
UNITARY = ['*', 'ψ', '?']

"""
    Class tree to simulate a tree, each node of the tree contains
    the symbol and the operator or symbol that it is on the right and in the left
"""

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.symbol = None

"""
    Method to generate the tree to use in the direct algorithm
    @param expression in infix
    @return tree
"""
def generate_tree(expression):
    output = []
    stack = []
    i = 0
    
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        elif expression[i] == "(":
            stack.append(expression[i])    
        elif expression[i] not in OPERATORS:
            val = ""
            while (i < len(expression)) and expression[i] not in OPERATORS:
                val = str(val) + expression[i]
                i -= -1
            tree = Tree()
            tree.symbol = val
            output.append(tree)
            i -= 1
        elif expression[i] == ")":
            while len(stack) != 0 and stack[-1] != "(":
                val2 = output.pop()
                val1 = output.pop()
                op = stack.pop()
                tree = Tree()
                tree.symbol = op
                tree.left = val1
                tree.right = val2
                output.append(tree)
            stack.pop()
        else:
            if (expression[i] in UNITARY):
                op = expression[i]
                val = output.pop()
                tree = Tree()
                tree.symbol = op
                tree.left = val
                tree.right = None
                output.append(tree)
            else:
                while (len(stack) != 0  and stack[-1] != '('):
                    op = stack.pop()
                    val2 = output.pop()
                    val1 = output.pop()
                    tree = Tree()
                    tree.symbol = op
                    tree.left = val1
                    tree.right = val2
                    output.append(tree)
                stack.append(expression[i])
        i -= -1
    
    while(len(stack) != 0):
        val2 = output.pop()
        val1 = output.pop()
        op = stack.pop()
        tree = Tree()
        tree.symbol = op
        tree.left = val1
        tree.right = val2
        output.append(tree)
        if (len(output) == 1):
            return output[-1]
    return output[-1]