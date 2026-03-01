import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
from operator import itemgetter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COMMON_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
COMMON_VALS = [
    0.12702, 0.09056, 0.08167, 0.07507, 0.06966, 0.06749, 0.06327, 0.06094, 0.05987,
    0.04253, 0.04025, 0.02782, 0.02758, 0.02406, 0.02360, 0.02228, 0.02015, 0.01974,
    0.01929, 0.01492, 0.00978, 0.00772, 0.00153, 0.00150, 0.00095, 0.00074
]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter_freq(text: str) -> dict[str, float]:
    letters = [ch for ch in text.upper() if ch.isalpha()]
    total = len(letters)
    freqs = {c: 0.0 for c in ALPHABET}
    if total == 0:
        return freqs
    counts = Counter(letters)
    for c in ALPHABET:
        freqs[c] = counts.get(c, 0) / total
    return freqs


def make_identity_pairs() -> dict[str, str]:
    return {c: c for c in ALPHABET}


def is_reciprocal(mapping: dict[str, str]) -> bool:
    for a in ALPHABET:
        b = mapping.get(a, a)
        if b not in ALPHABET:
            return False
        if mapping.get(b, b) != a:
            return False
    return True


def set_pair(mapping: dict[str, str], a: str, b: str) -> None:
    a = a.upper()
    b = b.upper()
    if a not in ALPHABET or b not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    mapping[a] = b
    mapping[b] = a


def initial_reciprocal_mapping_by_frequency(ciphertext: str) -> dict[str, str]:
    freqs = letter_freq(ciphertext)
    ranked = [c for c, _ in sorted(freqs.items(), key=itemgetter(1), reverse=True)]

    mapping = make_identity_pairs()
    used = set()

    i = 0
    j = 0
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


def decode(text: str, mapping: dict[str, str]) -> str:
    out = []
    for ch in text:
        if ch.isalpha():
            up = ch.upper()
            out.append(mapping.get(up, up))
        else:
            out.append(ch)
    return "".join(out)


def associate(mapping: dict[str, str], a: str, b: str) -> None:
    a = a.upper()
    b = b.upper()
    if a not in ALPHABET or b not in ALPHABET:
        raise ValueError("Letters must be A-Z.")
    if a == b:
        return


    c1 = mapping.get(a, a)
    

    x = c1
    y = b
  
    xp = mapping.get(x, x) 
    yp = mapping.get(y, y)
    
  
    orphans = {xp, yp} - {x, y}
    
  
    set_pair(mapping, x, y)
    
 
    if len(orphans) == 2:
        o1, o2 = orphans
        set_pair(mapping, o1, o2)
    elif len(orphans) == 1:
        o1 = orphans.pop()
        set_pair(mapping, o1, o1)


def top_trigrams(text: str, n: int = 10) -> list[tuple[str, int]]:
    letters = [ch for ch in text.upper() if ch.isalpha()]
    if len(letters) < 3:
        return []
    trigs = (letters[i] + letters[i + 1] + letters[i + 2] for i in range(len(letters) - 2))
    return Counter(trigs).most_common(n)


class ReciprocalCrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reciprocal Cipher Cracker")
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

        assoc_frame = ttk.LabelFrame(right, text="Associate Pair", padding=10)
        assoc_frame.pack(fill=tk.X, pady=5)

        ttk.Label(assoc_frame, text="Letter 1:").grid(row=0, column=0, sticky="w")
        self.a_var = tk.StringVar()
        self.a_box = ttk.Combobox(assoc_frame, textvariable=self.a_var, values=list(ALPHABET), width=3, state="readonly")
        self.a_box.grid(row=0, column=1, padx=5)

        ttk.Label(assoc_frame, text="Letter 2:").grid(row=1, column=0, sticky="w")
        self.b_var = tk.StringVar()
        self.b_box = ttk.Combobox(assoc_frame, textvariable=self.b_var, values=list(ALPHABET), width=3, state="readonly")
        self.b_box.grid(row=1, column=1, padx=5)

        ttk.Button(assoc_frame, text="ASOC", command=self.do_associate).grid(row=2, column=0, columnspan=2, pady=8, sticky="ew")

        map_frame = ttk.LabelFrame(right, text="Mapping", padding=10)
        map_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.map_list = tk.Listbox(map_frame, height=20, width=18)
        self.map_list.pack(fill=tk.BOTH, expand=True)

        btns = ttk.Frame(right, padding=10)
        btns.pack(fill=tk.X)

        ttk.Button(btns, text="Update View", command=self.refresh_all).pack(fill=tk.X, pady=3)
        ttk.Button(btns, text="Check Reciprocal", command=self.check_reciprocal).pack(fill=tk.X, pady=3)

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
        self.mapping = initial_reciprocal_mapping_by_frequency(self.ct.upper())
        self.refresh_all()

    def reset_mapping(self):
        self.mapping = make_identity_pairs()
        self.refresh_all()

    def do_associate(self):
        a = (self.a_var.get() or "").strip().upper()
        b = (self.b_var.get() or "").strip().upper()
        if len(a) != 1 or len(b) != 1:
            messagebox.showwarning("Input", "Choose two letters.")
            return
        try:
            associate(self.mapping, a, b)
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

    def check_reciprocal(self):
        ok = is_reciprocal(self.mapping)
        messagebox.showinfo("Reciprocity Check", f"Reciprocal OK? {ok}")


if __name__ == "__main__":
    app = ReciprocalCrackerGUI()
    app.mainloop()