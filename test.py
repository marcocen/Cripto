import sys
import os

def comer(f,n=1):
	for _ in range(n):
		f.readline()
 
def leer_valor(f,n=1):
	m=''
	for _ in range(n):
		m=m+f.readline().rstrip(os.linesep)
	f.readline()
	f.readline()
	return ''.join(m.splitlines())
f=open("oaep-int.txt")
valores=dict()
comer(f,37)

# Los valores del RSA
valores["n"]=leer_valor(f,8)
valores['e']=leer_valor(f)
valores['p']=leer_valor(f,4)
valores['q']=leer_valor(f,4)
valores['dp']=leer_valor(f,4)
valores['dq']=leer_valor(f,4)
valores['qinv']=leer_valor(f,4)

# Encriptacion
comer(f,4)
valores['mensaje']=leer_valor(f)
valores['L']=''
comer(f,12)
valores['lHash']=leer_valor(f,2)
valores['DB']=leer_valor(f,7)
valores['seed']=leer_valor(f,2)
valores['dbMask']=leer_valor(f,7)
valores['maskedDB']=leer_valor(f,7)
valores['seedMask']=leer_valor(f,2)
valores['maskedSeed']=leer_valor(f,2)
valores['maskedSeedmaskedDB']=leer_valor(f,8)
valores['cipherText']=leer_valor(f,8)

# Desencriptacion
comer(f,10)
valores['cModP']=leer_valor(f,4)
valores['cModQ']=leer_valor(f,4)
valores['m1']=leer_valor(f,4)
valores['m2']=leer_valor(f,4)
valores['h']=leer_valor(f,4)
valores['m']=leer_valor(f,8)


print valores['m']



f.close()
