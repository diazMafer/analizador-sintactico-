from automata import Node

def analyze_productions(productions, tokens, keywords):
    parsed_productions = {}
    string = ""
    def_funct = {}
    all_code = ""
    for p in productions:
        string, name = funct_name(p)
        def_funct[name] = string
        parsed_productions[name] = productions[p]
    for p in parsed_productions:
        if p == "Expr":
            string = def_funct[p]
            stack = production_tokens(parsed_productions[p], parsed_productions, tokens)
            print(p+":\n")
            print(stack)
            print('\n')
            code = clean()
            string += code
            all_code += string + '\n'
        else:
            stack = production_tokens(parsed_productions[p], parsed_productions, tokens)
            print(p+":")
            print(stack)
            print('\n')
            string = def_funct[p]
            code = python_code(stack)
            string += code
            all_code += string + '\n'
    code = write_code(all_code)
    return code
    
def funct_name(id):
    function_list = id.split("<")
    string = ''
    string += "\tdef " + function_list[0] + "(self"
    if len(function_list) > 1:
        for i in function_list[1:]:
            i = i.replace(">", "")
            string +="," + i
    string += "):\n"

    return string, function_list[0]

def first(productions, tokens):
    endings = [")", "}", "]"]
    dict_ntokens = {}
    new_tokens = []
    for l in productions:
        code = productions[l]
        counter = 0
        #check only the firsts that are within the production code
        string = ""
        while counter < len(code):
            string += code[counter]
            if code[counter] == '"':
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            elif string.replace("(","").strip() in tokens: #if the char we are checking is a Node add 
                new_tokens.append(string.replace("(","").strip())
                string = ""
            elif string.replace(")","").replace("|","").strip() in tokens: #if the char we are checking is a Node add 
                new_tokens.append(string.replace(")","").replace("|","").strip())
                string = ""
            counter +=1
        dict_ntokens[l] = new_tokens
        new_tokens = []

    #recursive check productions
        
    #check the firsts that are within the functions to which the production refers
    for l in productions: #l es la produccion que estoy leyendo
        #if it is empty it means that it does not have terminals and searches in the first reference
        if len(dict_ntokens[l]) == 0:
            code = productions[l]
            counter = 0
            for x in productions:
                if str(x) in code:
                    dict_ntokens[l] = dict_ntokens[x]
                    counter += 1
                if counter > 0:
                    break   

    return dict_ntokens

def firstCode(code, productions, dict_ntokens, tokens = []):
    endings = [")", "}", "]"]
    new_tokens = []
    counter = 0
    string = ""
    if "|" in code:
        code = code.strip()
        list1 = code.split("|")
        for x in list1:
            x = x.strip()
            string += x
            if x[0] == '"':                
                new_tokens.append(x[1])
            elif string.replace("(","").strip() in tokens:
                new_tokens.append(string.replace("(","").strip())
                string = ""
            elif string.replace(")","").strip() in tokens:
                new_tokens.append(string.replace(")","").strip())
                string = ""
            else:
                for l in productions: 
                    for n in productions:
                        if str(n) in x:
                            new_tokens = dict_ntokens[n]
                            counter += 1
                        if counter > 0:
                            break
            
    else:
        while counter < len(code):
            if code[counter] == '"':
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            counter +=1
        
        if len(new_tokens) == 0:
            for l in productions: 
                for x in productions:
                    if str(x) in code:
                        new_tokens = dict_ntokens[x]
                        counter += 1
                    if counter > 0:
                        break   
    return new_tokens

