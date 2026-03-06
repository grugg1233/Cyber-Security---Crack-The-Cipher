"""
George Attallah , Rishik Yesgari , Andrew Beshay
Homework 3 CS351

"""

import sys
from collections import Counter
from operator import itemgetter
import matplotlib.pyplot as plt

"""

Explanation of the code and Assumptions made 

The program is interactive such that it is a recurring loop (until the user enters exit) that is command based. User will interact in the terminal . 

The logic and assumptions is as follows: 
    1) we initialize a global common frequencies pairing sorted in desc. order of letters in english to their frequencies from oxford emory

    2) we then take the cipher text (with provided assumptions in mind) and clean it just in case (to upper) 

    3) we compute the frequencies of alphabetic characters for the cipher text (ignoring special chars like punctuation) 

    4) we sort the frequencies in desc. order using pythons built in sorted( ) funciton with reverse flag

    5) we map cipher frequencies to common frequencies and provide the user the option to graph this relationship 

    6) the user can make an initial mapping that will do pairwise frequency substitution based soley on frequency alignment 
        i.e. most frequent cipher char maps to (->) e the most frequent common character according to our source 
    
    7) users are then given the option to manually interact with cipher via the : command which is used to swap characters in the cipher text and = to assign a character to 
    another in the character map.  

    8) the user will continue to manually associate characters using the map and commmon trigrams - computed using the built in Counter and most_common functions 
    as well as their current status of decryption using the show command 

    9) user can quit the program with quit or exit when done 

    9a) user can reset to origianl mapping with reset 
    9b) user can check that the mapping is monoalphabetic using check comand 
    
"""


