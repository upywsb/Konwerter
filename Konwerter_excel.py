import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from io import StringIO
import re

class Kodowanie:
    MAZOVIA_TO_UTF8 = {
        0x8f: 'Ą', 0x95: 'Ć', 0x90: 'Ę', 0x92: 'Ł', 0xa4: 'Ń', 0xa5: 'Ó', 0x8e: 'Ś', 0x98: 'Ź', 0x9b: 'Ż',
        0x86: 'ą', 0x8d: 'ć', 0x91: 'ę', 0x93: 'ł', 0xa2: 'ń', 0xa3: 'ó', 0x9c: 'ś', 0xa0: 'ź', 0xa1: 'ż'
    }

    @staticmethod
    def konwertuj(data, from_enc):
        if from_enc == "Mazovia":
            return "".join(Kodowanie.MAZOVIA_TO_UTF8.get(b, chr(b) if 32 <= b <= 126 or b in [10, 13] else "") for b in data)
        return data.decode(from_enc, errors='ignore')

class KonwerterMBS:
    def __init__(self, root):
        self.root = root
        self.root.title("MBS Konwerter to Excel v3.7 by Marek")
        self.root.geometry("1300x900")
        
        self.all_lines_view = []
        self.podzialy = []
        self.char_width = 0
        
        # --- UI: 1. Import ---
        self.top_frame = tk.LabelFrame(root, text=" 1. Import i Kodowanie ", padx=10, pady=5)
        self.top_frame.pack(fill="x", padx=20, pady=5)
        
        self.combo_enc = ttk.Combobox(self.top_frame, values=["Mazovia", "cp1250", "utf-8"], width=10)
        self.combo_enc.set("Mazovia")
        self.combo_enc.pack(side=tk.LEFT, padx=5)

        tk.Button(self.top_frame, text="Wczytaj Plik", command=self.wczytaj_plik, bg="#1976d2", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)

        # --- UI: Podgląd ---
        self.preview_frame = tk.Frame(root)
        self.preview_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.canvas = tk.Canvas(self.preview_frame, bg="white", cursor="cross", relief="sunken", bd=2)
        self.vbar = tk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.hbar = tk.Scrollbar(self.preview_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.vbar.pack(side=tk.RIGHT, fill="y")
        self.hbar.pack(side=tk.BOTTOM, fill="x")
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.dodaj_linie)

        # --- UI: 2. Parametry ---
        self.settings_frame = tk.LabelFrame(root, text=" 2. Parametry Eksportu ", padx=10, pady=10)
        self.settings_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.settings_frame, text="Miejsc po przecinku:").grid(row=0, column=0, sticky="w")
        self.entry_prec = tk.Entry(self.settings_frame, width=5)
        self.entry_prec.grid(row=0, column=1, sticky="w", padx=5)
        self.entry_prec.insert(0, "2")

        tk.Label(self.settings_frame, text="Dodatkowe znaki do usunięcia:").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.entry_chars = tk.Entry(self.settings_frame, width=15)
        self.entry_chars.grid(row=0, column=3, sticky="w")
        
        tk.Label(self.settings_frame, text="(Spacje w liczbach są usuwane automatycznie)", fg="blue", font=("Arial", 8)).grid(row=1, column=0, columnspan=4, sticky="w", pady=(5,0))

        # --- UI: Akcje ---
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)
        tk.Button(self.btn_frame, text="Resetuj linie", command=self.resetuj_linie).pack(side=tk.LEFT, padx=10)
        tk.Button(self.btn_frame, text="GENERUJ EXCEL", command=self.generuj_excel, bg="#2e7d32", fg="white", font=("Arial", 11, "bold"), padx=40).pack(side=tk.LEFT, padx=10)

        self.label_status = tk.Label(root, text="Gotowy", fg="blue")
        self.label_status.pack()

    def wczytaj_plik(self):
        path = filedialog.askopenfilename()
        if not path: return
        try:
            with open(path, 'rb') as f:
                raw_data = f.read()
            content = Kodowanie.konwertuj(raw_data, self.combo_enc.get())
            self.all_lines_view = content.splitlines()
            self.canvas.delete("all")
            txt_id = self.canvas.create_text(10, 10, anchor="nw", text="\n".join(self.all_lines_view), font=("Courier", 11))
            bbox = self.canvas.bbox(txt_id)
            self.canvas.config(scrollregion=(0, 0, bbox[2] + 200, bbox[3] + 50))
            test_id = self.canvas.create_text(0, -100, text="X" * 100, font=("Courier", 11))
            self.char_width = (self.canvas.bbox(test_id)[2] - self.canvas.bbox(test_id)[0]) / 100
            self.canvas.delete(test_id)
            self.podzialy = []
            self.label_status.config(text=f"Wczytano {len(self.all_lines_view)} linii.", fg="green")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def dodaj_linie(self, event):
        x_canvas = self.canvas.canvasx(event.x)
        sr = self.canvas.cget("scrollregion").split()
        height = float(sr[3]) if sr else 2000
        self.canvas.create_line(x_canvas, 0, x_canvas, height, fill="red", width=1, dash=(4, 4), tags="split_line")
        idx = round((x_canvas - 10) / self.char_width)
        if idx not in self.podzialy:
            self.podzialy.append(idx); self.podzialy.sort()

    def resetuj_linie(self):
        self.canvas.delete("split_line")
        self.podzialy = []

    def clean_for_xml(self, text):
        if not isinstance(text, str): return text
        return "".join(ch for ch in text if ord(ch) >= 32 or ch in "\n\r\t")

    def czy_linia_ozdobna(self, line):
        clean = line.strip()
        if not clean: return False
        if re.match(r'^([\-\=\*\_\. \xA0])\1{2,}$', clean): return True
        return False

    def generuj_excel(self):
        if not self.podzialy: return
        indices = [0] + self.podzialy + [1000]
        specs = [(indices[i], indices[i+1]) for i in range(len(indices)-1)]
        prec = self.entry_prec.get()
        p_val = int(prec) if prec.isdigit() else 2
        user_chars = self.entry_chars.get()
        
        try:
            filtered_content = [l for l in self.all_lines_view if not self.czy_linia_ozdobna(l)]
            df = pd.read_fwf(StringIO("\n".join(filtered_content)), colspecs=specs, header=None, dtype=str)
            
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if not save_path: return

            writer = pd.ExcelWriter(save_path, engine='xlsxwriter', engine_kwargs={'options': {'strings_to_urls': False}})
            df.to_excel(writer, index=False, header=False, sheet_name='Dane')
            
            workbook = writer.book
            worksheet = writer.sheets['Dane']
            num_format = workbook.add_format({'num_format': f'#,##0.{"0"*p_val}'})

            for r_idx, row in df.iterrows():
                for c_idx, val in enumerate(row):
                    if pd.isna(val): continue
                    
                    # 1. Czyszczenie XML i znaków użytkownika
                    raw_str = self.clean_for_xml(str(val).strip())
                    for char in user_chars:
                        raw_str = raw_str.replace(char, "")
                    
                    # 2. Inteligentne usuwanie spacji TYLKO z liczb
                    # Tworzymy wersję "ultra-czystą" (bez żadnych spacji/tabulatorów)
                    clean_for_test = re.sub(r'\s+', '', raw_str).replace("\xa0", "").replace(",", ".")
                    
                    # Sprawdzamy czy to co zostało to liczba ORAZ czy w oryginale był separator (kropka/przecinek)
                    has_decimal = ('.' in raw_str or ',' in raw_str)
                    
                    try:
                        # Jeśli po usunięciu spacji to czysta liczba (np. 4000.00) i miała kropkę/przecinek
                        if re.match(r'^-?\d+(\.\d+)?$', clean_for_test) and has_decimal:
                            worksheet.write_number(r_idx, c_idx, float(clean_for_test), num_format)
                        else:
                            # Jeśli to np. 12/22 albo tekst, zostawiamy ze spacjami (trimowane na początku)
                            worksheet.write_string(r_idx, c_idx, raw_str)
                    except:
                        worksheet.write_string(r_idx, c_idx, raw_str)

            writer.close()
            messagebox.showinfo("Sukces", "Eksport zakończony.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

if __name__ == "__main__":
    root = tk.Tk(); app = KonwerterMBS(root); root.mainloop()
