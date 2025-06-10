import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import winreg

steps = [
    ("install.png", "Далее"),
    ("eula.png", "Принять"),
    ("perf.png", "Далее"),
    ("ep.png", "Установить")
]

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows 12 installer")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Центровка окна
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - 700) // 2
        y = (sh - 500) // 2
        root.geometry(f"700x500+{x}+{y}")

        self.step = 0

        self.dark_theme = self.is_dark_theme()
        self.apply_theme()

        # Левая сторона — изображение
        self.canvas = tk.Canvas(root, bg=self.bg_color, highlightthickness=0)
        self.canvas.place(x=30, rely=0.5, anchor="w")

        # Заголовок
        self.title_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"),
                                    bg=self.bg_color, fg=self.fg_color, anchor="nw", justify="left")
        self.title_label.place(x=360, y=30)

        # Описание
        self.text_label = tk.Label(root, text="", font=("Segoe UI", 10),
                                   bg=self.bg_color, fg=self.fg_color, anchor="nw", justify="left", wraplength=290)
        self.text_label.place(x=360, y=70)

        # Чекбоксы
        self.check_vars = []
        self.checkboxes = []
        options = [
            "Удалить Microsoft Edge",
            "Удалить GetHelp",
            "Удалить Feedback Hub",
            "Удалить GetStarted",
            "Удалить Dev Home"
        ]

        for i, text in enumerate(options):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(root, text=text, variable=var, style="Dark.TCheckbutton")
            chk.place(x=360, y=70 + i * 30)
            chk.place_forget()
            self.check_vars.append(var)
            self.checkboxes.append(chk)

        # Кнопка действия
        self.button = ttk.Button(root, text="", command=self.next_step, style="Dark.TButton")
        self.button.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-20)

        self.tk_image = None
        self.show_image()

    def is_dark_theme(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0
        except:
            return False  # по умолчанию — светлая

    def apply_theme(self):
        if self.dark_theme:
            self.bg_color = "#1e1e1e"
            self.fg_color = "#f0f0f0"
        else:
            self.bg_color = "white"
            self.fg_color = "black"

        self.root.configure(bg=self.bg_color)

        style = ttk.Style()
        style.theme_use("default")

        if self.dark_theme:
            style.configure("Dark.TButton", foreground="white", background="#333333")
            style.map("Dark.TButton", background=[("active", "#444444")])
            style.configure("Dark.TCheckbutton", foreground="white", background=self.bg_color)
        else:
            style.configure("Dark.TButton", foreground="black", background="#f0f0f0")
            style.map("Dark.TButton", background=[("active", "#e0e0e0")])
            style.configure("Dark.TCheckbutton", foreground="black", background=self.bg_color)

    def load_image(self, filename):
        path = os.path.join("images", filename)
        if not os.path.isfile(path):
            print(f"[Ошибка] Нет файла: {path}")
            return None
        img = Image.open(path)
        img.thumbnail((300, 400), Image.Resampling.LANCZOS)
        return img

    def show_image(self):
        filename, btn_text = steps[self.step]
        image = self.load_image(filename)
        if image:
            self.tk_image = ImageTk.PhotoImage(image)
            self.root.update_idletasks()
            y = (self.root.winfo_height() - self.tk_image.height()) // 2
            self.canvas.config(width=300, height=self.root.winfo_height())
            self.canvas.delete("all")
            self.canvas.create_image(0, y, anchor="nw", image=self.tk_image)

        self.button.config(text=btn_text)
        self.update_text_and_options()

    def update_text_and_options(self):
        for chk in self.checkboxes:
            chk.place_forget()

        self.title_label.config(text="")
        self.text_label.config(text="")

        if self.step == 0:
            self.title_label.config(text="Добро пожаловать!")
            self.text_label.config(
                text="Данный инсталлятор установит фанатскую Windows 12, версии 1.0.\n\n"
                     "Рекомендуем отключить антивирус перед началом установки.\n\n"
                     "Нажмите \"Далее\" для продолжения.")
        elif self.step == 1:
            self.title_label.config(text="Лицензия")
            self.text_label.config(
                text="1. Автор не несет ответственности за любую неправильную установку и возможный ущерб системе.\n\n"
                     "2. Данный установщик и модификация не продается и является полностью бесплатным.\n\n"
                     "Вам запрещено продавать данную модификацию или выдавать за свою.")
        elif self.step == 2:
            self.title_label.config(text="Параметры производительности")
            self.text_label.config(text="Выберите, что удалить из системы при установке:")
            for i, chk in enumerate(self.checkboxes):
                chk.place(x=360, y=120 + i * 30)
        elif self.step == 3:
            self.title_label.config(text="Последний этап")
            self.text_label.config(
                text="Будут установлены настройки, которые вы выбрали в параметрах производительности,\n"
                     "а также будут применены базовые компоненты Windows 12 (fan):\n\n"
                     "• Обои\n• Функции\n• Новые параметры\n• И некоторые другие вещи.")

    def next_step(self):
        if self.step < len(steps) - 1:
            self.step += 1
            self.show_image()
        else:
            print("Установка началась (заглушка)")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()
