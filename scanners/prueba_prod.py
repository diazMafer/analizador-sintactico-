
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
	def Expr(self):

		while self.actual_token.type == 'number' or self.actual_token.type == 'decnumber' or self.actual_token.value == '-' or self.actual_token.value == '(':
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
		while self.actual_token.value == "+"or self.actual_token.value == "-":
			if self.actual_token.value == '+': 
				self.read('+')
				result2 = self.Term(result2)
				result1+=result2
			if self.actual_token.value == '-': 
				self.read('-')
				result2 = self.Term(result2)
				result1-=result2
				
		return result1

	def Term(self,result):
		result1, result2 =  0,0
		result1 = self.Factor(result1)
		while self.actual_token.value == "*"or self.actual_token.value == "/":
			if self.actual_token.value == '*': 
				self.read('*')
				result2 = self.Factor(result2)
				result1*=result2
			if self.actual_token.value == '/': 
				self.read('/')
				result2 = self.Factor(result2)
				result1/=result2
				
		result=result1
		return result

	def Factor(self,result):
		signo=1
		if self.actual_token.value == '-': 
			self.read('-')
			signo = -1
		if self.actual_token.type == 'number': 
			self.read('number', True)
			result = self.Number(result)
		if self.actual_token.type == 'decnumber': 
			self.read('decnumber', True)
			result = self.Number(result)
		if self.actual_token.value == '(': 
			self.read('(')
			result = self.expression(result)
			self.read(')')
		result*=signo
		return result

	def Number(self,result):
		if self.actual_token.type == 'number': 
			self.read('number',True)
		if self.actual_token.type == 'decnumber': 
			self.read('decnumber', True)
			
		result = float(self.last_token.value)
		return result

