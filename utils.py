def word_break(line, characters, actual = 0, inicial = ""):
    temp = inicial
    actual += 1
    validos = [inicial]
    while actual < len(line):
        temp += line[actual]
        if temp in characters:
            validos.append(temp)
        actual += 1
    return max(validos, key = len)