def production_tokens(string, production_dict, token_dict):
    skip = 0
    operator = ""
    exclude = ['[', '{', '}', ']', '|', '"', "(",")", "<"]
    current = 0
    stack = []
    firsts_prods = first(production_dict, token_dict)
    ifFlag = False
    for i in range(len(string)-1):
        
        if skip > 0:
            skip -= 1
            continue

        ch = string[i]
        follow_ch = string[i+1]
        #si no esta en los operadores... ni es un espacio
        if ch not in exclude and ch not in firsts_prods:
            operator += ch
        else:
            #revisamos si no existe una produccion ya definida
            is_production = validate_exist(operator.strip(), production_dict)
            operator = operator.replace(")", "")
            is_token = validate_exist(operator.strip(), token_dict)
            poss_follow = check_follow(firsts_prods, ch)
            if poss_follow and follow_ch == '"' and stack[-1].type == "production":
                val = "self.read('" + ch + "')"
                tkk = Node(type="follow", value=val, first=[ch])
                stack.append(tkk)
                
            if is_production:
                if ch == "<":
                    buffer = ""
                    while ch != ">":
                        ch = string[i]
                        buffer += ch
                        i += 1
                    buffer = buffer.replace("<", "(").replace(">", ")")
                    vals = buffer.split("(")[1].replace(")", "")

                    code = vals + " = " + "self." + operator.strip() + buffer
                    tkk = Node(type="production", value=f"{code}", first=None)
                    stack.append(tkk)
                else:
                    tkk = Node(type="production", value=f"self.{operator}()", first=None)
                    stack.append(tkk)
                
                
            if is_token:
                operator = operator.strip()
                tkk = Node(type="Node", value=f"{operator}", first=x)
                stack.append(tkk)
            if ch == "{":
                buffer = ""
                while ch != "}":
                    ch = string[i]
                    buffer += ch
                    i += 1
                buffer = buffer.replace("{", "").replace("}", "")
                first_de_linea = firstCode(buffer, production_dict, firsts_prods)
                tkk = Node(type="while", value="while", first=first_de_linea)
                stack.append(tkk)

            elif ch == "|":
                tkk = Node(type="or", value="|", first=None)
                stack.append(tkk)
            elif ch == "[":
                buffer = ""
                while ch != "]":
                    ch = string[i]
                    buffer += ch
                    i += 1

                x = firstCode(buffer, production_dict, firsts_prods)
                tkk_if = Node(type="if", value="if()", first=x)
                stack.append(tkk_if)
                
            elif ch == "}":
                tkk = Node(type="endwhile", value="", first=None)
                stack.append(tkk)

            elif ch == "]":
                tkk = Node(type="endif", value="", first=None)
                stack.append(tkk)
            operator = ""

        #sacamos codigo.
        if ch == "(" and follow_ch == ".":
            x, skip = get_code(string[i:])
            
            stack.append(Node(type="code", value=x[2:], first=""))

        #if entre parentesis
        elif ch == "(" and follow_ch != "." and follow_ch != '"':
            buffer = ""
            while ch != ")":
                ch = string[i]
                buffer += ch
                i += 1

            x = firstCode(buffer, production_dict, firsts_prods, token_dict)
            tkk_if = Node(type="if op", value="", first=x)
            stack.append(tkk_if)
            ifFlag = True

        #posible end if?
        elif ch == ")" and follow_ch != '"' and ifFlag:
            ifFlag = False
            tkk_end = Node(type="end if op", value="", first=None)
            stack.append(tkk_end)
            
        current += 1


    return stack

def check_follow(first, ch):
    possibleFollow = False
    for i in first:
        for x in i:
            if ch != x:
                possibleFollow = True
    return possibleFollow
            
