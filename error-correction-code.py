import numpy as np
import itertools
import random

def getSyndrome(rCode):
    #Check t5t6t7
    s1 = rCode[0]^rCode[1]^rCode[2]^rCode[4]
    s2 = rCode[1]^rCode[2]^rCode[3]^rCode[5]
    s3 = rCode[0]^rCode[2]^rCode[3]^rCode[6]
    
    #Check t8t9t10t11
    s4 = rCode[0]^rCode[1]^rCode[7]
    s5 = rCode[1]^rCode[2]^rCode[8]
    s6 = rCode[2]^rCode[3]^rCode[9]
    s7 = rCode[3]^rCode[0]^rCode[10]

    #Construct synchrome
    syndrome = [s1,s2,s3,s4,s5,s6,s7]
    syndrome = map(str, syndrome)
    strSyn = "".join(syndrome)
    return strSyn

def buildSyndromes(rCode, syndromes, errorBits):
    strSyn = getSyndrome(rCode)
    # print strSyn
    flipBits = "".join(["t"+str(b) for b in errorBits])
    if strSyn in synBitMap:
        pass
        # print "Syndrome will be the same when errors occur in %s and %s"%(synBitMap[strSyn], flipBits)
    else:
        synBitMap[strSyn] = flipBits

    syndromes.add(strSyn)
    
    return syndromes

def encode(srcCode):
    G = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],
    [1,1,1,0],[0,1,1,1],[1,0,1,1],[1,1,0,0],
    [0,1,1,0],[0,0,1,1],[1,0,0,1]])

    s = np.matrix([[srcCode[0]],
    [srcCode[1]],
    [srcCode[2]],
    [srcCode[3]]])
    x = np.dot(G,s)
    x = x%2
    tCode = [x.item((i,0)) for i in range(0,11)]
    return tCode

def getSyn4BitsErr(errCount, BitErrors, syndromes, tCode):
    for errorBits in BitErrors:
        # print "Error bits are %s"%(",".join(["t"+str(b) for b in errorBits]))
        #Initialize synchrome
        syndrome = []
        for i in range(0, len(errorBits)):
            exec("error_%s = errorBits[%s]-1"%(i+1,i))

        rCode = tCode[:]
        for i in range(0, len(errorBits)):
            exec("rCode[error_%s] = rCode[error_%s]^1"%(i+1,i+1))

        #print rCode
        #Construct syndromes
        buildSyndromes(rCode, syndromes, errorBits)
    if len(BitErrors) == 0:
        buildSyndromes(rCode, syndromes, ())

