import re
import tkinter as tk
from tkinter import ttk

def tr_to_greek(text: str) -> str:
    # 1. Kelime sınırına bağlı diftonglar
    text = re.sub(r'\b(ev|ef)\b', 'ευ', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\w)(ev|ef)\b', 'ευ', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(ev|ef)', 'ευ', text, flags=re.IGNORECASE)
    text = re.sub(r'(av|af)\b', 'αυ', text, flags=re.IGNORECASE)

    # 2. Çoklu ünsüzler ve harf haritası
    # 'y' harfi için bağlam analizi
    def replace_y(match):
        idx = match.start()
        prev_c = text[idx - 1] if idx > 0 else ''
        if prev_c.lower() in "aeıioöuüαεηιοωυ":
            return 'ι'
        return 'γ'

    text = re.sub(r'[yY]', replace_y, text)

    # Birebir ve çoklu eşleme tablosu (ı ve i kesin olarak ayrılmıştır)
    mapping = [
        ('ç', 'τσ'), ('Ç', 'ΤΣ'),
        ('c', 'τζ'), ('C', 'ΤΖ'),
        ('d', 'ντ'), ('D', 'ΝΤ'),
        ('b', 'μπ'), ('B', 'ΜΠ'),
        ('u', 'ου'), ('U', 'ΟΥ'),
        ('ş', 'ς'),  ('Ş', 'Σ'),
        ('g', 'γ'),  ('G', 'Γ'),
        ('ğ', 'γ'),  ('Ğ', 'Γ'),
        ('ö', 'ω'),  ('Ö', 'Ω'),
        ('o', 'ο'),  ('O', 'Ο'),
        ('ı', 'η'),  ('I', 'Η'),
        ('i', 'ι'),  ('İ', 'Ι'),
        ('h', 'χ'),  ('H', 'Χ'),
        ('a', 'α'),  ('A', 'Α'),
        ('e', 'ε'),  ('E', 'Ε'),
        ('f', 'φ'),  ('F', 'Φ'),
        ('j', 'ζ'),  ('J', 'Ζ'),
        ('k', 'κ'),  ('K', 'Κ'),
        ('l', 'λ'),  ('L', 'Λ'),
        ('m', 'μ'),  ('M', 'Μ'),
        ('n', 'ν'),  ('N', 'Ν'),
        ('p', 'π'),  ('P', 'Π'),
        ('r', 'ρ'),  ('R', 'Ρ'),
        ('s', 'σ'),  ('S', 'Σ'),
        ('t', 'τ'),  ('T', 'Τ'),
        ('ü', 'υ'),  ('Ü', 'Υ'),
        ('v', 'β'),  ('V', 'Β'),
        ('z', 'ζ'),  ('Z', 'Ζ')
    ]

    for tr_char, gr_char in mapping:
        text = text.replace(tr_char, gr_char)

    # Kelime sonundaki standart 'σ' harfini 'ς' yapma
    text = re.sub(r'σ(?=[^\w]|$)', 'ς', text)
    return text

def greek_to_tr(text: str) -> str:
    rules = [
        ('ευ', 'ev'), ('ΕΥ', 'EV'),
        ('αυ', 'av'), ('ΑΥ', 'AV'),
        ('ου', 'u'),  ('ΟΥ', 'U'),
        ('ντ', 'd'),  ('ΝΤ', 'D'),
        ('μπ', 'b'),  ('ΜΠ', 'B'),
        ('τσ', 'ç'),  ('ΤΣ', 'Ç'),
        ('τζ', 'c'),  ('ΤΖ', 'C'),
        ('α', 'a'),   ('Α', 'A'),
        ('β', 'v'),   ('Β', 'V'),
        ('ε', 'e'),   ('Ε', 'E'),
        ('ζ', 'z'),   ('Ζ', 'Z'),
        ('η', 'ı'),   ('Η', 'I'),
        ('ι', 'i'),   ('Ι', 'İ'),
        ('κ', 'k'),   ('Κ', 'K'),
        ('λ', 'l'),   ('Λ', 'L'),
        ('μ', 'm'),   ('Μ', 'M'),
        ('ν', 'n'),   ('Ν', 'N'),
        ('ο', 'o'),   ('Ο', 'O'),
        ('π', 'p'),   ('Π', 'P'),
        ('ρ', 'r'),   ('Ρ', 'R'),
        ('σ', 's'),   ('Σ', 'S'),
        ('ς', 'ş'),
        ('τ', 't'),   ('Τ', 'T'),
        ('υ', 'ü'),   ('Υ', 'Ü'),
        ('φ', 'f'),   ('Φ', 'F'),
        ('χ', 'h'),   ('Χ', 'H'),
        ('ω', 'ö'),   ('Ω', 'Ö'),
        ('γ', 'g'),   ('Γ', 'G')
    ]

    # Grekçe diftong 'ι' ve sesli öncesi 'γ' çözümlemeleri
    text = re.sub(r'(?<=[αεηιοω])ι', 'y', text)
    text = re.sub(r'γ(?=[αεηιοω])', 'y', text)

    for gr_char, tr_char in rules:
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
root.geometry("460x420")
root.resizable(False, False)

mode_var = tk.StringVar(value="tr_to_el")
frame_mode = ttk.Frame(root)
frame_mode.pack(pady=10)

ttk.Radiobutton(frame_mode, text="Türkçe -> Grek", variable=mode_var, value="tr_to_el").pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(frame_mode, text="Grek -> Türkçe", variable=mode_var, value="el_to_tr").pack(side=tk.LEFT, padx=10)

ttk.Label(root, text="Girdi Metni:").pack(anchor="w", padx=20)
text_input = tk.Text(root, height=4, width=52)
text_input.pack(padx=20, pady=(0, 10))

ttk.Button(root, text="Çevir", command=on_translate).pack(pady=5)

ttk.Label(root, text="Sonuç:").pack(anchor="w", padx=20)
text_output = tk.Text(root, height=4, width=52, state=tk.DISABLED, bg="#f3f3f3")
text_output.pack(padx=20, pady=(0, 10))

root.mainloop()