def python_code(prod_nodes):
    code = ""
    flagWhile = None
    counterPipes = 0
    counterTabs = 2
    for x in range(len(prod_nodes)):
        if prod_nodes[x].type == "while":
            code += (counterTabs*'\t') + "while"
            for i in prod_nodes[x].first:
                code += " self.actual_token.value == " + '"' + i + '"' + "or"
            code = code[:-2]
            code += ":\n"
            flagWhile = x
            counterTabs += 1
        elif prod_nodes[x].type == "if":
            first = prod_nodes[x].first
            if len(first) > 1:
                code += (counterTabs*'\t') + "if self.actual_token.type == " + "'" + first[0] + "': \n"
                counterTabs += 1
                code += (counterTabs*'\t') + "self.read(" + "'" + first[0] + "')\n"
            else:
                code += (counterTabs*'\t') + "if self.actual_token.value == " + "'" + first[0] + "': \n"
                counterTabs += 1
                code += (counterTabs*'\t') + "self.read(" + "'" + first[0] + "')\n"
                
            
        elif prod_nodes[x].type == "endif":
            counterTabs -= 1
        elif prod_nodes[x].type == "code":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_nodes[x].value + "\n"
        elif prod_nodes[x].type == "production":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_nodes[x].value + "\n"
        elif prod_nodes[x].type == "if op":
            flagWhile = x
        elif prod_nodes[x].type == "endwhile":
            flagWhile = None
            counterTabs -= 1
        elif prod_nodes[x].type == "or":
            steps = x - flagWhile + 1
            firstWhile = prod_nodes[flagWhile].first
            for i in firstWhile:
                first = i 
                counterPipes += 1
                if len(firstWhile) <= 2:
                    if counterPipes <= 1:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.actual_token.type == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "',True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.actual_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps-1):
                            innerCode = ""
                            n = prod_nodes[x-c]
                            if n.type != "Node":
                                innerCode = (counterTabs*'\t') + n.value + "\n"
                            codeStack.append(innerCode)
                        counterTabs -= 1
                        reverCodeStack = codeStack.copy()
                        reverCodeStack.reverse()
                        code += ''.join(reverCodeStack)
                    else:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.actual_token.type == " + "'" + first + "': \n"
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.actual_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps):
                            n = prod_nodes[x+c]
                            if n.type != "Node":
                                code += (counterTabs*'\t') + n.value + "\n"
                        counterTabs -= 1
                else:
                    if counterPipes <= 2:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.actual_token.type == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "', True)\n"
                        else: 
                            code += (counterTabs*'\t') + "if self.actual_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps-1):
                            innerCode = ""
                            n = prod_nodes[x-c]
                            if n.type != "Node":
                                innerCode = (counterTabs*'\t') + n.value + "\n"
                            codeStack.append(innerCode)
                        counterTabs -= 1
                        reverCodeStack = codeStack.copy()
                        reverCodeStack.reverse()
                        code += ''.join(reverCodeStack)
                    else:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.actual_token.type ==  " + "'" + first + "': \n"
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.actual_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps):
                            n = prod_nodes[x+c]
                            if n.type != "Node":
                                code += (counterTabs*'\t') + n.value + "\n"
                        counterTabs -= 1
        elif prod_nodes[x].type == "end if op":
            flagWhile = None
        elif prod_nodes[x].type == "Node":
            if flagWhile != None:
                pass
            else:
                if len(prod_nodes[x].value) > 1:
                    code += (counterTabs*'\t') + "self.read('" + prod_nodes[x].value + "', True)\n"
                else:
                    code += (counterTabs*'\t') + "self.read('" + prod_nodes[x].value + "')\n"
                    

    return code

def validate_exist(val, dictionary):
    keys = dictionary.keys()
    isProd = False
    for elem in keys:
        if val == elem:
            isProd = True
            break
    return isProd

def get_code(string):
    counter = 0
    toReturn = ''
    char = string[0]
    delimiterCounter = 0
    skip = False
    while delimiterCounter < 2:
        if skip:
            skip = False
            counter += 1
            continue
        try:
            char = string[counter]
            next_char = string[counter+1]
        except:
            toReturn = ""
            counter = 0
            break
        if (char == "." and next_char == ")"):
            break
        toReturn += char
        counter += 1
    return toReturn, counter + 2

def write_code(code):
    output = open("./scanners/" + "prueba_prod" + ".py", "w+")
    clase="""
class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.id_token = 0
		self.actual_token = self.tokens[self.id_token]
		self.last_token = ''

	def advance( self ):
		self.id_token += 1
		if self.id_token < len(self.tokens):
			self.actual_token = self.tokens[self.id_token]
			self.last_token = self.tokens[self.id_token - 1]

	def read(self, item, type = False):
		if type:
			if self.actual_token.type == item:
				self.advance()
				return True
			else:
				print ("Error sintactico esperando " + str(item))
				return False
		else:
			if self.actual_token.value == item:
				self.advance()
				return True
			else:
				print ("Error sintactico esperando " + str(item))
				return False
"""
    clase += code 
    output.write(clase)
    return clase

def clean():
    code ='''
\t\twhile self.actual_token.type == 'number' or self.actual_token.type == 'decnumber' or self.actual_token.value == '-' or self.actual_token.value == '(':
\t\t\tself.Stat()
\t\t\tself.read(";")
\t\tself.read(".")
    '''
    return code