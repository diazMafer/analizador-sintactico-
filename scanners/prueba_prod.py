
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
				#print('expected ', item, ' got ', self.actual_token.type)
		else:
			if self.actual_token.value == item:
				self.advance()
				return True
			else:
				return False
	def Expr(self):

		while self.expect('number', True) or self.expect('decnumber', True) or self.expect('-') or self.expect('('):
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
			if self.expect('-'): 
				self.read('-')
				result2 = self.Term(result2)
				result1-=result2
				
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
				
		result=result1
		return result

	def Factor(self,result):
		signo=1
		if self.expect('-'): 
			self.read('-')
			signo = -1
		if self.expect('number', True): 
			self.read('number', True)
			result = self.Number(result)
		if self.expect('decnumber', True): 
			self.read('decnumber', True)
			result = self.Number(result)
		if self.expect('('): 
			self.read('(')
			result = self.expression(result)
			self.read(')')
		result*=signo
		return result

	def Number(self,result):
		if self.expect('number',True): 
			self.read('number',True)
		if self.expect('decnumber', True): 
			self.read('decnumber', True)
			
		result = float(self.last_token.value)
		return result

