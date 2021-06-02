from automata import Token

def analyze_productions(productions, tokens, keywords):
    parsed_productions = {}
    string = ""
    def_funct = {}
    all_code = ""
    for p in productions:
        string, name = funct_name(p)
        def_funct[name] = string
        parsed_productions[name] = productions[p]
        #stack = second(productions[p])

    for p in parsed_productions:
        if p == "Expr":
            string = def_funct[p]
            stack = production_tokens(parsed_productions[p], parsed_productions, tokens)
            print(stack)
            code = clean()
            string += code
            print(string)
            all_code += string + '\n'
        else:
            stack = production_tokens(parsed_productions[p], parsed_productions, tokens)
            print(stack)
            string = def_funct[p]
            code = code_prods(stack)
            string += code
            print(string)
            all_code += string + '\n'
    write_code(all_code)
    
def funct_name(id):
    #position 0 is always the name of the function, if len > 1 then has parameters
    function_list = id.split("<")
    string = ''
    string += "def " + function_list[0] + "(self"
    if len(function_list) > 1:
        for i in function_list[1:]:
            i = i.replace(">", "")
            string +="," + i
    string += "):\n"

    return string, function_list[0]

def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

def first(productions, tokens):
    endings = [")", "}", "]"]
    #productions = {'expr': 'codigo'}
    #dict_ntokens = {'expr': [+, *]}
    #expr hace refencia a term y term tiene -, / 
    dict_ntokens = {}
    new_tokens = []

    #AQUI REVISAMOS LOS FIRST QUE ESTAN DIRECTAMENTE EN LA FUNCION ENTIENDASE LOS QUE ESTAN DENTRO DE "" O TOKENS
    for l in productions:
        code = productions[l]
        counter = 0
        #revise unicamente los ")" que estan dentro del codio de la produccion 
        string = ""
        while counter < len(code):
            string += code[counter]
            if code[counter] == '"':
                #OJO LO MEJOR ES ANALIZAR POR EL | Y HACER SPLIT PARA SABER CUANTOS HAY EN EL PRIMERO 
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            elif string.replace("(","").strip() in tokens:
                new_tokens.append(string.replace("(","").strip())
                string = ""
            counter +=1
        dict_ntokens[l] = new_tokens
        new_tokens = []

    #REVISAMOS LOS RECURSIVOS QUE SE ENCUENTRAN EN OTRAS PRODUCCIONES A LAS QUE SE HACEN REFERENCIA EN LA QUE SE ESTA EVALUANDO
        
    #revisar los ")" que esten dentro de las funciones a las que haga referencia la produccion
    for l in productions: #l es la produccion que estoy leyendo
        #si esta vacio significa que no tiene terminales y busca en la primera referencia
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
    print(code)
    print(dict_ntokens)
    endings = [")", "}", "]"]
    new_tokens = []
    counter = 0
    string = ""
    if "|" in code:
        code = code.strip()
        list1 = code.split("|")
        print(list1)
        for x in list1:
            print(x)
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
                for l in productions: #l es la produccion que estoy leyendo
                    for n in productions:
                        if str(n) in x:
                            new_tokens = dict_ntokens[n]
                            counter += 1
                        if counter > 0:
                            break
            
    else:
        while counter < len(code):
            if code[counter] == '"':
                #OJO LO MEJOR ES ANALIZAR POR EL | Y HACER SPLIT PARA SABER CUANTOS HAY EN EL PRIMERO 
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            counter +=1
        
        if len(new_tokens) == 0:
            #revisar los ")" que esten dentro de las funciones a las que haga referencia la produccion
            for l in productions: #l es la produccion que estoy leyendo
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
    symb_to_ignore = first(production_dict, token_dict)
    ifFlag = False
    for i in range(len(string)-1):
        
        if skip > 0:
            skip -= 1
            continue

        ch = string[i]
        follow_ch = string[i+1]
        #si no esta en los operadores... ni es un espacio
        if ch not in exclude and ch not in symb_to_ignore:
            operator += ch
        else:
            #revisamos si no existe una produccion ya definida
            is_production = check_dict(operator.strip(), production_dict)
            operator = operator.replace(")", "")
            is_token = check_dict(operator.strip(), token_dict)
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
                    tkk = Token(type="PRODUCTION", value=f"{code}", first=None)
                    stack.append(tkk)
                else:
                    tkk = Token(type="PRODUCTION", value=f"self.{operator}()", first=None)
                    stack.append(tkk)
                
                
            if is_token:
                operator = operator.strip()

                #OJO HAY QUE HACER UNA FUNCION QUE LOS IDENTIFIQUE RECURSIVAMENTE I.E AUTOMATA
                x = token_dict[operator]
                x = x.replace("(", "").replace(")", "")
                x = x.split("ξ")[0]
                x = x.split("|")
                tkk = Token(type="TOKEN", value=f"{operator}", first=x)
                stack.append(tkk)
            if ch == "{":
                buffer = ""
                while ch != "}":
                    ch = string[i]
                    buffer += ch
                    i += 1
                buffer = buffer.replace("{", "").replace("}", "")
                first_de_linea = firstCode(buffer, production_dict, symb_to_ignore)
                tkk = Token(type="WHILE", value="while", first=first_de_linea)
                stack.append(tkk)

            elif ch == "|":
                tkk = Token(type="PIPE", value="|", first=None)
                stack.append(tkk)
            elif ch == "[":
                buffer = ""
                while ch != "]":
                    ch = string[i]
                    buffer += ch
                    i += 1

                x = firstCode(buffer, production_dict, symb_to_ignore)
                tkk_if = Token(type="IF", value="if()", first=x)
                stack.append(tkk_if)
                
            elif ch == "}":
                tkk = Token(type="ENDWHILE", value="", first=None)
                stack.append(tkk)

            elif ch == "]":
                tkk = Token(type="ENDIF", value="", first=None)
                stack.append(tkk)
            operator = ""

        #sacamos codigo.
        if ch == "(" and follow_ch == ".":
            x, skip = get_code(string[i:])
            
            stack.append(Token(type="CODE", value=x[2:], first=""))

        #if entre parentesis
        elif ch == "(" and follow_ch != "." and follow_ch != '"':
            buffer = ""
            while ch != ")":
                ch = string[i]
                buffer += ch
                i += 1

            x = firstCode(buffer, production_dict, symb_to_ignore, token_dict)
            tkk_if = Token(type="IFP", value="", first=x)
            stack.append(tkk_if)
            ifFlag = True

        #posible end if?
        elif ch == ")" and follow_ch != '"' and ifFlag:
            ifFlag = False
            tkk_end = Token(type="ENDIFP", value="", first=None)
            stack.append(tkk_end)
            
        current += 1


    return stack

