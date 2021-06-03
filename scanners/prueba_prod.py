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
	if self.expect('number'): 
		self.read('number')
		result = self.Number(result)
	if self.expect('decnumber'): 
		self.read('decnumber')
		result = self.expression(result)
		
	if self.expect('('): 
		self.read('(')
		result = self.expression(result)
		
	result*=signo
	return result

def Number(self,result):
	if self.expect('number'): 
		self.read('number')
	if self.expect('decnumber'): 
		self.read('decnumber')
		
	result = float(self.last_token.value)
	return result

