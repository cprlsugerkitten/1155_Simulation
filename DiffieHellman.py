import time
import random

def smallestPrimRoot(primeNum):
    o = 1
    r = 2
    while r < primeNum:
        k = pow(r, o, primeNum)
        while (k > 1):
            o = o + 1
            k = (k * r) % primeNum
        if o == (primeNum - 1):
            return r
        o = 1
        r = r + 1      

def attack(exchangedNum, g, p):
    for x in range(1,p):
        if((g**x)%p == exchangedNum):
            return x
    return -1

def findKey(x,y,g,p):
    return (g**(x*y)) % p

        
if __name__ == "__main__":

    #Public Values
    p = 65539 # must be prime!
    g = smallestPrimRoot(p) # finds smallest primitive root of p

    #Private Values
    x = random.randint(1,p-1) # randomly generates private values
    y = random.randint(1,p-1) # randomly generates private values

    #calculate exchanged values
    K1 = (g**x)%p
    K2 = (g**y)%p


    start_time = time.time()
    
    discoveredX = attack(K1,g,p)
    foundX_time = time.time()

    discoveredY = attack(K2,g,p)
    foundY_time = time.time()

    # secretKey = findKey(discoveredX,discoveredY,g,p)
    # foundKey_time = time.time()

    print("x = " + str(discoveredX) + " was found in " + str(foundX_time-start_time) + " seconds!")
    print("y = " + str(discoveredY) + " was found in " + str(foundY_time-foundX_time) + " seconds!")
    # print("Secret Key = " + str(secretKey) + ", found in " + str(foundKey_time-foundY_time) + " seconds!")
    




