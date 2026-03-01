import sys
from collections import Counter
from operator import itemgetter
import matplotlib.pyplot as plt
# global from : https://mathcenter.oxford.emory.edu/site/math125/englishLetterFreqs/
COMMON_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
COMMON_VALS = [
    0.12702, 0.09056, 0.08167, 0.07507, 0.06966, 0.06749, 0.06327, 0.06094, 0.05987,
    0.04253, 0.04025, 0.02782, 0.02758, 0.02406, 0.02360, 0.02228, 0.02015, 0.01974,
    0.01929, 0.01492, 0.00978, 0.00772, 0.00153, 0.00150, 0.00095, 0.00074
]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def letter_freq(text: str) -> dict:
    #get a list of all the letters in the cipher text
    letters = [ch for ch in text.upper() if ch.isalpha()]
    total = len(letters)
    #initialize to 0 for all characters 
    freqs = {c: 0.0 for c in ALPHABET}
    if total == 0:
        return freqs
    #Counter is an object that returns counts of iterable objects in this case the list of letters
    counts = Counter(letters)
    #compute the actual frequencies 
    for c in ALPHABET:
        freqs[c] = counts.get(c, 0) / total
    return freqs

def make_identity_pairs() -> dict:
    #map each character to itself initially 
    return {c: c for c in ALPHABET}

def is_reciprocal(mapping: dict) -> bool:
    #sanity check for reciprocity of mapping 
    for a in ALPHABET:
        #b is the pair of a 
        b = mapping.get(a, a)
        if b not in ALPHABET:
            return False
        # check that a is the pair of b
        if mapping.get(b, b) != a:
            return False
    return True

def set_pair(mapping: dict, a: str, b: str) -> None:

    a = a.upper()
    b = b.upper()
    
    if a not in ALPHABET or b not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    #association of 2 letters reciprocally 
    mapping[a] = b
    mapping[b] = a

def initial_reciprocal_mapping_by_frequency(ct: str) -> dict:
    freqs = letter_freq(ct)
    # the original frequencies is indescending order so we sort this in reverse so they can be matched
    ranked = sorted(freqs, key=freqs.get, reverse=True)

    mapping = make_identity_pairs()
    
    #to avoid duplicate entries
    used = set()

    i = 0
    j = 0
    #map new pairs : most frequent in cipher to most frequent from common freq
    while i < len(ranked) and j < len(COMMON_FREQ):
        c = ranked[i]
        p = COMMON_FREQ[j]
        i += 1
        j += 1

        if c in used or p in used:
            continue

        set_pair(mapping, c, p)
        used.add(c)
        used.add(p)

    return mapping

def decode(text: str, mapping: dict) -> str:
    out = []
    #making the substitutions in the actual cipher
    for ch in text:
        if ch.isalpha():
            up = ch.upper()
            out.append(mapping.get(up, up))
        else:
            out.append(ch)
    return "".join(out)

def associate(mapping: dict, a: str, b: str) -> None:
    #association in plce of swapping so any 2 letters a and b can be associated at runtime
    a = a.upper()
    b = b.upper()
    if a not in ALPHABET or b not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    if a == b:
        return

    old_a_partner = mapping.get(a, a)
    old_b_partner = mapping.get(b, b)


    set_pair(mapping, a, b)

    # remove the pairing of the old partners to the associated values
    orphans = {old_a_partner, old_b_partner} - {a, b}


    if len(orphans) == 2:
        o1, o2 = orphans
        set_pair(mapping, o1, o2)
    #if one of the letters was mapped to itself 
    elif len(orphans) == 1:

        o1 = orphans.pop()
        set_pair(mapping, o1, o1)

def top_trigrams(text: str, n: int = 10) -> list:
    #get all the letters in the text
    letters = [ch for ch in text.upper() if ch.isalpha()]
    if len(letters) < 3:
        return []
    #compute the trigrams as the groupings of 3 letters from each initial position to the end of the text 
    trigs = (letters[i] + letters[i + 1] + letters[i + 2] for i in range(len(letters) - 2))
    # most commmon is a built in function that returns the n most common elements in descending order
    return Counter(trigs).most_common(n)

def show_graph(ct: str):
    
    if not ct.strip():
        print("Error: Load ciphertext first before graphing.")
        return
    
    ct_freq = letter_freq(ct.upper())
    #zip here is used to pair frequencies to the common letters pairwise,
    english_by_letter = {ch: val for ch, val in zip(COMMON_FREQ, COMMON_VALS)}
    #x-axis value
    letters = list(ALPHABET)
    #the two bars we want to evaluate are cipher text and common frequencies
    ct_vals = [ct_freq[c] for c in letters]
    en_vals = [english_by_letter[c] for c in letters]

    x = list(range(len(letters)))
    w = 0.42

    plt.figure(figsize=(10, 5), dpi=100)
    #plot the two next to eachother 
    plt.bar([i - w/2 for i in x], ct_vals, width=w, edgecolor="black", label="Cipher")
    plt.bar([i + w/2 for i in x], en_vals, width=w, edgecolor="black", label="English")
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
    print("  assoc <L1> <L2> - Associate two letters (e.g., 'assoc A E')")
    print("  reset           - Reset the mapping to defaults")
    print("  show            - Display the current mapping, trigrams, and decrypted output")
    print("  graph           - Open the letter frequency bar chart")
    print("  check           - Check if the current mapping is perfectly reciprocal")
    print("  help            - Show this menu")
    print("  quit / exit     - Exit the program")

def main():
    print("Reciprocal Cipher Cracker")
    print('Type "help" for a list of commands.')
    
    ct = ""
    #initialize mapping of all letters to self i.e. a->a b->b etc
    mapping = make_identity_pairs()
    
    print_help()
    #crack loop 
    while True:
        
        user_input = input("\n> ").strip().split()
            
        if not user_input:
            continue
            
        cmd = user_input[0].lower()

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
                mapping = initial_reciprocal_mapping_by_frequency(ct.upper())
                print("Mapping by frequency.")
                
        elif cmd == "reset":
            mapping = make_identity_pairs()
            print("Mapping reset to identity pairs.")
            
        elif cmd in ["assoc", "a"]:
            if len(user_input) != 3:
                print("Usage Error: Please use format 'assoc A B'")
                continue

            associate(mapping, user_input[1], user_input[2])
            print(f"Associated '{user_input[1].upper()}' with '{user_input[2].upper()}'.")

                
        elif cmd == "show":
            if not ct:
                print("No ciphertext loaded. Type 'load' first.")
                continue
            

            print("\n[Current Mapping]")
            #display mapping 
            map_strs = [f"{c}->{mapping.get(c, c)}" for c in ALPHABET]
            for i in range(0, 26, 6):
                print("  " + "   ".join(map_strs[i:i+6]))

            #display current decoding step
            plain = decode(ct, mapping)
            #display trigrams
            trigs = top_trigrams(plain, n=10)
            print("\n[Top Trigrams (Decrypted)]")
            if not trigs:
                print("  No trigrams found (need at least 3 letters).")
            else:
                for i, (tri, k) in enumerate(trigs, start=1):
                    print(f"  {i:2d}) {tri} -> {k}")
                    

            print("\n[Decrypted Output]")
            print(plain)

            
        elif cmd == "graph":
            show_graph(ct)
            
        elif cmd == "check":
            ok = is_reciprocal(mapping)
            print(f"Reciprocal Mapping OK? {ok}")
            
        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()