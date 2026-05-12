import tkinter as tk
from tkinter import ttk

# Импортируй свои функции (замени имя файла при необходимости)
from Decrypt import break_caesar_auto
from Incrypt import caesar_encrypt, caesar_reverse_encrypt

from Utils import text_analyze, separated


class CaesarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Цезаря")
        self.root.geometry("600x400")  # ширина x высота
        self.root.minsize(600, 400)

        self.main_frame()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_frame(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="Выберите действие:").pack(pady=10)

        ttk.Button(frame, text="Зашифровать", command=self.encrypt_frame).pack(pady=5)
        ttk.Button(frame, text="Расшифровать", command=self.encrypt_reverse_frame).pack(pady=5)
        ttk.Button(frame, text="Возломать", command=self.decrypt_frame).pack(pady=5)
# Encrypt
    def encrypt_frame(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="Введите текст:").pack()
        input_text = tk.Text(frame, height=5, width=40)
        input_text.pack()

        ttk.Label(frame, text="Сдвиг:").pack()
        shift_entry = ttk.Entry(frame)
        shift_entry.pack()

        output = tk.Text(frame, height=5, width=40)
        output.pack(pady=10)
        output.config(state='disabled')

        def encrypt_action():
            text = input_text.get("1.0", tk.END).strip()
            if input_text=="":
                output.config(state='normal')
                output.delete("1.0", tk.END)
                output.insert(tk.END, "Ошибка: Ключ должен быть целым числом")
                output.config(state='disabled')
                return
            try:
                shift = int(shift_entry.get())
            except:
                output.config(state='normal')
                output.delete("1.0", tk.END)
                output.insert(tk.END, "Ошибка: Ключ должен быть целым числом")
                output.config(state='disabled')
                return
            is_valid, message = text_analyze(text)
            if not is_valid:
                output.config(state='normal')
                output.delete("1.0", tk.END)
                output.insert(tk.END, message)
                output.config(state='disabled')
                return
            result = caesar_encrypt(text, shift)
            print(result)
            result = separated(result)
            print(result)
            output.config(state='normal')
            output.delete("1.0", tk.END)
            output.insert(tk.END, result)
            output.config(state='disabled')

        ttk.Button(frame, text="Зашифровать", command=encrypt_action).pack(pady=5)
        ttk.Button(frame, text="Назад", command=self.main_frame).pack()
# Encrypt_reverse
    def encrypt_reverse_frame(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="Введите текст:").pack()
        input_text = tk.Text(frame, height=5, width=40)
        input_text.pack()

        ttk.Label(frame, text="Сдвиг:").pack()
        shift_entry = ttk.Entry(frame)
        shift_entry.pack()

        output = tk.Text(frame, height=5, width=40)
        output.pack(pady=10)
        output.config(state='disabled')

        def encrypt_action():
            text = input_text.get("1.0", tk.END).strip()
            try:
                shift = int(shift_entry.get())
            except:
                output.config(state='normal')
                output.delete("1.0", tk.END)
                output.insert(tk.END, "Ошибка: поле сдвига не может быть пустым")
                output.config(state='disabled')
                return
            is_valid, message = text_analyze(text)
            if not is_valid:
                output.config(state='normal')
                output.delete("1.0", tk.END)
                output.insert(tk.END, message)
                output.config(state='disabled')
                return
            result = caesar_reverse_encrypt(text, shift)
            result = separated(result)
            output.config(state='normal')
            output.delete("1.0", tk.END)
            output.insert(tk.END, result)
            output.config(state='disabled')

        ttk.Button(frame, text="Расшифровать", command=encrypt_action).pack(pady=5)
        ttk.Button(frame, text="Назад", command=self.main_frame).pack()

# Decrypt
    def decrypt_frame(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="Введите текст:").pack()
        input_text = tk.Text(frame, height=5, width=40)
        input_text.pack()

        output = tk.Text(frame, height=5, width=40)
        output.pack(pady=10)

        def decrypt_action():
            text = input_text.get("1.0", tk.END).strip()

            is_valid, message = text_analyze(text)

            if not is_valid:
                output.delete("1.0", tk.END)
                output.insert(tk.END, message)
                return

            result = break_caesar_auto(text)

            formatted_text = separated(result['text'])

            languages = ", ".join(result['languages_detected'])

            output.delete("1.0", tk.END)

            output.insert(
                tk.END,
                f"Языки: {languages}\n"
                f"Сдвиг: {result['shift']}\n"
                f"Текст: {formatted_text}"
            )

        ttk.Button(frame, text="Взломать", command=decrypt_action).pack(pady=5)
        ttk.Button(frame, text="Назад", command=self.main_frame).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarApp(root)
    root.mainloop()