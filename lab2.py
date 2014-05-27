import random
default_pseudo_random=random.Random()
default_crypto_random=random.SystemRandom()

DEFAULT_ITERATION=20

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
	a1=pow(a,q,n)
	if a1 == 1:
		return False
	for i in range(k):
		if a1== n-1:
			return False
		a1=pow(a1, 2,n)
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
    
print hallar_primo()
