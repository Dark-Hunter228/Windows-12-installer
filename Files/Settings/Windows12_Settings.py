import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Убедись, что установлен pillow: pip install pillow

class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows 12 Settings")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        self.root.resizable(True, True)

        self.setup_ui()
        self.load_image()

    def setup_ui(self):
        # "Тема"
        theme_label = tk.Label(self.root, text="Тема", bg="white", font=("Segoe UI", 10))
        theme_label.place(x=20, y=20)

        self.theme_var = tk.StringVar(value="Windows 12 Light")
        theme_menu = ttk.Combobox(self.root, textvariable=self.theme_var, state="readonly")
        theme_menu["values"] = ("Windows 12 Light", "Windows 12 Dark")
        theme_menu.place(x=20, y=50)

        # "Панель задач"
        taskbar_label = tk.Label(self.root, text="Панель задач", bg="white", font=("Segoe UI", 10))
        taskbar_label.place(x=20, y=100)

        self.taskbar_size = tk.StringVar(value="medium")

        tk.Radiobutton(self.root, text="Большой размер", variable=self.taskbar_size,
                       value="big", bg="white").place(x=20, y=130)

        tk.Radiobutton(self.root, text="Средний размер (По умолчанию)", variable=self.taskbar_size,
                       value="medium", bg="white").place(x=20, y=160)

        tk.Radiobutton(self.root, text="Маленький размер", variable=self.taskbar_size,
                       value="small", bg="white").place(x=20, y=190)

        # "Windows Defender"
        defender_label = tk.Label(self.root, text="Windows Defender", bg="white", font=("Segoe UI", 10))
        defender_label.place(x=20, y=240)

        self.defender_enabled = True
        self.defender_button = tk.Button(self.root, text="Выключить Defender", command=self.toggle_defender)
        self.defender_button.place(x=20, y=270)

    def toggle_defender(self):
        self.defender_enabled = not self.defender_enabled
        self.defender_button.config(
            text="Выключить Defender" if self.defender_enabled else "Включить Defender"
        )

    def load_image(self):
        try:
            image = Image.open("dpi.png")
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.root, image=self.photo, bg="white")
            label.place(x=780, y=20)  # Сместили в верхний правый угол
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()
