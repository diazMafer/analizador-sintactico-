from scanner import get_productions
from tree import generate_tree
from direct import directo
from utils import word_break
from automata import Token

#documentacion from page 6 of pdf https://ssw.jku.at/Research/Projects/Coco/Doc/UserManual.pdf 
RESERVERD_KEYWORDS = ["ANY", "CHARACTERS", "COMMENTS", "COMPILER", "CONTEXT",
"END", "FROM", "IF", "IGNORE", "IGNORECASE", "NESTED", "out", "PRAGMAS",
"PRODUCTIONS", "SYNC", "TO", "TOKENS", "WEAK"]
OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '('] #or y concatenacion nueva definicion para no entorpecer con el . de characters, tokens o mas
OPS  = ["[", "{", "|", "("]
ENDING = ["]", "}", "|", ")", "\n", '"']

def analized_chars(characters):
    character_parsed = {}
    for c in characters:
        temp_string = ""
        flag = False
        i = 0
        chars_regex = ""
        while i < len(characters[c]):
            if characters[c][i] == '"' or characters[c][i] == "'":
                flag = not flag
                if not flag:
                    temp_string = temp_string[:-1] + ")"
                    chars_regex += temp_string 
                    temp_string = ""
                else:
                    temp_string += "("
            elif flag:
                temp_string += characters[c][i] + "|"
            elif characters[c][i] == "+":
                chars_regex += "|"
            elif temp_string + characters[c][i] in character_parsed:
                chars_regex += character_parsed[temp_string+characters[c][i]]
                temp_string = ""
            elif temp_string == ".":
                if characters[c][i] == ".":
                    start = chars_regex[-2]
                    finish = ""
                    while i < len(characters[c]):
                        if characters[c][i] == "'":
                            break
                        i += 1
                    finish = characters[c][i + 1]
                    j = ord(start)
                    while j < ord(finish):
                        chars_regex += "|" + chr(j)
                        j += 1
                    chars_regex += "|" + finish

            elif temp_string == "CHR(":
                number = ""
                while i < len(characters[c]):
                    if characters[c][i] == ")":
                        break
                    elif characters[c][i] == " ":
                        pass
                    else:
                        number += characters[c][i]
                    i += 1
                number = int(number)
                symbol = chr(number)
                chars_regex += symbol
                temp_string = ""
            else:
                temp_string += characters[c][i]
            i += 1
        character_parsed[c] = "(" +  chars_regex + ")"
    return character_parsed


def analyzed_keywords(keywords,character_parsed):
    keywords_parsed = {}
    for k in keywords:
        word = keywords[k][:-1]
        i = 0
        temp = ""
        flag = False
        while i < len(word):
            if word[i] == '"':
                flag = not flag
                if not flag:
                    temp = temp[:-1] +  ")"
                else:
                    temp += "("
            else:
                temp += word[i] + "ξ"
            i += 1
        keywords_parsed[k] = temp
    return keywords_parsed


def analyzed_tokens(tokens, characters):
    tokens_parse_lines = {}
    for t in tokens:
        token = tokens[t]
        i = 0
        temp = ""
        individual_regex = ""
        flag = False
        while i < len(token):
            temp += token[i]
            if temp in characters:
                og = temp
                temp = word_break(token, characters, i, temp)
                if og != temp:
                    i += len(temp) - len(og)
                if flag:
                    individual_regex += characters[temp] + ")*"
                else:
                    individual_regex += characters[temp]
                temp = ""
            if temp == "|":
                individual_regex = individual_regex[:-2] + "|"
                temp = ""
            if temp == "{":
                flag = not flag
                individual_regex += "ξ("
                temp = ""
            if temp == "}" and flag:
                flag = not flag
                temp = ""
            if temp == "[":
                second_flag = True
                if individual_regex != "":
                    individual_regex += "ξ"
                individual_regex += "("
                temp = ""
            if temp == "]":
                second_flag = False
                individual_regex += "?)ξ"
                temp = ""
            if temp == "(":
                individual_regex += "("
                temp = ""
            if temp == ")":
                individual_regex += ")"
                temp = ""
            if temp == '"':
                inner = ""
                i += 1
                while i < len(token):
                    if token[i] == '"':
                        break
                    inner += token[i]
                    i += 1
                if individual_regex != "" :
                    individual_regex += "ξ(" + inner + ")"
                else:
                    individual_regex += "(" + inner + ")"
                if token[i + 1] != "" and token[i + 1] != "\n" and token[i + 1] != ".":
                    individual_regex += "ξ"
                temp = ""
            if temp == "CHR(":
                number = ""
                if tokens[t][i+3] == "." and i+4 <= len(tokens[t]):
                    while i < len(tokens[t]):
                        if tokens[t][i] == ")":
                            break
                        elif tokens[t][i] == " ":
                            pass
                        elif tokens[t][i] == "(":
                            pass
                        else:
                            number += tokens[t][i]
                        i += 1
                    start = number
                    i = i+6
                    finish = ""
                    while i < len(tokens[t]):
                        if tokens[t][i] == ")":
                            break
                        elif tokens[t][i] == " ":
                            pass
                        elif tokens[t][i] == "(":
                            pass
                        else:
                            finish += tokens[t][i]
                        i += 1
                    finish = int(finish)

                    j = int(start)
                    while j < finish:
                        individual_regex += chr(j) + "|"
                        j += 1
                    individual_regex +=  chr(finish)
                    temp = ""
                else:
                    while i < len(tokens[t]):
                        if tokens[t][i] == ")":
                            break
                        elif tokens[t][i] == " ":
                            pass
                        elif tokens[t][i] == "(":
                            pass
                        else:
                            number += tokens[t][i]
                        i += 1
                    number = int(number)
                    symbol = chr(number)
                    individual_regex += symbol
                    temp = ""
            i += 1
        if individual_regex[-1] in OPERATORS:
            individual_regex = individual_regex[:-1]
        tokens_parse_lines[t] = individual_regex
    return tokens_parse_lines


