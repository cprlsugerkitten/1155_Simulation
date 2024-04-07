import time
import random
import matplotlib.pyplot as plt
import math

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

def isPrime(n):
    if n == 0 or n == 1 or n == 2: #2 doesn't have a primitive root so its set to not a prime
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
        
    return True


def averageAttackSpeed(numOfBits, trials):
    xTimes = []
    yTimes = []
    print("Starting " + str(trials) + " attacks on " + str(numOfBits) + " bit prime!")
    for i in range(trials):
        p = random.getrandbits(numOfBits) # randomly select p
        while not isPrime(p):
            p = random.getrandbits(numOfBits) # make sure p is prime
        g = smallestPrimRoot(p) # finds smallest primitive root of p
        x = random.randint(1,p-1) # randomly generates private values
        y = random.randint(1,p-1) # randomly generates private values
        K1 = (g**x)%p
        K2 = (g**y)%p

        start_time = time.time()

        discoveredX = attack(K1,g,p)
        foundX_time = time.time()

        discoveredY = attack(K2,g,p)
        foundY_time = time.time()

        xTimes.append(foundX_time-start_time)
        yTimes.append(foundY_time-foundX_time)
    
    avgX = sum(xTimes)/len(xTimes)
    avgY = sum(yTimes)/len(yTimes)

    print("In " + str(trials) + " trials, the average time to crack x was " + str(avgX) + " seconds!")
    print("In " + str(trials) + " trials, the average time to crack y was " + str(avgY) + " seconds!")
    print("\n")

    return avgX,avgY

    
def attackOnce(numOfBits):
    #Public Values
    p = random.getrandbits(numOfBits) # randomly select p
    while not isPrime(p):
        p = random.getrandbits(numOfBits) # make sure p is prime

    print("p = " + str(p))
    g = smallestPrimRoot(p) # finds smallest primitive root of p
    print("g = " + str(g))

    #Private Values
    x = random.randint(1,p-1) # randomly generates private values
    y = random.randint(1,p-1) # randomly generates private values

    #calculate exchanged values
    K1 = (g**x)%p
    K2 = (g**y)%p

    print("Starting Attack!")
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
    
def graph(numOfBits,trials,isSemiLogGraph):
    x =[]
    y = []
    for i in range(2,numOfBits):
        (avgX, avgY) = averageAttackSpeed(i,trials)
        x.append(i)
        if isSemiLogGraph:
            y.append(math.log10((avgX+avgY)/2))
        else:
            y.append((avgX+avgY)/2)

    plt.plot(x,y)
    plt.show()

        
if __name__ == "__main__":

    NUM_OF_BITS = 12 #num of bits that p is generated from

    #Attack DH with a random p, lowest primitive root g
    attackOnce(NUM_OF_BITS)

    #Attack DH with a random p, lowest primitive root g, for some amount
    #of trials, and returns the average time to crack private keys
    averageAttackSpeed(NUM_OF_BITS,20)

    #Attack DH with a random p, lowest primitive root g, for some amount
    #of trials, and returns the average time to crack private keys, and graphs on a logGraph
    graph(NUM_OF_BITS,20,True)

    




