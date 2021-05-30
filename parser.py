from tree import generate_tree
from direct import directo
from utils import word_break

#documentacion from page 6 of pdf https://ssw.jku.at/Research/Projects/Coco/Doc/UserManual.pdf 
RESERVERD_KEYWORDS = ["ANY", "CHARACTERS", "COMMENTS", "COMPILER", "CONTEXT",
"END", "FROM", "IF", "IGNORE", "IGNORECASE", "NESTED", "out", "PRAGMAS",
"PRODUCTIONS", "SYNC", "TO", "TOKENS", "WEAK"]
OPERATORS = ['|', 'ξ'] #or y concatenacion nueva definicion para no entorpecer con el . de characters, tokens o mas

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

def make_one(dfas, final_regex):
    tree = generate_tree(final_regex)
    final_dfa = directo(tree, final_regex)
    return final_dfa

def analyze(name, characters, keywords, tokens):
    character_parsed = analized_chars(characters)
    keyword_parsed = analyzed_keywords(keywords, character_parsed)
    token_parsed = analyzed_tokens(tokens, character_parsed)
    dfas, final_regex = make_tree(keyword_parsed, token_parsed)
    final_dfa = make_one(dfas, final_regex)

    print("Characters parse:")
    print(character_parsed)
    print("Keywords parsed: ")
    print(keyword_parsed)
    print("Tokens parse:")
    print(token_parsed)

    return final_dfa, dfas