def analyze_productions(productions, tokens, keywords):
    parsed_productions = {}
    string = ""
    for p in productions:
        string, name = funct_name(p)
        parsed_productions[name] = productions[p]
        #stack = second(productions[p])

    for p in parsed_productions:
        stack = production_tokens(parsed_productions[p], parsed_productions, tokens)
        print(stack)
        code_prods(stack)
        #print(new)
    

def funct_name(id):
    #position 0 is always the name of the function, if len > 1 then has parameters
    function_list = id.split("<")
    string = ''
    string += "\tdef " + function_list[0] + "(self"
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
            elif string.strip() in tokens:
                new_tokens.append(string.strip())
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

def firstCode(code, productions, dict_ntokens):
    print(dict_ntokens)
    endings = [")", "}", "]"]
    new_tokens = []
    counter = 0
    if "|" in code:
        code = code.strip()
        list1 = code.split("|")
        for x in list1:
            x = x.strip()
            if x[0] == '"':                
                new_tokens.append(x[1])
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
    exclude = ['[', '{', '}', ']', '|', '"', "(", "<"]
    current = 0
    stack = []
    symb_to_ignore = first(production_dict, token_dict)
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
            is_token = check_dict(operator.strip(), token_dict)

            if is_production:
                if ch == "<":
                    buffer = ""
                    while ch != ">":
                        ch = string[i]
                        buffer += ch
                        i += 1
                    buffer = buffer.replace("<", "(").replace(">", ")")
                    #(result1,result2)
                    #["", "result,result2)"]
                    #result,result2
                    value = buffer.split("(")[1].replace(")","")
                    toApend = value + " = " + "self." + operator.strip() + buffer
                    tkk = Token(type="PRODUCTION", value=toApend, first=None)
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
                tkk = Token(type="WHILE", value="while First()", first=first_de_linea)
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
            elif ch == "(" and follow_ch != ".":
                buffer = ""
                while ch != ")":
                    ch = string[i]
                    buffer += ch
                    i += 1

                x = firstCode(buffer, production_dict, symb_to_ignore)
                tkk_if = Token(type="IFP", value="", first=x)
                stack.append(tkk_if)
            elif ch == ")" and string[i-1] != ".":
                tkk_if = Token(type="ENDIFP", value="", first=x)
                stack.append(tkk_if)

            
            operator = ""
        #sacamos codigo.
        if ch == "(" and follow_ch == ".":
            x, skip = get_code(string[i:])
            stack.append(Token(type="CODE", value=x[2:], first=None))
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
            code += (counterTabs*'\t') + "if lastToken == " + "'" + first[0] + "': \n"
            counterTabs += 1
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
                    code += (counterTabs*'\t') + "if lastToken == " + "'" + first + "': \n"
                    codeStack = []
                    counterTabs += 1
                    for c in range(1,steps-1):
                        innerCode = ""
                        n = prod_tokens[x-c]
                        innerCode = (counterTabs*'\t') + n.value + "\n"
                        codeStack.append(innerCode)
                    counterTabs -= 1
                    reverCodeStack = codeStack.copy()
                    reverCodeStack.reverse()
                    code += ''.join(reverCodeStack)
                else:
                    code += (counterTabs*'\t') + "if lastToken == " + "'" + first + "': \n"
                    counterTabs += 1
                    for c in range(1,steps):
                        n = prod_tokens[x+c]
                        code += (counterTabs*'\t') + n.value + "\n"
                    counterTabs -= 1

    print("code generado")
    print(code)

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
    

def make_tree(keyword_parse_lines, token_parse_lines):
    final_regex = ""
    dfas = {}
    for keyword in keyword_parse_lines:
        final_regex += "(" + keyword_parse_lines[keyword] + ")" + "|"
        tree = generate_tree(keyword_parse_lines[keyword])
        dfas[keyword] = directo(tree, keyword_parse_lines[keyword])

    for token in token_parse_lines:
        final_regex += "(" + token_parse_lines[token] +")" + "|"
        tree = generate_tree(token_parse_lines[token])
        dfas[token] = directo(tree, token_parse_lines[token])
    final_regex = final_regex[:-1]
    tree = generate_tree(final_regex)
    return dfas, final_regex

def make_one(final_regex):
    tree = generate_tree(final_regex)
    final_dfa = directo(tree, final_regex)
    return final_dfa

def analyze(name, characters, keywords, tokens, productions):
    character_parsed = analized_chars(characters)
    keyword_parsed = analyzed_keywords(keywords, character_parsed)
    token_parsed = analyzed_tokens(tokens, character_parsed)
    productions_parsed = analyze_productions(productions, token_parsed, keyword_parsed)
    #dfas, final_regex = make_tree(keyword_parsed, token_parsed)
    #final_dfa = make_one(dfas, final_regex)


