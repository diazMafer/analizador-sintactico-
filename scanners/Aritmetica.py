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

    def expect(self, item, arg = False):
        og = self.id_token
        possible = False
        try:
            ans = self.read(item, arg)
            if type(ans) == bool:
                possible = ans
            else:
                possible = True
        except:
            possible = False
        self.id_token = og
        self.actual_token = self.tokens[self.id_token]
        self.last_token = self.tokens[self.id_token - 1]
        return possible

    def read(self, item, type = False):
        if type:
            if self.actual_token.type == item:
                self.advance()
                return True
            else:
                return False
        else:
            if self.actual_token.value == item:
                self.advance()
                return True
            else:
                return False

    def Expr(self):
        while self.expect('number', True) or self.expect('decnumber', True) or self.expect('-') or self.expect('('):
            print("solo entro una vez :)")
            self.Stat()
            self.read(";")
        self.read(".")

    def Stat(self):
        value = 0
        value = self.expression(value)
        print(value)

    def expression(self,result1):
        result1, result2 = 0, 0
        result1 = self.Term(result1)
        while self.expect("+") or self.expect("-") :
            if self.expect('+'): 
                self.read('+')
                result2 = self.Term(result2)
                result1+=result2
            elif self.expect('-'): 
                self.read('-')
                result2 = self.Term(result2)
                result1-=result2
            else:
                print("error")
            
        return result1

    def Term(self,result):
        result1, result2 =  0,0
        result1 = self.Factor(result1)
        while self.expect("*") or self.expect("/") :
            if self.expect('*'): 
                self.read('*')
                result2 = self.Factor(result2)
                result1*=result2
            if self.expect('/'): 
                self.read('/')
                result2 = self.Factor(result2)
                result1/=result2
            else:
                print("hola")
            
        result=result1
        return result

    def Factor(self,result):
        signo=1
        if self.expect('-'): 
            self.read('-')
            signo = -1
        elif self.expect('number', True): 
            result = self.Number(result)
        elif self.expect('decnumber', True):
            result = self.Number(result)
        elif self.expect('('): 
            self.read('(')
            result = self.expression(result)
            self.read(')')
        else:
            print("chay by")
        
        result*=signo
        return result

    def Number(self,result):
        if self.expect('number', True):
            self.read('number', True)
        elif self.expect('decnumber', True):
            self.read('decnumber', True)
        else:
            print("error")
        result = float(self.last_token.value)
        return result


import collections
EPSILON = 'ε'
class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

class Automata:
     def __init__(self, exp):
        self.id = exp 
        self.states = []

class State: 
   def __init__(self,num):
     self.id = num
     self.transitions = []
     self.accept = False 

class Transition: 
  def __init__(self,sym,to):
        self.symbol = sym
        self.to = to

def is_in_language(automata, expresion):
  if expresion == ' ' or expresion == '':
      expresion = EPSILON
  actual = [0]
  actual = cerradura(automata, actual)
  i = 0
  while True:
      temp = []
      for num in actual:
          for transition in automata.states[num].transitions:
              if transition.symbol == expresion[i] and transition.to not in temp:
                  temp.append(transition.to)
      i += 1
      temp = cerradura(automata, temp)
      if not temp and expresion == EPSILON:
          break
      actual = temp.copy()
      if i > len(expresion)-1:
          break
  for id in actual:
      if automata.states[id].accept:
          return True
  return False

def cerradura(automata, actual):
  for num in actual:
      for transition in automata.states[num].transitions:
          if transition.symbol == EPSILON and transition.to not in actual:
              actual.append(transition.to)
  return actual

def read_word(file, actual):
  temp_word = ''
  while actual < len(file):
      if(file[actual] == ' ' or file[actual] == '\n') and (len(temp_word)>0):
          break
      elif file[actual] == ' ' or file[actual] == '\n':
          actual += 1
      else:
          temp_word += file[actual]
          actual += 1
  return temp_word, actual

def word_break(file, automata0, actual = 0):
  temp = ''
  validos = []
  while actual < len(file):
      temp += file[actual]
      if is_in_language(automata0, temp):
          validos.append(temp)
      elif len(temp) == 1  and is_in_language(automata0, str(ord(temp))):
          validos.append(temp)
      actual += 1
  if validos:
      return max(validos, key = len)
  return False
