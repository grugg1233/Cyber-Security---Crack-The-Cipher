import numpy as np
from operator import itemgetter

# global from : https://mathcenter.oxford.emory.edu/site/math125/englishLetterFreqs/
commonFreq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
lcf = [c for c in commonFreq]
commonVals = [
    0.12702,
    0.09056,
    0.08167,
    0.07507,
    0.06966,
    0.06749,
    0.06327,
    0.06094,
    0.05987,
    0.04253,
    0.04025,
    0.02782,
    0.02758,
    0.02406,
    0.02360,
    0.02228,
    0.02015,
    0.01974,
    0.01929,
    0.01492,
    0.00978,
    0.00772,
    0.00153,
    0.00150,
    0.00095,
    0.00074,
]


def freq(cipher: str) -> dict:
    d = {}
    ignore = {}
    for ch in cipher:
        if ch.isalpha():
            if ch in d:
                d[ch] += 1
            else:
                d[ch] = 1
        else:
            if ch in ignore:
                ignore[ch] += 1
            else:
                ignore[ch] = 1
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in d:
            d[c] = 0

    for x in d:
        d[x] /= len(cipher) - sum(list(ignore.values()))
    return d


def crack(cipher: str) -> str:
    mapOfFreq = freq(cipher)

    letterKeys = list(mapOfFreq.keys())
    lettervals = list(mapOfFreq.values())
    print(f"Sum of values : {sum(lettervals)}")

    sortedMap = sorted(zip(letterKeys, lettervals), key=itemgetter(1), reverse=True)

    print("\n", sortedMap)

    cipher_to_common = {}
    usedL = set()
    i = 0
    j = 0

    while i < len(sortedMap) and j < len(commonFreq):

        cipher_letter = sortedMap[i][0]
        common_letter = commonFreq[j]

        if cipher_letter in usedL:
            i += 1
            continue

        if common_letter in usedL:
            j += 1
            continue

        cipher_to_common[cipher_letter] = common_letter
        cipher_to_common[common_letter] = cipher_letter

        usedL.add(cipher_letter)
        usedL.add(common_letter)

        i += 1
        j += 1

    print("\n", cipher_to_common)

    char_list = []

    global history

    history = cipher_to_common

    for c in cipher:
        if not c.isalpha():
            char_list.append(c)
        else:
            char_list.append(cipher_to_common[c])
    decrypt = "".join(char_list)
    return decrypt


def manualSwap(change):
    global history

    a = change[0]
    b = change[1]

    a_partner = history[a]
    b_partner = history[b]

    history[a_partner] = b
    history[b_partner] = a

    history[a] = b_partner
    history[b] = a_partner


def main():
    ct = input("Enter the Cipher Text: ")
    decrypt = crack(ct.upper())
    print("\n", decrypt)

    global history

    while True:
        ans = input("\nDo you want to change any swap that was made? ")
        if ans == "No":
            break
        else:
            change = input("\nWhat do you want to change? (eg: YH) : ")
            change = change.upper()

            if len(change) != 2:
                print("Incorrect input")
                continue

            if not change[0].isalpha() or not change[1].isalpha():
                print("Only alphabets pls")
                continue

            manualSwap(change=change)

            char_list = []

            for c in ct:
                if not c.isalpha():
                    char_list.append(c)
                else:
                    char_list.append(history[c])

            decrypt = "".join(char_list)

            print("\n", decrypt)


if __name__ == "__main__":
    main()
