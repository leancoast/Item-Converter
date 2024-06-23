import re
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

def convert_format(input_str, pattern):
    matches = pattern.finditer(input_str)
    output = []

    for match in matches:
        key = match.group('key')
        label = match.group('label')
        weight = match.group('weight')
        description = match.group('description')
        image = match.group('image')

        converted = f"""
        ["{key}"] = {{
            label = "{label}",
            weight = {weight},
            stack = false,
            close = true,
            description = "{description}",
            client = {{
                image = "{image}",
            }}
        }},
        """
        output.append(converted.strip())

    return "\n".join(output)

def process_input():
    input_str = text_area.get("1.0", tk.END)
    selected_format = format_var.get()
    
    if selected_format == "Silah":
        pattern = pattern_weapon
    elif selected_format == "Eşya":
        pattern = pattern_item
    else:
        messagebox.showerror("Error", "Geçerli olmayan bir format seçildi.")
        return
    
    converted_str = convert_format(input_str, pattern)
    save_output(converted_str)

def save_output(output_str):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_str)
        status_label.config(text=f"Buraya kaydedildi: {file_path}")

# Farklı formatların tanımları
pattern_weapon = re.compile(
    r"(?P<key>\w+)\s*=\s*\{\s*name\s*=\s*'(?P<name>[^']+)',\s*label\s*=\s*'(?P<label>[^']+)',\s*weight\s*=\s*(?P<weight>\d+),\s*type\s*=\s*'(?P<type>[^']+)',\s*ammotype\s*=\s*(?P<ammotype>\w+),\s*image\s*=\s*'(?P<image>[^']+)',\s*unique\s*=\s*(?P<unique>\w+),\s*useable\s*=\s*(?P<useable>\w+),\s*description\s*=\s*'(?P<description>[^']+)'"
)

pattern_item = re.compile(
    r"(?P<key>\w+)\s*=\s*\{\s*name\s*=\s*'(?P<name>[^']+)',\s*label\s*=\s*'(?P<label>[^']+)',\s*weight\s*=\s*(?P<weight>\d+),\s*type\s*=\s*'(?P<type>[^']+)',\s*image\s*=\s*'(?P<image>[^']+)',\s*unique\s*=\s*(?P<unique>\w+),\s*useable\s*=\s*(?P<useable>\w+),\s*shouldClose\s*=\s*(?P<shouldClose>\w+),\s*description\s*=\s*'(?P<description>[^']+)'"
)

# GUI oluşturma
root = tk.Tk()
root.title("Eşya Dönüştürücü")
root.geometry("600x500")

# Girdi alanı
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
text_area.pack(padx=10, pady=10)

# Format seçim menüsü
format_var = tk.StringVar(value="Silah")
format_label = tk.Label(root, text="Seçili Format:")
format_label.pack(pady=5)
format_menu = tk.OptionMenu(root, format_var, "Silah", "Eşya")
format_menu.pack(pady=5)

# İşlem butonu
process_button = tk.Button(root, text="Dönüştür ve Kaydet", command=process_input, bg="green", fg="white")
process_button.pack(pady=10)

# Durum etiketi
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# GUI başlatma
root.mainloop()
