
def first(productions):
    endings = [")", "}", "]"]
    #productions = {'expr': 'codigo'}
    #dict_ntokens = {'expr': [+, *]}
    #expr hace refencia a term y term tiene -, / 
    dict_ntokens = {}
    new_tokens = []
    for l in productions:
        code = productions[l]
        counter = 0
        #revise unicamente los ")" que estan dentro del codio de la produccion 
        while counter < len(code):
            if code[counter] == '"':
                #OJO LO MEJOR ES ANALIZAR POR EL | Y HACER SPLIT PARA SABER CUANTOS HAY EN EL PRIMERO 
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            counter +=1
        dict_ntokens[l] = new_tokens
        new_tokens = []
        
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


def production_tokens(key, string, production_dict, token_dict):
    tokens = []
    skip = 0
    operator = ""
    exclude = ['[', '{', '}', ']', '|', '"', "(", "<"]
    current = 0
    counter = 0
    stack = []
    symb_to_ignore = first(production_dict)
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
                #stack[-1] is while
                """ if stack[-1].type == "WHILE":
                    #llamamos a first
                    stack[-1].identifier= symb_to_ignore[operator.strip()]"""
                print("found production!")
                tkk = Token.Tokenizer(type_t="PRODUCTION", value=f"self.{operator}")
                stack.append(tkk)

                #def first() -> array -> stack[-1].extend(first())
                

            if is_token:
                print("found token!")


            if ch == "{":

                buffer = ""
                while ch != "}":
                    ch = string[i]
                    buffer += ch
                    i += 1
                buffer = buffer.replace("{", "").replace("}", "")
                first_de_linea = firstCode(buffer, production_dict, symb_to_ignore)
                tkk = Token.Tokenizer(type_t="WHILE", value="while First()", identifier=[])
                tkk.identifier = first_de_linea
                stack.append(tkk)

            elif ch == "|":
                
                print("found pipe")
                print(operator)
            elif ch == "[":
                buffer = ""
                while ch != "]":
                    ch = string[i]
                    buffer += ch
                    i += 1

                x = firstCode(buffer, production_dict, symb_to_ignore)
                tkk_if = Token.Tokenizer(type_t="IF", value="if()", identifier=[])
                tkk_if.identifier = x
                stack.append(tkk_if)
                
            elif ch == "}":
                print("found end while")

            elif ch == "]":
                print("found end optional")
            
            
            operator = ""

        #sacamos codigo.
        if ch == "(" and follow_ch == ".":
            x, skip = get_code(string[i:])
            print('found code', x[2:])
            first_de_linea = firstCode(string[i:] production_dict, symb_to_ignore)
            stack.append(Token.Tokenizer(type_t="CODE", value=x[2:], identifier=first_de_linea))

        current += 1


    return stack

def check_dict(val, dictionary):
    keys = dictionary.keys()
    isProd = False
    for elem in keys:
        if val == elem:
            isProd = True
            break
    return isProd

def get_code(body):
    counter = 0
    temp = ""
    while (body[counter] != ".") or (body[counter+1] != ")"):
        temp += body[counter]
        counter += 1
    return temp