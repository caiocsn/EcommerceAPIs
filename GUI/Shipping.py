import os
import tkinter as tk
import tkinter.ttk as ttk
import requests
import json
from .utils import *

class ShippingWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Payment Window")
        self.geometry("900x400")
        self.transient(master)

        # Create a treeview to display orders
        self.order_tree = ttk.Treeview(self)
        self.order_tree["columns"] = ("Customer Name", "Email", "CEP", "Phone Number", "Items", "Status")
        self.order_tree.heading("#0", text="ID",)
        self.order_tree.heading("Customer Name", text="Customer Name")
        self.order_tree.heading("Email", text="Email")
        self.order_tree.heading("CEP", text="CEP")
        self.order_tree.heading("Phone Number", text="Phone Number")
        self.order_tree.heading("Items", text="Items")
        self.order_tree.heading("Status", text="Staus")
        self.order_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Reduce the width of each column
        self.order_tree.column("#0", width=40)  # Order ID column
        self.order_tree.column("Customer Name", width=80)
        self.order_tree.column("Email", width=120)
        self.order_tree.column("CEP", width=80)
        self.order_tree.column("Phone Number", width=100)
        self.order_tree.column("Items", width=80)
        self.order_tree.column("Status", width=60)

        # Create a scrollbar for the treeview
        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.order_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.populate_order_tree()

        tk.Button(self, text="Processing", command=self.set_processing).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self, text="Sent", command=self.set_sent).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self, text="Delivered", command=self.set_delivered).pack(side=tk.LEFT, padx=10, pady=5)

    def populate_order_tree(self):
        try:
            orders_data = get_all_orders()

            self.order_tree.delete(*self.order_tree.get_children())

            for order in orders_data:
                self.order_tree.insert("", "end", text=str(order["id"]),
                                       values=(order["customer_name"], order["email"],
                                               order["cep"], order["phone_number"],
                                               json.dumps(order["items"]),
                                                order["status"]))
        except Exception as e:
            print(f"Error populating order tree: {e}")

    def set_processing(self):
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item, "text")
            response = requests.post(os.environ.get('SHIPPING_API_URL') + f"processing/{order_id}")
            if response.status_code == 200:
                tk.messagebox.showinfo("Order status changed to processing", "Status changed successfully!")
                self.populate_order_tree()
            else:
                tk.messagebox.showerror("Status changing error", "Failed to change order status.")

    def set_sent(self):
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item, "text")
            response = requests.post(os.environ.get('SHIPPING_API_URL') + f"sent/{order_id}")
            if response.status_code == 200:
                tk.messagebox.showinfo("Order status changed to sent", "Status changed successfully!")
                self.populate_order_tree()
            else:
                tk.messagebox.showerror("Status changing error", "Failed to change order status.")

    def set_delivered(self):
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item, "text")
            response = requests.post(os.environ.get('SHIPPING_API_URL') + f"delivered/{order_id}")
            if response.status_code == 200:
                tk.messagebox.showinfo("Order status changed to delivered", "Status changed successfully!")
                self.populate_order_tree()
            else:
                tk.messagebox.showerror("Status changing error", "Failed to change order status.")

if __name__ == "__main__":
    root = tk.Tk()
    shipping_window = ShippingWindow(root)
    root.mainloop()
