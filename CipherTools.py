#CipherTools by Sam Medwell
import string

englishFreq = ["E", "T", "A", "O", "I", "N", "S", "R", "H", "L", "D", "C", "U", "M", "F", "G", "P", "W", "Y", "B", "V", "K", "J", "X", "Z", "Q"]

def returnAlphabet():
    alphabet = {}
    for c in string.ascii_uppercase:
        alphabet[c] = 0
    return alphabet


def freqAnalysis(text):
    countAlphabet = returnAlphabet()
    percentageAlphabet = returnAlphabet()
    total = 0
    for c in text:
        c = c.upper()
        if c in countAlphabet:
            countAlphabet[c] += 1
            total += 1

    for c in countAlphabet.keys():
        percentage = round((countAlphabet[c]/total)*100, 2)
        percentageAlphabet[c] = percentage

    percentageAlphabet = sorted(percentageAlphabet.items(), key=lambda x: x[1], reverse=True)
    
    return percentageAlphabet



