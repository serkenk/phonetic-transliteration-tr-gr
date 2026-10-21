import re
import tkinter as tk


def tr_to_greek(text: str) -> str:
    # 'd' sesi ile çakışmayı önlemek için 'nd' ve 'nt' öncelikli işlenir
    text = re.sub(r"nd", "νντ", text)
    text = re.sub(r"Nd", "Νντ", text)
    text = re.sub(r"ND", "ΝΝΤ", text)
    text = re.sub(r"nt", "νθ", text)
    text = re.sub(r"Nt", "Νθ", text)
    text = re.sub(r"NT", "ΝΘ", text)

    # Fonetik diftonglar ve ses benzerlikleri
    text = re.sub(r"(?i)va", "υα", text)
    text = re.sub(r"(?i)ev|ef", "ευ", text)
    text = re.sub(r"(?i)av\b|af\b", "αυ", text)

    # 'y' sesi 'g' (γ) ile çakışmaması için yarı-ünlü 'ι' olarak eşlenir
    text = text.replace("y", "ι").replace("Y", "Ι")

    # Birebir ve çoklu harf eşleme tablosu
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

    # Kelime sonundaki standart 'σ' harfini 'ς' formuna dönüştür
    text = re.sub(r"σ(?=[^\w]|$)", "ς", text)
    return text


def greek_to_tr(text: str) -> str:
    # Özel bileşik seslerin tersine çevrimi
    text = text.replace("Νντ", "Nd").replace("ΝΝΤ", "ND").replace("νντ", "nd")
    text = text.replace("Νθ", "Nt").replace("ΝΘ", "NT").replace("νθ", "nt")

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

    text = text.replace("Ντ", "D").replace("ντ", "d")

    # Ünlü komşuluğundaki yarı-ünlü 'ι' -> 'y'
    text = re.sub(r"\bΙ(?=[αεηοωυ])", "Y", text)
    text = re.sub(r"\bι(?=[αεηοωυ])", "y", text)
    text = re.sub(r"(?<=[αεηοωυ])ι(?=[αεηοωυ])", "y", text)
    text = re.sub(r"(?<=[αεηοωυ])ι\b", "y", text)

    # Fonetik bağlama göre 'γ' harfinin 'g' veya 'ğ' ayrımı
    text = re.sub(r"γ(?=[υειω])", "g", text)
    text = re.sub(r"Γ(?=[υειω])", "G", text)
    text = re.sub(r"(?<=[αη])γ(?=[αη])", "ğ", text)
    text = text.replace("Γ", "G").replace("γ", "g")

    # Tekil harflerin Türkçe karşılıkları
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


class TransliterationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fonetik Çevirici (TR ⇄ Grek)")
        self.root.geometry("620x680")
        self.root.minsize(500, 550)
        self.root.configure(bg="#121212")

        self.mode = "tr_to_el"

        # Renk paleti
        self.bg_color = "#121212"
        self.card_bg = "#1e1e1e"
        self.text_bg = "#252526"
        self.fg_primary = "#ffffff"
        self.fg_secondary = "#a0a0a0"
        self.accent_color = "#2563eb"

        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.root, bg=self.bg_color, padx=24, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Başlık alanı
        header_frame = tk.Frame(container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 16))

        title = tk.Label(
            header_frame,
            text="Fonetik Çevirici",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_primary,
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header_frame,
            text="Türkçe ve Eski Grek Alfabesi Arasında Fonetik Transliterasyon",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.fg_secondary,
        )
        subtitle.pack(anchor="w")

        # Çeviri yönü ve değiştirme çubuğu
        bar = tk.Frame(container, bg=self.card_bg, padx=12, pady=8)
        bar.pack(fill=tk.X, pady=(0, 16))

        self.lbl_src = tk.Label(
            bar,
            text="Türkçe",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_bg,
            fg=self.fg_primary,
        )
        self.lbl_src.pack(side=tk.LEFT, padx=8)

        self.btn_swap = tk.Button(
            bar,
            text="⇄ Değiştir",
            font=("Segoe UI", 9),
            bg=self.text_bg,
            fg=self.fg_primary,
            activebackground=self.accent_color,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.swap_modes,
        )
        self.btn_swap.pack(side=tk.LEFT, padx=10)

        self.lbl_dst = tk.Label(
            bar,
            text="Grek Alfabesi",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_bg,
            fg=self.accent_color,
        )
        self.lbl_dst.pack(side=tk.LEFT, padx=8)

        # Girdi metin kutusu
        lbl_input_title = tk.Label(
            container,
            text="GİRDİ",
            font=("Segoe UI", 8, "bold"),
            bg=self.bg_color,
            fg=self.fg_secondary,
        )
        lbl_input_title.pack(anchor="w", pady=(0, 4))

        self.txt_input = tk.Text(
            container,
            height=6,
            font=("Segoe UI", 11),
            bg=self.text_bg,
            fg=self.fg_primary,
            insertbackground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=10,
        )
        self.txt_input.pack(fill=tk.BOTH, expand=True, pady=(0, 14))
        self.txt_input.bind("<KeyRelease>", self.on_text_change)

        # Çıktı metin kutusu
        lbl_output_title = tk.Label(
            container,
            text="SONUÇ",
            font=("Segoe UI", 8, "bold"),
            bg=self.bg_color,
            fg=self.fg_secondary,
        )
        lbl_output_title.pack(anchor="w", pady=(0, 4))

        self.txt_output = tk.Text(
            container,
            height=6,
            font=("Segoe UI", 11),
            bg=self.card_bg,
            fg=self.fg_primary,
            relief=tk.FLAT,
            padx=12,
            pady=10,
            state=tk.DISABLED,
        )
        self.txt_output.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        # Alt araç çubuğu
        bottom_bar = tk.Frame(container, bg=self.bg_color)
        bottom_bar.pack(fill=tk.X)

        self.btn_copy = tk.Button(
            bottom_bar,
            text="Metni Kopyala",
            font=("Segoe UI", 9),
            bg=self.card_bg,
            fg=self.fg_primary,
            activebackground=self.text_bg,
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.copy_output,
        )
        self.btn_copy.pack(side=tk.RIGHT)

        self.lbl_status = tk.Label(
            bottom_bar, text="", font=("Segoe UI", 9), bg=self.bg_color, fg="#10b981"
        )
        self.lbl_status.pack(side=tk.RIGHT, padx=12)

    def on_text_change(self, event=None):
        content = self.txt_input.get("1.0", tk.END).strip()
        if not content:
            self.set_output("")
            return

        result = (
            tr_to_greek(content) if self.mode == "tr_to_el" else greek_to_tr(content)
        )
        self.set_output(result)

    def set_output(self, text):
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, text)
        self.txt_output.config(state=tk.DISABLED)

    def swap_modes(self):
        current_output = self.txt_output.get("1.0", tk.END).strip()

        # Yönü ve etiketleri güncelle
        if self.mode == "tr_to_el":
            self.mode = "el_to_tr"
            self.lbl_src.config(text="Grek Alfabesi", fg=self.accent_color)
            self.lbl_dst.config(text="Türkçe", fg=self.fg_primary)
        else:
            self.mode = "tr_to_el"
            self.lbl_src.config(text="Türkçe", fg=self.fg_primary)
            self.lbl_dst.config(text="Grek Alfabesi", fg=self.accent_color)

        # Mevcut çıktıyı yeni girdi olarak aktar
        self.txt_input.delete("1.0", tk.END)
        if current_output:
            self.txt_input.insert(tk.END, current_output)
            self.on_text_change()
        else:
            self.set_output("")

    def copy_output(self):
        text = self.txt_output.get("1.0", tk.END).strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.lbl_status.config(text="Kopyalandı!")
        self.root.after(1800, lambda: self.lbl_status.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = TransliterationApp(root)
    root.mainloop()
