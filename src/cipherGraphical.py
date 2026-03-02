import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
from operator import itemgetter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def check_func(mapping: dict) -> bool:
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

    a = a.upper()
    b = b.upper()

    if a not in ALPHABET or b not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    #association of 2 letters reciprocally
    mapping[a] = b


def initial_mapping_by_frequency(ct: str) -> dict:
    freqs = letter_freq(ct)
    # the original frequencies is indescending order so we sort this in reverse so they can be matched
    ranked = sorted(freqs, key=freqs.get, reverse=True)

    mapping = make_identity_pairs()

    #to avoid duplicate entries
    used_out = set()
    assigned = set()
    i = 0
    j = 0
    #map new pairs : most frequent in cipher to most frequent from common freq
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
    out = []
    #making the substitutions in the actual cipher
    for ch in text:
        if ch.isalpha():
            up = ch.upper()
            out.append(mapping.get(up, up))
        else:
            out.append(ch)
    return "".join(out)

def associate(mapping: dict[str, str], a: str, b: str) -> None:
    p = a.upper()
    q = b.upper()

    if p not in ALPHABET or q not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    if p == q:
        return

    cp = next((k for k, v in mapping.items() if v == p), None)
    cq = next((k for k, v in mapping.items() if v == q), None)

    if cp is None or cq is None:
        print(f"Cannot swap '{p}' and '{q}' because one of them is not currently produced by the mapping.")
        return

    mapping[cp], mapping[cq] = q, p

def force_cipher_to_plain(mapping: dict[str,str], c: str, p: str) -> None:
    c = c.upper()
    p = p.upper()
    if c not in ALPHABET or p not in ALPHABET:
        raise ValueError("Letters must be A-Z.")

    old_p = mapping[c]                       # what c used to decode to
    other = next((k for k, v in mapping.items() if v == p), None)

    mapping[c] = p                           # set it

    if other is not None and other != c:     # fix collision
        mapping[other] = old_p

def top_trigrams(text: str, n: int = 10) -> list:
    #get all the letters in the text
    letters = [ch for ch in text.upper() if ch.isalpha()]
    if len(letters) < 3:
        return []
    #compute the trigrams as the groupings of 3 letters from each initial position to the end of the text
    trigs = (letters[i] + letters[i + 1] + letters[i + 2] for i in range(len(letters) - 2))
    # most commmon is a built in function that returns the n most common elements in descending order
    return Counter(trigs).most_common(n)

class MonoalphabeticCrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monoalphabetic Cipher Cracker")
        self.geometry("1200x800")

        self.ct = ""
        self.mapping = make_identity_pairs()

        self._build_ui()
        self._build_plot()

    def _build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top, text="Ciphertext:").pack(side=tk.LEFT)
        self.ct_entry = ttk.Entry(top, width=90)
        self.ct_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

        ttk.Button(top, text="Load", command=self.load_cipher).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Seed by Freq", command=self.seed_mapping).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Reset", command=self.reset_mapping).pack(side=tk.LEFT, padx=5)

        mid = ttk.Frame(self, padding=10)
        mid.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        left = ttk.Frame(mid)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = ttk.Frame(mid)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(left, text="Decrypted Output:").pack(anchor="w")
        self.out_text = tk.Text(left, wrap="word", height=18)
        self.out_text.pack(fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Trigrams (Decrypted):").pack(anchor="w", pady=(10, 0))
        self.tri_text = tk.Text(left, wrap="none", height=7)
        self.tri_text.pack(fill=tk.X)

        swap_frame = ttk.LabelFrame(right, text="Swap", padding=10)
        swap_frame.pack(fill=tk.X, pady=5)

        ttk.Label(swap_frame, text="Type 2 letters (e.g., ET):").grid(row=0, column=0, sticky="w")
        self.swap_entry = ttk.Entry(swap_frame, width=6)
        self.swap_entry.grid(row=0, column=1, padx=6, sticky="w")
        ttk.Button(swap_frame, text="Swap", command=self.do_swap).grid(row=1, column=0, columnspan=2, pady=8, sticky="ew")

        force_frame = ttk.LabelFrame(right, text="assign", padding=10)
        force_frame.pack(fill=tk.X, pady=5)

        ttk.Label(force_frame, text="Type 2 letters (e.g., XE means X->E):").grid(row=0, column=0, sticky="w")
        self.force_entry = ttk.Entry(force_frame, width=6)
        self.force_entry.grid(row=0, column=1, padx=6, sticky="w")
        ttk.Button(force_frame, text="Force", command=self.do_force).grid(row=1, column=0, columnspan=2, pady=8, sticky="ew")

        map_frame = ttk.LabelFrame(right, text="Mapping", padding=10)
        map_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.map_list = tk.Listbox(map_frame, height=20, width=18)
        self.map_list.pack(fill=tk.BOTH, expand=True)

        btns = ttk.Frame(right, padding=10)
        btns.pack(fill=tk.X)

        ttk.Button(btns, text="Update View", command=self.refresh_all).pack(fill=tk.X, pady=3)
        ttk.Button(btns, text="Check Monoalphabetic", command=self.check_mapping).pack(fill=tk.X, pady=3)

    def _build_plot(self):
        plot_frame = ttk.LabelFrame(self, text="Letter Frequencies", padding=10)
        plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.fig = plt.Figure(figsize=(10, 2.6), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_cipher(self):
        self.ct = self.ct_entry.get().rstrip("\n")
        if not self.ct.strip():
            messagebox.showwarning("Empty", "Please enter ciphertext.")
            return
        self.refresh_all()

    def seed_mapping(self):
        if not self.ct.strip():
            self.load_cipher()
            if not self.ct.strip():
                return
        self.mapping = initial_mapping_by_frequency(self.ct.upper())
        self.refresh_all()

    def reset_mapping(self):
        self.mapping = make_identity_pairs()
        self.refresh_all()

    def _parse_two_letters(self, s: str) -> tuple[str, str] | None:
        raw = "".join(ch for ch in (s or "").upper() if ch.isalpha())
        if len(raw) != 2:
            return None
        return raw[0], raw[1]

    def do_swap(self):
        parsed = self._parse_two_letters(self.swap_entry.get())
        if parsed is None:
            messagebox.showwarning("Input", "Enter exactly 2 letters (e.g., ET).")
            return
        a, b = parsed
        try:
            associate(self.mapping, a, b)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.refresh_all()

    def do_force(self):
        parsed = self._parse_two_letters(self.force_entry.get())
        if parsed is None:
            messagebox.showwarning("Input", "Enter exactly 2 letters (e.g., XE).")
            return
        c, p = parsed
        try:
            force_cipher_to_plain(self.mapping, c, p)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.refresh_all()

    def refresh_all(self):
        self._update_output()
        self._update_trigrams()
        self._update_mapping_list()
        self._update_plot()

    def _update_output(self):
        self.out_text.delete("1.0", tk.END)
        if not self.ct:
            return
        self.out_text.insert(tk.END, decode(self.ct, self.mapping))

    def _update_trigrams(self):
        self.tri_text.delete("1.0", tk.END)
        if not self.ct:
            return
        plain = decode(self.ct, self.mapping)
        trigs = top_trigrams(plain, n=12)
        if not trigs:
            self.tri_text.insert(tk.END, "No trigrams (need at least 3 letters).")
            return
        for i, (tri, k) in enumerate(trigs, start=1):
            self.tri_text.insert(tk.END, f"{i:2d}) {tri} -> {k}\n")

    def _update_mapping_list(self):
        self.map_list.delete(0, tk.END)
        for c in ALPHABET:
            self.map_list.insert(tk.END, f"{c} -> {self.mapping.get(c, c)}")

    def _update_plot(self):
        self.ax.clear()
        if not self.ct.strip():
            self.canvas.draw()
            return

        ct_freq = letter_freq(self.ct.upper())
        english_by_letter = {ch: val for ch, val in zip(COMMON_FREQ, COMMON_VALS)}

        letters = list(ALPHABET)
        ct_vals = [ct_freq[c] for c in letters]
        en_vals = [english_by_letter[c] for c in letters]

        x = list(range(len(letters)))
        w = 0.42

        self.ax.bar([i - w/2 for i in x], ct_vals, width=w, edgecolor="black", label="Cipher")
        self.ax.bar([i + w/2 for i in x], en_vals, width=w, edgecolor="black", label="English")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(letters)
        self.ax.set_title("Letter Frequencies: Ciphertext vs English")
        self.ax.set_xlabel("Letter")
        self.ax.set_ylabel("Frequency")
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def check_mapping(self):
        ok = check_func(self.mapping)
        messagebox.showinfo("Mapping Check", f"Mapping OK? {ok}")

if __name__ == "__main__":
    app = MonoalphabeticCrackerGUI()
    app.mainloop()