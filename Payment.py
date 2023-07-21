import tkinter as tk
import tkinter.ttk as ttk
import requests
import json

def get_all_orders():
    try:
        response = requests.get("http://127.0.0.1:8001/orders/")
        response.raise_for_status()
        orders_data = response.json()
        return orders_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders from the API: {e}")
        return []

class PaymentWindow(tk.Toplevel):
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
        self.order_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Reduce the width of each column
        self.order_tree.column("#0", width=40)
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
        
        self.populate_order_tree()

        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm_payment)
        self.confirm_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_payment)
        self.cancel_button.pack(side=tk.LEFT, padx=10, pady=5)

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

    def confirm_payment(self):
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item, "text")
            response = requests.post(f"http://127.0.0.1:8002/payments/confirm/{order_id}")
            if response.status_code == 200:
                tk.messagebox.showinfo("Payment Confirmation", "Payment confirmed successfully!")
                self.populate_order_tree()
            else:
                tk.messagebox.showerror("Payment Confirmation Error", "Failed to confirm payment.")

    def cancel_payment(self):
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item, "text")
            response = requests.post(f"http://127.0.0.1:8002/payments/cancel/{order_id}")
            if response.status_code == 200:
                tk.messagebox.showinfo("Payment Cancellation", "Payment cancelled successfully!")
                self.populate_order_tree()
            else:
                tk.messagebox.showerror("Payment Cancellation Error", "Failed to cancel payment.")

if __name__ == "__main__":
    root = tk.Tk()
    payment_window = PaymentWindow(root)
    root.mainloop()
