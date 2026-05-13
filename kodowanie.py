import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime

# --- POPRAWNA TABELA MAZOVIA (Prawdziwy standard DOS) ---
MAZOVIA_TABLE = (
    u'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
    u'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
    u' !"#$%&\'()*+,-./0123456789:;<=>?'
    u'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'
    u'`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
    u'\u0106\u0118\u0142\u0104\u00e4\u0105\u0107\u0119\u0141\u00eb\u00d3\u00f3\u015b\u015a\u00c4\u0104'
    u'\u0179\u017b\u017a\u00f4\u00f6\u0106\u00fb\u00f9\u017c\u00d6\u00dc\u00a2\u0141\u00a5\u015a\u0192'
    u'\u00e1\u00ed\u00f3\u00fa\u00f1\u00d1\u00aa\u00ba\u00bf\u2310\xac\xbd\xbc\u00a1\u00ab\u00bb'
    u'\u2591\u2592\u2593\u2502\u2524\u2561\u2562\u2556\u2555\u2563\u2551\u2557\u255d\u255c\u255b\u2510'
    u'\u2514\u2534\u252c\u251c\u2500\u253c\u255e\u255f\u255a\u2554\u2569\u2566\u2560\u2550\u256c\u2567'
    u'\u2568\u2564\u2565\u2559\u2558\u2552\u2553\u256b\u256a\u2518\u250c\u2588\u2584\u258c\u2590\u2580'
    u'\u03b1\u00df\u0393\u03c0\u03a3\u03c3\u00b5\u03c4\u03a6\u0398\u03a9\u03b4\u221e\u03c6\u03b5\u2229'
    u'\u2261\u00b1\u2265\u2264\u2320\u2321\u00f7\u2248\u00b0\u2219\u00b7\u221a\u207f\u00b2\u25a0\xa0'
)

def convert_files():
    target_encoding = encoding_var.get()
    
    input_paths = filedialog.askopenfilenames(
        title="Wybierz pliki (Mazovia)",
        filetypes=[("Pliki danych", "*.txt *.dat *.prn *.x *.xx"), ("Wszystkie pliki", "*.*")]
    )
    
    if not input_paths:
        return

    success_count = 0
    error_list = []

    for path in input_paths:
        try:
            with open(path, 'rb') as f_in:
                raw_data = f_in.read()

            # Dekodowanie Mazovia -> Unicode
            unicode_text = "".join(MAZOVIA_TABLE[b] for b in raw_data)

            input_dir = os.path.dirname(path)
            base_name = os.path.basename(path)
            name, ext = os.path.splitext(base_name)
            date_str = datetime.now().strftime("%Y-%m-%d")
            
            # Anty-nadpisywanie
            counter = 0
            while True:
                suffix = f"_{target_encoding}_{date_str}"
                if counter > 0:
                    suffix += f"_{counter}"
                output_filename = f"{name}{suffix}{ext}"
                output_path = os.path.join(input_dir, output_filename)
                if not os.path.exists(output_path):
                    break
                counter += 1

            with open(output_path, 'w', encoding=target_encoding, errors='replace') as f_out:
                f_out.write(unicode_text)
            
            success_count += 1
        except Exception as e:
            error_list.append(f"{base_name}: {str(e)}")

    if error_list:
        messagebox.showwarning("Raport", f"Zrobiono: {success_count}\nBłędy:\n" + "\n".join(error_list))
    else:
        messagebox.showinfo("Sukces", f"Przetworzono plików: {success_count}")

# --- INTERFEJS ---
root = tk.Tk()
root.title("Konwerter Mazovia by Marek v1.5")
root.geometry("480x400")

main_frame = tk.Frame(root, padx=25, pady=20)
main_frame.pack(expand=True, fill="both")

tk.Label(main_frame, text="Konwerter Standardu Mazovia", font=("Segoe UI", 14, "bold")).pack(pady=(0,15))
tk.Label(main_frame, text="Wybierz format wynikowy:", font=("Segoe UI", 10)).pack(anchor="w")

# DOMYŚLNIE: cp1250
encoding_var = tk.StringVar(value="cp1250") 

options = [
    ("Windows-1250 (Polski Windows / Excel)", "cp1250"),
    ("UTF-8 (Nowoczesny standard / Splunk)", "utf-8"),
    ("ISO-8859-2 (Systemy Linux / Unix)", "iso8859_2"),
    ("ASCII (Tylko podstawowe znaki - bez PL)", "ascii")
]

for text, value in options:
    tk.Radiobutton(
        main_frame, text=text, variable=encoding_var, value=value,
        font=("Segoe UI", 9), pady=2
    ).pack(anchor="w", padx=20)

btn_convert = tk.Button(
    main_frame, text="WYBIERZ PLIKI I KONWERTUJ", command=convert_files,
    bg="#1565C0", fg="white", font=("Segoe UI", 11, "bold"),
    padx=20, pady=12, cursor="hand2", relief="flat"
)
btn_convert.pack(pady=30)

tk.Label(main_frame, text="Zabezpieczenie: pliki nie są nadpisywane.", font=("Segoe UI", 8), fg="gray").pack()

root.mainloop()