import re
import tkinter as tk
from tkinter import ttk

VOWELS_TR = set("aeıioöuüAEIİOÖUÜαεηιοωυΑΕΗΙΟΩΥ")


def tr_to_greek(text: str) -> str:
    # 1. 'nd' bileşiği: 'n' + 'd' durumunda çift 'ν' oluşmasını engeller
    text = re.sub(r"nd", "ντ", text, flags=re.IGNORECASE)
    text = re.sub(r"Nd|ND", "Ντ", text)

    # 2. Fonetik diftonglar ve 'va' / 'ev' kuralları (kelime içi dahil)
    text = re.sub(r"(?i)va", "υα", text)
    text = re.sub(r"(?i)ev|ef", "ευ", text)
    text = re.sub(r"(?i)av\b|af\b", "αυ", text)

    # 3. 'y' harfi fonetik analizi (öncesinde sesli varsa 'ι', yoksa 'γ')
    def replace_y(match):
        idx = match.start()
        prev_c = text[idx - 1] if idx > 0 else ""
        is_upper = match.group(0).isupper()
        if prev_c in VOWELS_TR:
            return "Ι" if is_upper else "ι"
        return "Γ" if is_upper else "γ"

    text = re.sub(r"[yY]", replace_y, text)

    # 4. Standart ve çift harf eşlemeleri
    mapping = [
        ("ç", "τσ"),
        ("Ç", "Τσ"),
        ("c", "τζ"),
        ("C", "Τζ"),
        ("d", "ντ"),
        ("D", "Ντ"),
        ("b", "μπ"),
        ("B", "Μπ"),
        ("u", "ου"),
        ("U", "Ου"),
        ("ş", "ς"),
        ("Ş", "Σ"),
        ("g", "γ"),
        ("G", "Γ"),
        ("ğ", "γ"),
        ("Ğ", "Γ"),
        ("ö", "ω"),
        ("Ö", "Ω"),
        ("o", "ο"),
        ("O", "Ο"),
        ("ı", "η"),
        ("I", "Η"),
        ("i", "ι"),
        ("İ", "Ι"),
        ("h", "χ"),
        ("H", "Χ"),
        ("a", "α"),
        ("A", "Α"),
        ("e", "ε"),
        ("E", "Ε"),
        ("f", "φ"),
        ("F", "Φ"),
        ("j", "ζ"),
        ("J", "Ζ"),
        ("k", "κ"),
        ("K", "Κ"),
        ("l", "λ"),
        ("L", "Λ"),
        ("m", "μ"),
        ("M", "Μ"),
        ("n", "ν"),
        ("N", "Ν"),
        ("p", "π"),
        ("P", "Π"),
        ("r", "ρ"),
        ("R", "Ρ"),
        ("s", "σ"),
        ("S", "Σ"),
        ("t", "τ"),
        ("T", "Τ"),
        ("ü", "υ"),
        ("Ü", "Υ"),
        ("v", "β"),
        ("V", "Β"),
        ("z", "ζ"),
        ("Z", "Ζ"),
    ]

    for tr_char, gr_char in mapping:
        text = text.replace(tr_char, gr_char)

    # 5. Kelime sonu 'σ' harfini 'ς' yapma
    text = re.sub(r"σ(?=[^\w]|$)", "ς", text)
    return text


def greek_to_tr(text: str) -> str:
    rules = [
        ("ευ", "ev"),
        ("ΕΥ", "EV"),
        ("Ευ", "Ev"),
        ("αυ", "av"),
        ("ΑΥ", "AV"),
        ("Αυ", "Av"),
        ("υα", "va"),
        ("ΥΑ", "VA"),
        ("Υα", "Va"),
        ("ου", "u"),
        ("ΟΥ", "U"),
        ("Ου", "U"),
        ("ντ", "d"),
        ("ΝΤ", "D"),
        ("Ντ", "D"),
        ("μπ", "b"),
        ("ΜΠ", "B"),
        ("Μπ", "B"),
        ("τσ", "ç"),
        ("ΤΣ", "Ç"),
        ("Τσ", "Ç"),
        ("τζ", "c"),
        ("ΤΖ", "C"),
        ("Τζ", "C"),
    ]
    for gr_char, tr_char in rules:
        text = text.replace(gr_char, tr_char)

    text = re.sub(r"(?<=[aeıioöuüαεηιοωυ])ι", "y", text, flags=re.IGNORECASE)
    text = re.sub(r"γ(?=[aeıioöuüαεηιοωυ])", "y", text, flags=re.IGNORECASE)

    single_rules = [
        ("α", "a"),
        ("Α", "A"),
        ("β", "v"),
        ("Β", "V"),
        ("ε", "e"),
        ("Ε", "E"),
        ("ζ", "z"),
        ("Ζ", "Z"),
        ("η", "ı"),
        ("Η", "I"),
        ("ι", "i"),
        ("Ι", "İ"),
        ("κ", "k"),
        ("Κ", "K"),
        ("λ", "l"),
        ("Λ", "L"),
        ("μ", "m"),
        ("Μ", "M"),
        ("ν", "n"),
        ("Ν", "N"),
        ("ο", "o"),
        ("Ο", "O"),
        ("π", "p"),
        ("Π", "P"),
        ("ρ", "r"),
        ("Ρ", "R"),
        ("σ", "s"),
        ("Σ", "S"),
        ("ς", "ş"),
        ("τ", "t"),
        ("Τ", "T"),
        ("υ", "ü"),
        ("Υ", "Ü"),
        ("φ", "f"),
        ("Φ", "F"),
        ("χ", "h"),
        ("Χ", "H"),
        ("ω", "ö"),
        ("Ω", "Ö"),
        ("γ", "g"),
        ("Γ", "G"),
    ]
    for gr_char, tr_char in single_rules:
        text = text.replace(gr_char, tr_char)

    return text


def on_translate():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        return
    mode = mode_var.get()
    result = tr_to_greek(input_text) if mode == "tr_to_el" else greek_to_tr(input_text)

    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, result)
    text_output.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Fonetik Çevirici (TR <-> Grek)")
root.geometry("520x450")
root.resizable(False, False)

mode_var = tk.StringVar(value="tr_to_el")
frame_mode = ttk.Frame(root)
frame_mode.pack(pady=10)

ttk.Radiobutton(
    frame_mode, text="Türkçe -> Grek", variable=mode_var, value="tr_to_el"
).pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(
    frame_mode, text="Grek -> Türkçe", variable=mode_var, value="el_to_tr"
).pack(side=tk.LEFT, padx=10)

ttk.Label(root, text="Girdi Metni:").pack(anchor="w", padx=20)
text_input = tk.Text(root, height=6, width=60)
text_input.pack(padx=20, pady=(0, 10))

ttk.Button(root, text="Çevir", command=on_translate).pack(pady=5)

ttk.Label(root, text="Sonuç:").pack(anchor="w", padx=20)
text_output = tk.Text(root, height=6, width=60, state=tk.DISABLED, bg="#f3f3f3")
text_output.pack(padx=20, pady=(0, 10))

root.mainloop()
