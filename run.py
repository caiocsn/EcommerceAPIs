import tkinter as tk
from Orders import OrderWindow
from Payment import PaymentWindow

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Interface")
        self.geometry("200x200")
        
        self.orders_window = None
        self.payment_window = None

        self.orders_button = tk.Button(self, text="Orders", command= lambda: self.open_window(self.orders_window, OrderWindow))
        self.orders_button.pack(pady=5)
        self.payment_button = tk.Button(self, text="Payment", command= lambda: self.open_window(self.payment_window, PaymentWindow))
        self.payment_button.pack(pady=5)

    def open_window(self, window, creator):
        if not window:
            window = creator(self)
            window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(window))
        else:
            window.deiconify()

    def on_window_close(self, window):
        window.destroy()
        window = None

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
    
