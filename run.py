import tkinter as tk
from Orders import CreateOrderWindow

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Interface")
        self.geometry("300x100")
        
        self.create_user_window = None

        self.create_user_button = tk.Button(self, text="Orders", command=self.open_create_user_window)
        self.create_user_button.pack(pady=20)

    def open_create_user_window(self):
        if not self.create_user_window:
            self.create_user_window = CreateOrderWindow(self)
            self.create_user_window.protocol("WM_DELETE_WINDOW", self.on_create_user_close)
        else:
            self.create_user_window.deiconify()

    def on_create_user_close(self):
        self.create_user_window.destroy()
        self.create_user_window = None

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
