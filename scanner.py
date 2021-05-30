

COMMENTS = ["/*", "*/", "//"]

no_keyword = False

def read_word(file, actual):
    word = ""
    while actual < len(file):
        if (file[actual] == " " or file[actual] == "\n") and (len(word) > 0):
            break
        elif file[actual] == " " or file[actual] == "\n":
            actual += 1
        else:
            word += file[actual]
            actual += 1
    return word, actual

def scan(file):
    actual = 0
    characters = []
    keywords = []
    tokens = []
    productions = []
    temp_word = ""
    while True:
        temp_word, actual = read_word(file, actual)
        if temp_word == "COMPILER":
            name, actual = get_compiler(file, actual)
        if temp_word == "CHARACTERS":
            characters, actual = get_chars(file, actual)
        if not no_keyword and temp_word == "KEYWORDS":
            keywords, actual = get_keywords(file, actual)
        if temp_word == "TOKENS":
            tokens, actual = get_tokens(file, actual)
        if temp_word == "PRODUCTIONS":
            productions, actual = get_productions(file, actual)
        if temp_word == "END":
            final = get_end(file, actual, name)
            if final:
                break
            else:
                print("name does not match")
                break
    
    print(name)
    print(characters)
    print(keywords)
    print(tokens)
    return name, characters, keywords, tokens, productions

def get_compiler(file, actual):
    actual += 1 
    name, actual = read_word(file, actual)
    return name, actual

def get_chars(file, actual):
    actual += 1
    temp = ""
    characters = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "KEYWORDS":
            actual -= 8
            break
        if temp == "TOKENS":
            no_keyword = True
            actual -= 6
            break
        line += temp
        if line[-1] == "." and line[-2] != ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                characters[temp_id] = temp_values
                line =  ""
            else:
                print("= not found in chars")
    return characters, actual

def get_keywords(file, actual):
    actual += 1
    temp = ""
    keywords = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "TOKENS":
            actual -= 6
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                keywords[temp_id] = temp_values
                line =  ""
            else:
                print("= not found in keywords")
    return keywords, actual

def get_tokens(file, actual):
    actual += 1
    temp = ""
    tokens = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "PRODUCTIONS":
            actual -= 11
            break
        if temp == "END":
            actual -= 3
            break
        line += temp
        if line[-1] == "." and line[-2] != ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                tokens[temp_id] = temp_values
                line =  ""
            else:
                print("= not found in tokens")
    return tokens, actual

def get_productions(file, actual):
    actual += 1
    temp = ""
    productions = {}
    temp_id = ""
    temp_values = ""
    while actual < len(file):
        temp += file[actual]
        if temp[-1] == "."  and temp[-2] != "(" and (file[actual + 1] == " " or file[actual+1] == "\n"):
            temp_id = temp.split("=", 1)[0]
            temp_values = temp.split("=", 1)[1]
            temp_id = temp_id.replace("\n", "")
            temp_id = temp_id.replace("\t", "")
            temp_id = temp_id.replace(" ", "")
            temp_values = temp_values.replace("\t", "")
            productions[temp_id] = temp_values
            temp = ""
       
        if "\nEND" in temp:
            actual -= 3
            temp = ""
            break
        actual += 1
    return productions, actual

def get_end(file, actual, name):
    actual += 1
    end_name, actual = read_word(file, actual)
    if end_name == name:
        return True
    return False


if __name__ == "__main__":
    file = open("input/Ejemplo.txt")
    content = file.read()
    scanner(content)
    file.close()