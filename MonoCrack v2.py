#MonoCrack by Sam Medwell

import math
import random
import string
import CipherTools

def loadQuadgramData(path):
    try:
        with open(path, "r") as file:
            lines = file.readlines()

        lines = list(map(lambda x: x[:-1].split(" "), lines))

        quadgrams = {}
        total = 0
        for line in lines:
            quadgram = line[0]
            freq = int(line[1])
            total += freq
            quadgrams[quadgram] = freq

        for quadgram in quadgrams:
            quadgrams[quadgram] = math.log10(quadgrams[quadgram]/total)

        floor = math.log10(0.01/total)
        return quadgrams, floor
        
    except FileNotFoundError:
        print("Couldn't load training data")
        exit()      


def calculateFitness(text, trainingData, floor):
    text = ''.join([c for c in text if c.isalpha()])
    text = text.upper()
    fitness = 0
    for i in range(len(text)-3):
        quadgram = text[i:i+4]
        if quadgram in trainingData:
            fitness += trainingData[quadgram]
        else:
            fitness += floor

    return fitness


def generateKey():
    alphabet = list(string.ascii_uppercase)
    random.shuffle(alphabet)
    return alphabet


def mutateKey(key):

    offset = 1
        
    chromosome1=random.randint(0, 25-offset)
    key[chromosome1], key[chromosome1+offset] = key[chromosome1+offset], key[chromosome1]
    return key


def decryptText(text, key):
    lowerAlphabet = list(string.ascii_lowercase)
    upperAlphabet = list(string.ascii_uppercase)
    plaintext = ""
    for c in text:
        if c in lowerAlphabet:
            plaintext += lowerAlphabet[key.index(c.upper())]

        elif c in upperAlphabet:
            plaintext += upperAlphabet[key.index(c)]

        else:
            plaintext += c

    return plaintext
                                    

def calculateFreqKey(text):
    #perform frequency analysis on given text
    freqKey = [x[0] for x in CipherTools.freqAnalysis(text)]    
    return freqKey


#Convert a key that is in frequecny order into one that is in alphabetic order
def convertFreqKey(key):
    #Create a list of the normal alphabet
    Alphabet = list(string.ascii_uppercase)
    #Create a blank list of length 26
    freqKey = ["" for x in range(26)]
    #Iterate over english frequency order paired with chipher text frequency order
    for c in zip(CipherTools.englishFreq, key):
        freqKey[Alphabet.index(c[0])] = c[1]

    return freqKey

          
def crackMonoCipher(text, path, maxIter=1000, attempts=100, verbose=False):
    #Load traininhg data
    englishQuadgrams, floorValue = loadQuadgramData(path)
    topKey = []
    topFitness = -100000000000000000000
    topText = ""
    freqKey = calculateFreqKey(text)
    for i in range(attempts):      
        bestKey = list(freqKey)
        bestFitness = -1000000000000000
        bestText = ""
        iterations = 0
        while iterations < maxIter:
            potentialKey = mutateKey(bestKey)
            potentialText = decryptText(text, convertFreqKey(potentialKey))
            fitness = calculateFitness(potentialText, englishQuadgrams, floorValue)
            if fitness > bestFitness:
                bestFitness = fitness
                bestText = potentialText
                bestKey = potentialKey
                iterations = 0

            else:
                iterations += 1


        if bestFitness > topFitness:
            topKey, topFitness, topText = bestKey, bestFitness, bestText
        
            if verbose:
                print(topText)
                print(f"Fitness: {topFitness}")
                print(topKey)


    return topKey, topFitness, topText

    
    
with open("input.txt", "r") as file:
    text = file.read()


print(calculateFreqKey(text))
text, key, fitness = crackMonoCipher(text, "english_quadgrams.txt", maxIter=1000, attempts=10000000, verbose=True)




