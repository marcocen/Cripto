import random
import math
import hashlib
default_pseudo_random=random.Random()
default_crypto_random=random.SystemRandom()

DEFAULT_ITERATION=20

def exp_rapida(n,e,m):
	print n
	print e
	print '-'
	if e==0:
		return 1
	if e==1:
		return n
	if e%2==0:
		return exp_rapida(n**2%m,e/2,m)
	else:
		return n*exp_rapida(n**2%m,(e-1)/2,m)%m
		


def sacar_los_2(n):
	k=0
	while (n%2==0):
		n=n/2
		k+=1
	return (n,k)
    
#Miller Rabin
#Devuelve True si un numero es compuesto
def miller_rabin(n,a):
	(q,k)=sacar_los_2(n-1)
	a1=exp_rapida(a,q,n)
	if a1 == 1:
		return False
	for i in range(k):
		if a1== n-1:
			return False
		a1=a1**2%n # Hacer exp_rapida aca solo me meteria en una recursion innecesaria
	return True


#Devuelve True si es primo
def es_primo(n, rnd=default_pseudo_random, k=DEFAULT_ITERATION):
	primos_chicos=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
    #Optimizacion, chequeo contra varios primos chicos
	for prim in primos_chicos:
		if n==prim:
			return True
		if n%prim==0:
			return False
	for i in range(k):
		a=rnd.randint(2,n-1)
		if miller_rabin(n,a):
		#Si Miller Rabin devuelve True, entonces el numero es compuesto
			return False 
	#Si llegue hasta aca es que no encontre ningun testigo de compositeness
	#probablemente sea primo	
	return True 
    
    
def hallar_primo(size=128, rnd=default_crypto_random, k=DEFAULT_ITERATION):
	for i in range(20000):
		n=default_crypto_random.getrandbits(8*size)
		#Me aseguro que no sea multiplo de 2
		if (n%2==0):
			n+=1
		if es_primo(n,default_pseudo_random,100):
			return n
	return -1
    
def os2ip(x):
	return int(x.replace(' ',''),16)
    
def i2osp(x, x_len):
	y=(hex(x)[2:])[::-1]
	# Tomo la representacion hexa, le quito el '0x' y la invierto
	y=('{:0<'+str(2*x_len)+'}').format(y)
	# Padeo con ceros
	y=(' '.join(y[i:i+2] for i in xrange(0,len(y),2)))[::-1]
	# Separo en pares e invierto de nuevo
	
	return y
	
def rsaep(m, n):
	#m es la clave y n el mensaje
	# modulo    = m[0]
	# exponente = m[1]
	return 0
	
def mgf1(mgf_seed, mask_len, hash_class=hashlib.sha1):
	T=''
	h=hash_class()
	h_len=h.digest_size
	tope=4294967296*h_len
	if mask_len<=tope:
		for i in range(int(math.ceil(mask_len/h_len))):
			h.update(mgf_seed+i2osp(i,4))
			T=T+h.hexdigest()
		return T
	
	
print mgf1('asfqewwww',2**6)
	

	
	
	
	
	
	
	
	
	