def code_prods(prod_tokens):
    code = ""
    flagWhile = None
    counterPipes = 0
    counterTabs = 1
    for x in range(len(prod_tokens)):
        if prod_tokens[x].type == "WHILE":
            code += (counterTabs*'\t') + "while"
            for i in prod_tokens[x].first:
                code += " self.expect(" + '"' + i + '"' + ") or"
            code = code[:-2]
            code += ":\n"
            flagWhile = x
            counterTabs += 1
        elif prod_tokens[x].type == "IF":
            first = prod_tokens[x].first
            code += (counterTabs*'\t') + "if self.expect(" + "'" + first[0] + "'): \n"
            counterTabs += 1
            code += (counterTabs*'\t') + "self.read(" + "'" + first[0] + "')\n"
        elif prod_tokens[x].type == "ENDIF":
            counterTabs -= 1
        elif prod_tokens[x].type == "CODE":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_tokens[x].value + "\n"
        elif prod_tokens[x].type == "PRODUCTION":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_tokens[x].value + "\n"
        elif prod_tokens[x].type == "IFP":
            flagWhile = x
        elif prod_tokens[x].type == "ENDWHILE":
            flagWhile = None
            counterTabs -= 1
        elif prod_tokens[x].type == "PIPE":
            steps = x - flagWhile + 1
            firstWhile = prod_tokens[flagWhile].first
            for i in firstWhile:
                first = i 
                counterPipes += 1
                if counterPipes <= 1:
                    code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "'): \n"
                    codeStack = []
                    counterTabs += 1
                    code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                    for c in range(1,steps-1):
                        innerCode = ""
                        n = prod_tokens[x-c]
                        if n.type != "TOKEN":
                            innerCode = (counterTabs*'\t') + n.value + "\n"
                        codeStack.append(innerCode)
                    counterTabs -= 1
                    reverCodeStack = codeStack.copy()
                    reverCodeStack.reverse()
                    code += ''.join(reverCodeStack)
                else:
                    code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "'): \n"
                    counterTabs += 1
                    code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                    for c in range(1,steps):
                        n = prod_tokens[x+c]
                        if n.type != "TOKEN":
                            code += (counterTabs*'\t') + n.value + "\n"
                    counterTabs -= 1
        elif prod_tokens[x].type == "ENDIFP":
            flagWhile = None
        elif prod_tokens[x].type == "TOKEN":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + "self.read('" + prod_tokens[x].value + "')\n"

    return code

def check_dict(val, dictionary):
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
    output.write(code)

def clean():
    code = """
    while self.expect('number', True) or self.expect('decnumber', True) or self.expect('-') or self.expect('('):
        self.Stat()
        self.read(";")
    self.read(".")
    """
    return code