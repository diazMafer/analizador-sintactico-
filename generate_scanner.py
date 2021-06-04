# file to create another file

def create(dfa, extras, name, code):
    i = 0
    output = open("./scanners/" + name + ".py", "w+")
    output.write(code)
    output.write("#file to test\n\n")
    #output.write("from libs import evaluate\n")
    output.write("import collections\n")
    output.write("EPSILON = 'ε'\n")


    output.write("class Automata:\n\tdef __init__(self, exp):\n\t\tself.id = exp \n\t\tself.states = []\n\n")
    output.write("class Token:\n\tdef __init__(self, type, value):\n\t\tself.type = type \n\t\tself.value = value\n\n")
    output.write("class State: \n\tdef __init__(self,num):\n\t\tself.id = num\n\t\tself.transitions = []\n\t\tself.accept = False \n\n")
    output.write("class Transition: \n\tdef __init__(self,sym,to):\n\t\tself.symbol = sym\n\t\tself.to = to\n\n")

    output.write("def is_in_language(automata, expresion):\n")
    output.write("  if expresion == ' ' or expresion == '':\n")
    output.write("      expresion = EPSILON\n")
    output.write("  actual = [0]\n")
    output.write("  actual = cerradura(automata, actual)\n")
    output.write("  i = 0\n")
    output.write("  while True:\n")
    output.write("      temp = []\n")
    output.write("      for num in actual:\n")
    output.write("          for transition in automata.states[num].transitions:\n")
    output.write("              if transition.symbol == expresion[i] and transition.to not in temp:\n")
    output.write("                  temp.append(transition.to)\n")
    output.write("      i += 1\n")
    output.write("      temp = cerradura(automata, temp)\n")
    output.write("      if not temp and expresion == EPSILON:\n")
    output.write("          break\n")
    output.write("      actual = temp.copy()\n")
    output.write("      if i > len(expresion)-1:\n")
    output.write("          break\n")
    output.write("  for id in actual:\n")
    output.write("      if automata.states[id].accept:\n")
    output.write("          return True\n")
    output.write("  return False\n\n")

    output.write("def cerradura(automata, actual):\n")
    output.write("  for num in actual:\n")
    output.write("      for transition in automata.states[num].transitions:\n")
    output.write("          if transition.symbol == EPSILON and transition.to not in actual:\n")
    output.write("              actual.append(transition.to)\n")
    output.write("  return actual\n\n")


    output.write("def read_word(file, actual):\n")
    output.write("  temp_word = ''\n")
    output.write("  while actual < len(file):\n")
    output.write("      if(file[actual] == ' ' or file[actual] == '\\n') and (len(temp_word)>0):\n")
    output.write("          break\n")
    output.write("      elif file[actual] == ' ' or file[actual] == '\\n':\n")
    output.write("          actual += 1\n")
    output.write("      else:\n")
    output.write("          temp_word += file[actual]\n")
    output.write("          actual += 1\n")
    output.write("  return temp_word, actual\n\n")


    output.write("def word_break(file, automata0, actual = 0):\n")
    output.write("  temp = ''\n")
    output.write("  validos = []\n")
    output.write("  while actual < len(file):\n")
    output.write("      temp += file[actual]\n")
    output.write("      if is_in_language(automata0, temp):\n")
    output.write("          validos.append(temp)\n")
    output.write("      elif len(temp) == 1  and is_in_language(automata0, str(ord(temp))):\n")
    output.write("          validos.append(temp)\n")
    output.write("      actual += 1\n")
    output.write("  if validos:\n")
    output.write("      return max(validos, key = len)\n")
    output.write("  return False\n")

    
    
    output.write("def main():\n")
    
    output.write("  automatas = []\n")
    write_automata(dfa, i, output)
    i += 1
    for automata in extras:
        write_automata(extras[automata], i, output, automata)
        i += 1
    output.write("  print('archivo a revisar?')\n")
    output.write("  archivo = input()\n")
    output.write("  prueba = open('../test/'+archivo)\n")
    output.write("  data = prueba.read()\n")
    output.write("  prueba.close()\n")
    
    output.write("  i = 0\n")
    output.write("  tokens = []\n")
    output.write("  last = 0\n")
    output.write("  while i < len(data):\n")
    output.write("      valid = word_break(data, automata0, i)\n")
    output.write("      if valid:\n")
    output.write("          if last != 0 and (i - last > 0):\n")
    output.write("              while last < i:\n")
    output.write("                  print(data[last], end='')\n")
    output.write("                  last += 1\n")
    output.write("              print(': False')\n")
    output.write("          last += len(valid)\n")
    output.write("          aut = 1\n")
    output.write("          new_token = Token('ANY', valid)\n")
    output.write("          while aut<len(automatas):\n")
    output.write("              if (is_in_language(automatas[aut], valid)):\n")
    output.write("                  new_token = Token(automatas[aut].id, valid)\n")
    output.write("                  break\n")
    output.write('              aut += 1\n')
    output.write("          tokens.append(new_token)\n")
    output.write("          i += len(valid)\n")
    output.write("      else:\n")
    output.write("          i+=1\n")
    output.write("  parser = Parser(tokens)\n")
    output.write("  parser.Expr()\n")
    output.write('if __name__ == "__main__":\n'+'   main()')

    output.close()

def write_automata(automata,i, file, name = "completo"):
    file.write("  automata"+str(i)+' = Automata("'+ name +'")\n')
    for node in automata.states:
        file.write("  temp_node= State("+ str(node.id2) + ")\n")
        if node.accept:
            file.write("  temp_node.accept = True\n")
        for transition in node.transitions:
            file.write("  temp_transition = Transition(" + repr(transition.transition)+", "+str(transition.end) +")\n")
            file.write("  temp_node.transitions.append(temp_transition)\n")
        file.write("  automata"+str(i)+".states.append(temp_node)\n")
    file.write("  automatas.append(automata"+str(i)+")\n")
    file.write("\n")