def mapSynBit(syndromes, synBitMap):
    #Assume transmitted code is 10100101111
    tCode = [1,0,1,0,0,1,0,1,1,1,1]

    #Construct 0 bit error syndrome
    zeroBitErrors = list(itertools.combinations(range(1,12),0))
    #Construct combinations of 1 flipped bit position in all 11 bits
    oneBitErrors = list(itertools.combinations(range(1,12),1))
    #Construct combinations of 2 flipped bits positions in all 11 bits
    twoBitErrors = list(itertools.combinations(range(1,12),2))
    # twoErrorBitsList = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),
    #           (2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11),
    #           (3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),
    #           (4,5),(4,6),(4,7),(4,8),(4,9),(4,10),(4,11),
    #           (5,6),(5,7),(5,8),(5,9),(5,10),(5,11),
    #           (6,7),(6,8),(6,9),(6,10),(6,11),
    #           (7,8),(7,9),(7,10),(7,11),
    #           (8,9),(8,10),(8,11),
    #           (9,10),(9,11),
    #           (10,11)]

    thrBitErrors = list(itertools.combinations(range(1,12),3))
    forBitErrors = list(itertools.combinations(range(1,12),4))
    fivBitErrors = list(itertools.combinations(range(1,12),5))
    sixBitErrors = list(itertools.combinations(range(1,12),6))
    sevBitErrors = list(itertools.combinations(range(1,12),7))
    egtBitErrors = list(itertools.combinations(range(1,12),8))
    ninBitErrors = list(itertools.combinations(range(1,12),9))
    tenBitErrors = list(itertools.combinations(range(1,12),10))
    eleBitErrors = list(itertools.combinations(range(1,12),11))

    getSyn4BitsErr(0, zeroBitErrors, syndromes, tCode)
    getSyn4BitsErr(1, oneBitErrors, syndromes, tCode)
    getSyn4BitsErr(2, twoBitErrors, syndromes, tCode)
    getSyn4BitsErr(3, thrBitErrors, syndromes, tCode)
    getSyn4BitsErr(4, forBitErrors, syndromes, tCode)
    getSyn4BitsErr(5, fivBitErrors, syndromes, tCode)
    getSyn4BitsErr(6, sixBitErrors, syndromes, tCode)
    getSyn4BitsErr(7, sevBitErrors, syndromes, tCode)
    getSyn4BitsErr(8, egtBitErrors, syndromes, tCode)
    getSyn4BitsErr(9, ninBitErrors, syndromes, tCode)
    getSyn4BitsErr(10, tenBitErrors, syndromes, tCode)
    getSyn4BitsErr(11, eleBitErrors, syndromes, tCode)

    # print synBitMap


def decode(receivedCode, syndromes, synBitMap):
    syn = getSyndrome(receivedCode)
    # print syn
    flipBits = synBitMap[syn]
    # print flipBits
    flipBits = flipBits.split("t")[1:]
    flipBits = map(int, flipBits)

    for fb in flipBits:
        fbInd = fb-1
        receivedCode[fbInd] = receivedCode[fbInd] ^ 1

    # decode = "".join(map(str, receivedCode))
    
    decodeSrc = receivedCode[0:4]
    return decodeSrc

def flip(p):
    return random.random() < p

def bitErrProb(syndromes, p, testTimes, synBitMap):
    err1 = 0
    err2 = 0
    err3 = 0
    err4 = 0

    for i in range(testTimes):
        srcCode = []
        for j in range(0,4):
            j = random.randrange(2)
            srcCode.append(j)
        
        tCode = encode(srcCode)
        # print srcCode
        # print tCode
        rCode = []
        for t in tCode:
            if flip(p):
                r = t^1
            else:
                r = t
            rCode.append(r)
        # print rCode

        decodeSrc = decode(rCode, syndromes, synBitMap)
        # print decodeSrc

        for k in range(0, 4):
            if decodeSrc[k] != srcCode[k]:
                exec("err%s += 1" %(k+1))

    print err1, err2, err3, err4
    p1 = float(err1)/testTimes
    p2 = float(err2)/testTimes
    p3 = float(err3)/testTimes
    p4 = float(err4)/testTimes

    bitErrProb = (p1+p2+p3+p4)/4
    return bitErrProb


# encode()
source = list(set(itertools.combinations([0,1,0,1,0,1,0,1],4)))

for srcCode in source:
    #Get transmitted codes for 16 source codes
    tCodeStr = encode(srcCode)
    # print "Transmitted code for source code %s is: %s"%("".join(str(b) for b in srcCode), tCodeStr)

#Syndromes
syndromes = set()
synBitMap = {}

mapSynBit(syndromes, synBitMap)

#Transmit n times to get probability from frequency
testTimes = 5000000

prob_a = bitErrProb(syndromes, 0.4, testTimes, synBitMap)
print "Bit error probability under f=0.4, is %s"%prob_a
prob_b = bitErrProb(syndromes, 0.1, testTimes, synBitMap)
print "Bit error probability under f=0.1, is %s"%prob_b
prob_c = bitErrProb(syndromes, 0.01, testTimes, synBitMap)
print "Bit error probability under f=0.01, is %s"%prob_c