import random
import math
import hashlib
import sys

# Constantes
default_pseudo_random=random.Random()
default_crypto_random=random.SystemRandom()
DEFAULT_ITERATION=20

#MCD
def mcd(a,b):
    r=1
    while r>0:
        r=a%b
        (a,b)=(b,r)
    return a        


#XMCD
def xmcd(a,b):
    # Seteo los valores iniciales para
    # el algoritmo
    (ui,uj,vi,vj)=(1,0,0,1)
    r=1
    while(r>0):
        # asigno los valores a las variables
        (q,r)=(a//b,a%b)
        (u,v)=(ui-uj*q,vi-vj*q)
        # Preparo la siguiente iteracion
        (a,b,ui,uj,vi,vj)=(b,r,uj,u,vj,v)
    # Devuelvo los valores de la iteracion previa
    return (a, ui, vi)


# Exponenciacion rapida con modulo
def exp_rapida(n,e,m):
	resultado=1
	while e!=0:
		if e%2!=0:
			resultado=resultado*n%m
			e-=1
		n=n**2%m
		e=e/2
	return resultado
			
		

# Funcion auxiliar para Miller-Rabin, saca los factores de 2 y devuelve la 
# cantidad k de factores de 2 que tiene n y n/2^k
def sacar_los_2(n):
	k=0
	while (n%2==0):
		n=n/2
		k+=1
	return (n,k)
    
# Miller Rabin
# Devuelve True si un numero es compuesto
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


# Devuelve True si es primo
def es_primo(n, rnd=default_pseudo_random, k=DEFAULT_ITERATION):
	primos_chicos=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
    # Optimizacion, chequeo contra varios primos chicos
	for prim in primos_chicos:
		if n==prim:
			return True
		if n%prim==0:
			return False
	for i in range(k):
		a=rnd.randint(2,n-1)
		if miller_rabin(n,a):
		# Si Miller Rabin devuelve True, entonces el numero es compuesto
			return False 
	# Si llegue hasta aca es que no encontre ningun testigo de compositeness
	# probablemente sea primo	
	return True 
    
# Devuelve un primo de 128*8 bits    
def hallar_primo(size=128, rnd=default_crypto_random, k=DEFAULT_ITERATION):
	for i in range(20000):
		n=default_crypto_random.getrandbits(8*size)
		# Me aseguro que no sea multiplo de 2
		if (n%2==0):
			n+=1
		if es_primo(n,default_pseudo_random,100):
			return n
	return -1
    
# Toma un string de octetos y devuelve el entero que este represena en base 16
def os2ip(x):
	return int(x.replace(' ',''),16)

# Toma un entero y devuelve un string de octetos, en big endian, padeado con
# ceros hasta x_len
def i2osp(x, x_len):
	y=(hex(x)[2:])[::-1]
	# Tomo la representacion hexa, le quito el '0x' y la invierto
	y=('{:0<'+str(2*x_len)+'}').format(y)
	# Padeo con ceros
	y=(' '.join(y[i:i+2] for i in xrange(0,len(y),2)))[::-1]
	# Separo en pares e invierto de nuevo
	
	return y
	
	
# Primitiva de encriptacion de RSA	
def rsaep(m, n):
	# m es la clave y n el mensaje
	#  modulo    = m[0]
	#  exponente = m[1]
	if (n<0) or (n>m[0]-1):
		sys.exit('message representative out of range')
	return exp_rapida(n,m[1],m[0])
	
# Primitiva de desencriptacion de RSA
def rsadp(c,m):
	# c es la clave de la especificacion, hay dos casos
	# 	1) c=(n,d), donde n es el modulo y d el exponente
	#	2) c=((p,q,dP,dQ,qInv),[(ri,di,ti)])
	#
	#
	
	if isinstance(c[1],list):
		p,q,dp,dq,qinv=c[0]
		tuplas=c[1]
		m1=exp_rapida(m,dp,p)
		m2=exp_rapida(m,dq,q)
		emes=list()
		for i in range(len(tuplas)):
			emes.append(exp_rapida(m,tuplas[i][1],tuplas[i][0]))
		h=(m1-m2)*qinv%p
		m=m2+q*h
		
		print len(tuplas)
		if len(tuplas)>0:
			erres=[p,q]
			des=[dp,dq]
			tes=[0,qinv]
			for i in range(len(tuplas)):
				erres.append(tuplas[i][0])
				des.append(tuplas[i][1])
				tes.append(tuplas[i][2])	
			R=erres[0]
			print len(erres)
			print len(des)
			print len(tes)
			for i in range(2,len(erres)):
				print 'iteracion '
				print i-2
				R=R*erres[i-1]
				mi=exp_rapida(m,des[i],erres[i])
				h=(mi-m)*tes[i]%erres[i]
				m=m+R*h
		return m			
	m=exp_rapida(m,c[1],c[0])
	return m


# Devuelve una mascara como especificado en el documento
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
	
e=2**16-1
p=1299743
q=1299827

d=xmcd(e,(p-1)*(q-1))[1]

mm = (p-1)*(q-1)

r1,r2,r3,r4=(1299743, 1299827, 1299833, 1299887)
t3, t4 = 392357,538006 
d3, d4 = 67575,878571 
dP, dQ = 848189,303739 
qInv = 355905 
n = r1*r2*r3*r4
 
 
print rsadp(((r1,r2,dP,dQ,qInv), [(r3,d3,t3),(r4,d4,t4)]),e) 
print  rsaep((n,e),1008117944153308176100846) 




