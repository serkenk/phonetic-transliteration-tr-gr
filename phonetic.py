import re
import tkinter as tk
from tkinter import ttk

VOWELS_TR = "aeıioöuüAEIİOÖUÜ"

def tr_to_greek(text: str) -> str:
    # 1. Öncelikli çoklu ses ve diftong dönüşümleri
    compound_rules = [
        (r'(?i)\bev', 'ευ'),
        (r'(?i)\bef', 'ευ'),
        (r'(?i)ev\b', 'ευ'),
        (r'(?i)ef\b', 'ευ'),
        (r'(?i)av\b', 'αυ'),
        (r'(?i)af\b', 'αυ'),
        (r'(?i)ç', 'τσ'),
        (r'(?i)c', 'τζ'),
        (r'(?i)d', 'ντ'),
        (r'(?i)b', 'μπ'),
        (r'(?i)u', 'ου'),
        (r'(?i)ş', 'ς'),
        (r'(?i)[gğ]', 'γ'),
        (r'(?i)ö', 'ω'),
        (r'(?i)o', 'ο'),
        (r'(?i)ı', 'η'),
        (r'(?i)i', 'ι'),
        (r'(?i)h', 'χ'),
    ]
    for pattern, rep in compound_rules:
        text = re.sub(pattern, rep, text)

    # 2. Fonetik 'y' analizi (diftong / ünsüz ayrımı)
    def replace_y(match):
        idx = match.start()
        prev_c = text[idx - 1] if idx > 0 else ''
        if prev_c in "αεηιοωυΑΕΗΙΟΩΥ":
            return 'ι'
        return 'γ'

    text = re.sub(r'(?i)y', replace_y, text)

    # 3. Kalan standart harfler
    single_rules = [
        (r'(?i)a', 'α'), (r'(?i)e', 'ε'), (r'(?i)f', 'φ'),
        (r'(?i)j', 'ζ'), (r'(?i)k', 'κ'), (r'(?i)l', 'λ'),
        (r'(?i)m', 'μ'), (r'(?i)n', 'ν'), (r'(?i)p', 'π'),
        (r'(?i)r', 'ρ'), (r'(?i)s', 'σ'), (r'(?i)t', 'τ'),
        (r'(?i)ü', 'υ'), (r'(?i)v', 'β'), (r'(?i)z', 'ζ')
    ]
    for pattern, rep in single_rules:
        text = re.sub(pattern, rep, text)

    # 4. Kelime sonundaki standart 'σ' harfini 'ς' yapma
    text = re.sub(r'σ(?=[^\w]|$)', 'ς', text)
    return text

def greek_to_tr(text: str) -> str:
    # Çoklu karakterlerden tekillere doğru sıralı çözümleme
    rules = [
        (r'(?i)ευ', 'ev'),
        (r'(?i)αυ(?=[^\w]|$)', 'av'),
        (r'(?i)ου', 'u'),
        (r'(?i)ντ', 'd'),
        (r'(?i)μπ', 'b'),
        (r'(?i)τσ', 'ç'),
        (r'(?i)τζ', 'c'),
        # Diftong 'ι' -> 'y' (ünlüden sonra veya önce gelirse)
        (r'(?<=[αεηιοω])ι', 'y'),
        (r'ι(?=[αεηιοω])', 'y'),
        # γ -> 'y' (ünlü öncesi sürtünmeli ses) veya 'g'
        (r'γ(?=[αεηιοω])', 'y'),
        (r'(?i)γ', 'g'),
        # Standart sesler
        (r'(?i)α', 'a'), (r'(?i)β', 'v'), (r'(?i)ε', 'e'),
        (r'(?i)ζ', 'z'), (r'(?i)η', 'ı'), (r'(?i)ι', 'i'),
        (r'(?i)κ', 'k'), (r'(?i)λ', 'l'), (r'(?i)μ', 'm'),
        (r'(?i)ν', 'n'), (r'(?i)ο', 'o'), (r'(?i)π', 'p'),
        (r'(?i)ρ', 'r'), (r'(?i)σ', 's'), (r'(?i)ς', 'ş'),
        (r'(?i)τ', 't'), (r'(?i)υ', 'ü'), (r'(?i)φ', 'f'),
        (r'(?i)χ', 'h'), (r'(?i)ω', 'ö')
    ]
    for pattern, rep in rules:
        text = re.sub(pattern, rep, text)
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