def main():
  automatas = []
  automata0 = Automata("completo")
  temp_node= State(0)
  temp_transition = Transition('w', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('d', 2)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('0', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 3)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(1)
  temp_transition = Transition('h', 4)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(2)
  temp_transition = Transition('o', 5)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(3)
  temp_node.accept = True
  temp_transition = Transition('0', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('.', 6)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(4)
  temp_transition = Transition('i', 7)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(5)
  temp_node.accept = True
  automata0.states.append(temp_node)
  temp_node= State(6)
  temp_transition = Transition('0', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 8)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(7)
  temp_transition = Transition('l', 9)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(8)
  temp_node.accept = True
  temp_transition = Transition('0', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 8)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 8)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  temp_node= State(9)
  temp_transition = Transition('e', 5)
  temp_node.transitions.append(temp_transition)
  automata0.states.append(temp_node)
  automatas.append(automata0)

  automata1 = Automata("while")
  temp_node= State(0)
  temp_transition = Transition('w', 1)
  temp_node.transitions.append(temp_transition)
  automata1.states.append(temp_node)
  temp_node= State(1)
  temp_transition = Transition('h', 2)
  temp_node.transitions.append(temp_transition)
  automata1.states.append(temp_node)
  temp_node= State(2)
  temp_transition = Transition('i', 3)
  temp_node.transitions.append(temp_transition)
  automata1.states.append(temp_node)
  temp_node= State(3)
  temp_transition = Transition('l', 4)
  temp_node.transitions.append(temp_transition)
  automata1.states.append(temp_node)
  temp_node= State(4)
  temp_transition = Transition('e', 5)
  temp_node.transitions.append(temp_transition)
  automata1.states.append(temp_node)
  temp_node= State(5)
  temp_node.accept = True
  automata1.states.append(temp_node)
  automatas.append(automata1)

  automata2 = Automata("do")
  temp_node= State(0)
  temp_transition = Transition('d', 1)
  temp_node.transitions.append(temp_transition)
  automata2.states.append(temp_node)
  temp_node= State(1)
  temp_transition = Transition('o', 2)
  temp_node.transitions.append(temp_transition)
  automata2.states.append(temp_node)
  temp_node= State(2)
  temp_node.accept = True
  automata2.states.append(temp_node)
  automatas.append(automata2)

  automata3 = Automata("number")
  temp_node= State(0)
  temp_transition = Transition('0', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 1)
  temp_node.transitions.append(temp_transition)
  automata3.states.append(temp_node)
  temp_node= State(1)
  temp_node.accept = True
  temp_transition = Transition('0', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 1)
  temp_node.transitions.append(temp_transition)
  automata3.states.append(temp_node)
  automatas.append(automata3)

  automata4 = Automata("decnumber")
  temp_node= State(0)
  temp_transition = Transition('0', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 1)
  temp_node.transitions.append(temp_transition)
  automata4.states.append(temp_node)
  temp_node= State(1)
  temp_transition = Transition('0', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 1)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('.', 2)
  temp_node.transitions.append(temp_transition)
  automata4.states.append(temp_node)
  temp_node= State(2)
  temp_transition = Transition('0', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 3)
  temp_node.transitions.append(temp_transition)
  automata4.states.append(temp_node)
  temp_node= State(3)
  temp_node.accept = True
  temp_transition = Transition('0', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('1', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('2', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('3', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('4', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('5', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('6', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('7', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('8', 3)
  temp_node.transitions.append(temp_transition)
  temp_transition = Transition('9', 3)
  temp_node.transitions.append(temp_transition)
  automata4.states.append(temp_node)
  automatas.append(automata4)

  print('archivo a revisar?')
  archivo = input()
  prueba = open('../test/'+archivo)
  data = prueba.read()
  prueba.close()
  i = 0
  tokens = []
  last = 0
  while i < len(data):
      valid = word_break(data, automata0, i)
      if valid:
          if last != 0 and (i - last > 0):
              while last < i:
                  print(data[last], end='')
                  last += 1
              print(': False')
          last += len(valid)
          aut = 1
          new_token = Token("ANY", valid)
          while aut<len(automatas):
              if (is_in_language(automatas[aut], valid)):
                  new_token = Token(automatas[aut].id, valid)
                  break
              aut += 1
          print(new_token.value, ': ', new_token.type)
          tokens.append(new_token)
          i += len(valid)
      else:
          i+=1
  parser = Parser(tokens)
  parser.Expr()
if __name__ == "__main__":
   main()