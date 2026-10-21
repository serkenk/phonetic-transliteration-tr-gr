import re
import tkinter as tk
from tkinter import ttk


def tr_to_greek(text: str) -> str:
    # 1. 'nd' bileşikleri (d ile karışmaması için 'νντ')
    text = re.sub(r"nd", "νντ", text)
    text = re.sub(r"Nd", "Νντ", text)
    text = re.sub(r"ND", "ΝΝΤ", text)

    # 2. Diftonglar ve fonetik ikililer
    text = re.sub(r"(?i)va", "υα", text)
    text = re.sub(r"(?i)ev|ef", "ευ", text)
    text = re.sub(r"(?i)av\b|af\b", "αυ", text)

    # 3. 'y' harfi -> 'ι' / 'Ι' (g sesi 'γ' ile çakışmayı önlemek için)
    text = text.replace("y", "ι").replace("Y", "Ι")

    # 4. Standart harf eşlemeleri ('g' doğrudan 'γ')
    mapping = [
        ("ç", "τσ"),
        ("Ç", "Τσ"),
        ("c", "τζ"),
        ("C", "Τz"),
        ("d", "ντ"),
        ("D", "Ντ"),
        ("b", "μπ"),
        ("B", "Μπ"),
        ("u", "ου"),
        ("U", "Ου"),
        ("ş", "ς"),
        ("Ş", "Σ"),
        ("ğ", "γ"),
        ("Ğ", "Γ"),
        ("g", "γ"),
        ("G", "Γ"),
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

    text = re.sub(r"σ(?=[^\w]|$)", "ς", text)
    return text


def greek_to_tr(text: str) -> str:
    # 1. 'nd' çözümü
    text = text.replace("Νντ", "Nd").replace("ΝΝΤ", "ND").replace("νντ", "nd")

    # 2. Diftong ve bileşik sesler
    compounds = [
        ("ευ", "ev"),
        ("Ευ", "Ev"),
        ("ΕΥ", "EV"),
        ("αυ", "av"),
        ("Αυ", "Av"),
        ("ΑΥ", "AV"),
        ("υα", "va"),
        ("Υα", "Va"),
        ("ΥΑ", "VA"),
        ("ου", "u"),
        ("Ου", "U"),
        ("ΟΥ", "U"),
        ("μπ", "b"),
        ("Μπ", "B"),
        ("ΜΠ", "B"),
        ("τσ", "ç"),
        ("Τσ", "Ç"),
        ("ΤΣ", "Ç"),
        ("τζ", "c"),
        ("Τz", "C"),
        ("ΤΖ", "C"),
    ]
    for gr, tr in compounds:
        text = text.replace(gr, tr)

    # 3. 'ντ' -> 'd' çözümü (Türkçe fiil çekimleri ve ekler 'd' sesidir: eder, bakmadan, gider)
    text = text.replace("Ντ", "D").replace("ντ", "d")

    # 4. 'ι' / 'Ι' -> 'y' çözümü (ünlü yanındaki yarı-ünlüler)
    text = re.sub(r"\bΙ(?=[αεηοωυ])", "Y", text)
    text = re.sub(r"\bι(?=[αεηοωυ])", "y", text)
    text = re.sub(r"(?<=[αεηοωυ])ι(?=[αεηοωυ])", "y", text)
    text = re.sub(r"(?<=[αεηοωυ])ι\b", "y", text)

    # 5. 'γ' çözümü:
    # İnce ünlüler (υ, ε, ι, ω) önünde sert ses: 'g' (bugün, gibi, gözünün, gider)
    text = re.sub(r"γ(?=[υειω])", "g", text)
    text = re.sub(r"Γ(?=[υειω])", "G", text)
    # Kalın ünlüler (α, η) arasında yumuşak ses: 'ğ' (çağımızdaki)
    text = re.sub(r"(?<=[αη])γ(?=[αη])", "ğ", text)
    # Kalan tekil 'γ' karakterleri 'g' olarak eşlenir
    text = text.replace("Γ", "G").replace("γ", "g")

    # 6. Tekil standart harfler
    singles = [
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
    ]
    for gr, tr in singles:
        text = text.replace(gr, tr)

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

btn_translate = ttk.Button(root, text="Çevir", command=on_translate)
btn_translate.pack(pady=5)

ttk.Label(root, text="Sonuç:").pack(anchor="w", padx=20)
text_output = tk.Text(root, height=6, width=60, state=tk.DISABLED, bg="#f3f3f3")
text_output.pack(padx=20, pady=(0, 10))

root.mainloop()
