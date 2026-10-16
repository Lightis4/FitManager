
import tkinter as tk
from tkinter import messagebox

from interface import FitManagerApp


def main():
    root = tk.Tk()

    try:
        FitManagerApp(root)
    except Exception as erro:
        messagebox.showerror(
            "Erro ao iniciar o FitManager",
            str(erro),
            parent=root
        )
        root.destroy()
        return

    root.mainloop()


if __name__ == "__main__":
    main()