# global from : https://mathcenter.oxford.emory.edu/site/math125/englishLetterFreqs/
COMMON_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
COMMON_VALS = [
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
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter_freq(text: str) -> dict:
    """
    input: Text of type string
    return:
        Frequencies of all alphabets in the input text.

    Calculates how many times (frequency) each letter appears in the text
    """

    # get a list of all the letters in the cipher text
    letters = [ch for ch in text.upper() if ch.isalpha()]
    total = len(letters)
    # initialize to 0 for all characters
    freqs = {c: 0.0 for c in ALPHABET}
    if total == 0:
        return freqs
    # Counter is an object that returns counts of iterable objects in this case the list of letters
    counts = Counter(letters)
    # compute the actual frequencies
    for c in ALPHABET:
        freqs[c] = counts.get(c, 0) / total
    return freqs


def make_identity_pairs() -> dict:
    """
    return:
        A dictionary with each letter mapped to itself

    Creates a mapping in a dictionary where every letter maps to itself
    """

    # map each character to itself initially
    return {c: c for c in ALPHABET}


def check_func(mapping: dict) -> bool:
    """
    input:
        mapping: dictionary representing cipher -> plaintext mapping

    return:
        True if mapping represents a valid monoalphabetic substitution
        False otherwise

    Checks that the mapping is valid by checking if every letter maps to a different letter
    """

    # must define mappings for all letters (or at least behave like it does)
    for a in ALPHABET:
        if a not in mapping:
            return False
        b = mapping[a]
        if b not in ALPHABET:
            return False

    # outputs must be unique (a permutation)
    images = [mapping[a] for a in ALPHABET]
    return len(set(images)) == 26


def set_pair(mapping: dict, a: str, b: str) -> None:
    """
    input:
        mapping: dictionary representing cipher -> plaintext mapping
        a: cipher letter
        b: plaintext letter

    return:
        None

    Sets the mapping so that a cipher letter maps to plaintext letter
    """

    a = a.upper()
    b = b.upper()

    if a not in ALPHABET or b not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    # association of 2 letters reciprocally
    mapping[a] = b


def initial_mapping_by_frequency(ct: str) -> dict:
    """
    input:
        ct: ciphertext string

    return:
        mapping dictionary where cipher letters are mapped to
        plaintext letters based on descending frequency alignment

    Creates an initial mapping by swapping the most frequency letter in ciphertext to the most frequent english letter
    """

    freqs = letter_freq(ct)
    # the original frequencies is indescending order so we sort this in reverse so they can be matched
    ranked = sorted(freqs, key=freqs.get, reverse=True)

    mapping = make_identity_pairs()

    # to avoid duplicate entries
    used_out = set()
    assigned = set()
    i = 0
    j = 0
    # map new pairs : most frequent in cipher to most frequent from common freq
    while i < len(ranked) and j < len(COMMON_FREQ):
        c = ranked[i]
        p = COMMON_FREQ[j]
        i += 1
        j += 1

        if c in assigned or p in used_out:
            continue

        set_pair(mapping, c, p)
        assigned.add(c)
        used_out.add(p)

    remaining_keys = [a for a in ALPHABET if a not in assigned]
    remaining_outs = [a for a in ALPHABET if a not in used_out]

    for k, v in zip(remaining_keys, remaining_outs):
        set_pair(mapping, k, v)

    return mapping


def decode(text: str, mapping: dict[str, str]) -> str:
    """
    input:
        text: ciphertext string
        mapping: dictionary of cipher -> plaintext mapping

    return:
        decoded plaintext string

    Uses the current mapping to convert the cipher text to decrypted text
    """

    out = []
    # making the substitutions in the actual cipher
    for ch in text:
        if ch.isalpha():
            up = ch.upper()
            out.append(mapping.get(up, up))
        else:
            out.append(ch)
    return "".join(out)


def associate(mapping: dict[str, str], a: str, b: str) -> None:
    """
    input:
        mapping: dictionary of cipher -> plaintext mapping
        a: plaintext letter
        b: plaintext letter

    Swaps two plaintext letters so their decoded mapping also switch places
    """

    # turning the text to uppercase
    p = a.upper()
    q = b.upper()

    if p not in ALPHABET or q not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    if p == q:
        return

    cp = next((k for k, v in mapping.items() if v == p), None)
    cq = next((k for k, v in mapping.items() if v == q), None)

    if cp is None or cq is None:
        print(
            f"Cannot swap '{p}' and '{q}' because one of them is not currently produced by the mapping."
        )
        return

    mapping[cp], mapping[cq] = q, p


def force_cipher_to_plain(mapping: dict[str, str], c: str, p: str) -> None:
    """
    input:
        mapping: dictionary representing cipher -> plaintext mapping
        c: cipher letter
        p: plaintext letter

    Forces the cipher letter to decode to a chosen plaintext
    """

    # turning the text to uppercase
    c = c.upper()
    p = p.upper()

    if c not in ALPHABET or p not in ALPHABET:
        raise ValueError("Letters must be A-Z.")

    old_p = mapping[c]  # what c used to decode to
    other = next((k for k, v in mapping.items() if v == p), None)

    mapping[c] = p  # set it

    if other is not None and other != c:  # fix collision
        mapping[other] = old_p


def top_trigrams(text: str, n: int = 10) -> list:
    """
    input:
        text: string of decoded text
        n: number of trigrams to return

    return:
        list of tuples containing the most common trigrams and their frequency counts

    Finds the most common three letter sequences
    """

    # get all the letters in the text
    letters = [ch for ch in text.upper() if ch.isalpha()]
    if len(letters) < 3:
        return []
    # compute the trigrams as the groupings of 3 letters from each initial position to the end of the text
    trigs = (
        letters[i] + letters[i + 1] + letters[i + 2] for i in range(len(letters) - 2)
    )
    # most commmon is a built in function that returns the n most common elements in descending order
    return Counter(trigs).most_common(n)


def show_graph(ct: str):
    """
    input:
        ct: ciphertext string

    Displays the graph of the letter frequencies of the ciphertext
    """

    if not ct.strip():
        print("Error: Load ciphertext first before graphing.")
        return

    ct_freq = letter_freq(ct.upper())
    # zip here is used to pair frequencies to the common letters pairwise,
    english_by_letter = {ch: val for ch, val in zip(COMMON_FREQ, COMMON_VALS)}
    # x-axis value
    letters = list(ALPHABET)
    # the two bars we want to evaluate are cipher text and common frequencies
    ct_vals = [ct_freq[c] for c in letters]
    en_vals = [english_by_letter[c] for c in letters]

    x = list(range(len(letters)))
    w = 0.42

    plt.figure(figsize=(10, 5), dpi=100)
    # plot the two next to eachother
    plt.bar([i - w / 2 for i in x], ct_vals, width=w, edgecolor="black", label="Cipher")
    plt.bar(
        [i + w / 2 for i in x], en_vals, width=w, edgecolor="black", label="English"
    )
    plt.xticks(x, letters)
    plt.title("Letter Frequencies: Ciphertext vs English")
    plt.xlabel("Letter")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

    print("Graph opened in a new window. Close the window to continue typing commands.")
    plt.show()


def print_help():
    print("\nAvailable Commands")
    print("  load            - Enter a new ciphertext")
    print("  mapbyfreq       - map automatically by letter frequencies")
    print("  : <AB>          - Swap plaintext letters in current decode (e.g., ': ET')")
    print("  = <AB>          - Force cipher->plain mapping (e.g., '= XE' means X->E)")
    print("  reset           - Reset the mapping to defaults")
    print("  graph           - Open the letter frequency bar chart")
    print("  check           - Check if the current mapped monoalphabetically")
    print("  help            - Show this menu")
    print("  quit / exit     - Exit the program")


def main():
    try:
        print("Random Cipher Cracker")
        print('Type "help" for a list of commands.')

        ct = ""
        # initialize mapping of all letters to self i.e. a->a b->b etc
        mapping = make_identity_pairs()

        print_help()
        # crack loop
        while True:

            user_input = input("\n> ").strip().split()

            if not user_input:
                continue

            cmd = user_input[0].lower()

            # Checking for different input scenarios
            if cmd in ["quit", "exit"]:
                print("Exiting...")
                break

            elif cmd == "help":
                print_help()

            elif cmd == "load":
                print("Enter your ciphertext (press Enter to finish):")
                ct = input(">> ").strip()
                print("Ciphertext loaded successfully.")

            elif cmd == "mapbyfreq":
                if not ct:
                    print("Error: You must load a ciphertext first.")
                else:
                    mapping = initial_mapping_by_frequency(ct.upper())
                    print("Mapping by frequency.")

            elif cmd == "reset":
                mapping = make_identity_pairs()
                print("Mapping reset to identity pairs.")

            elif cmd == "graph":
                show_graph(ct)

            elif cmd == "check":
                ok = check_func(mapping)
                print(f"Mapping OK? {ok}")
            elif cmd == ":":
                if len(user_input) != 2 or len(user_input[1]) != 2:
                    print("Usage Error: Please use format ': AB' (two letters)")
                    continue
                a, b = user_input[1][0], user_input[1][1]
                associate(mapping, a, b)
                print(f"Swapped plaintext '{a.upper()}' <-> '{b.upper()}'.")
            elif cmd == "=":
                if len(user_input) != 2 or len(user_input[1]) != 2:
                    print("Usage Error: Please use format '= AB' (two letters)")
                    continue
                c, p = user_input[1][0], user_input[1][1]
                force_cipher_to_plain(mapping, c, p)
                print(f"Forced cipher '{c.upper()}' -> plaintext '{p.upper()}'.")
            else:
                print("Unknown command. Type 'help' for options.")

            if not ct:
                print("No ciphertext loaded. Type 'load' first.")
                continue

            print("\n[Current Mapping]")
            # display mapping
            map_strs = [f"{c}->{mapping.get(c, c)}" for c in ALPHABET]
            for i in range(0, 26, 6):
                print("  " + "   ".join(map_strs[i : i + 6]))

            # display current decoding step
            plain = decode(ct, mapping)
            # display trigrams
            trigs = top_trigrams(plain, n=3)
            print("\n[Top Trigrams (Decrypted)]")
            if not trigs:
                print("  No trigrams found (need at least 3 letters).")
            else:
                for i, (tri, k) in enumerate(trigs, start=1):
                    print(f"  {i:2d}) {tri} -> {k}")

            print("\n[Decrypted Output]")
            print(plain)
    except KeyboardInterrupt:
        print("\ngoodbye!")


if __name__ == "__main__":
    main()
