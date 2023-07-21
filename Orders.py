import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import re
import requests
import json
import random

from models.models import OrderWrite

def get_all_items():
    try:
        response = requests.get("http://127.0.0.1:8000/items/")
        response.raise_for_status()
        items_data = response.json()
        return items_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching items from the API: {e}")
        return []

def get_all_orders():
    try:
        response = requests.get("http://127.0.0.1:8001/orders/")
        response.raise_for_status()
        orders_data = response.json()
        return orders_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders from the API: {e}")
        return []
    
class CreateOrderWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Create Order")
        self.geometry("900x400")
        self.transient(master)

        self.master = master

        self.item_list = get_all_items()

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

        # Create a frame for the form elements
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.customer_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cep_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.items_var = tk.StringVar()

        self.cep_var.trace_add('write', self.format_cep)
        self.phone_var.trace_add('write', self.format_phone_number)

        tk.Label(self, text="Customer Name:").pack()
        tk.Entry(self, textvariable=self.customer_name_var).pack()

        tk.Label(self, text="Email:").pack()
        tk.Entry(self, textvariable=self.email_var).pack()

        tk.Label(self, text="CEP (Brazilian, 8 digits):").pack()
        tk.Entry(self, textvariable=self.cep_var).pack()

        tk.Label(self, text="Phone Number (Brazilian, 11 digits):").pack()
        tk.Entry(self, textvariable=self.phone_var).pack()

        tk.Label(self, text="Items (JSON format):").pack()
        tk.Entry(self, textvariable=self.items_var).pack()

        tk.Button(self, text="Create Order", command=self.create_order).pack(pady=10)
        tk.Button(self, text="Create Random Order", command= lambda: self.create_order("random")).pack(pady=10)

        # Bind a function to handle treeview selection
        self.order_tree.bind("<ButtonRelease-1>", self.populate_form_from_tree)

        # Populate the treeview with all orders
        self.populate_order_tree()

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

    def populate_form_from_tree(self, event):
        # Get the selected item from the treeview
        selected_item = self.order_tree.selection()
        if selected_item:
            # Get the values of the selected item
            values = self.order_tree.item(selected_item, "values")

            # Populate the form fields with the selected item's values
            self.customer_name_var.set(values[0])
            self.email_var.set(values[1])
            self.cep_var.set(values[2])
            self.phone_var.set(values[3])
            self.items_var.set(values[4])

    def format_cep(self, *args):
        cep = self.cep_var.get()
        cep = re.sub(r'[^0-9]', '', cep)[:8]
        self.cep_var.set(cep)

    def format_phone_number(self, *args):
        phone_number = self.phone_var.get()
        phone_number = re.sub(r'[^0-9]', '', phone_number)[:11]
        self.phone_var.set(phone_number)

    def create_order(self, mode="default"):
        try:
            if mode == "default":
                order_data = OrderWrite(
                    customer_name=self.customer_name_var.get(),
                    email=self.email_var.get(),
                    cep=self.cep_var.get(),
                    phone_number=self.phone_var.get(),
                    items=json.loads(self.items_var.get()),
                )
            elif mode == "random":
                random_name = random.choice(['Joao', 'Maria', 'Arthur', 'Pedro', 'Joana', 'Rebeca'])
                random_surname = random.choice(['Santos', 'Silva', 'Rocha', 'Aguiar'])
                random_cep = "".join(random.choices("0123456789", k=8))
                random_phone_number = "".join(random.choices("0123456789", k=11))
                item_choice = random.choice(self.item_list)
                random_item = {item_choice["id"]: 1}

                order_data = OrderWrite(
                    customer_name= random_name + " " + random_surname,
                    email="random@random.rd",
                    cep=random_cep,
                    phone_number=random_phone_number,
                    items=random_item,
                )

            response = requests.post("http://127.0.0.1:8001/orders/", json=order_data.dict())
            response.raise_for_status()  # Raise an exception for non-2xx responses

            # Display success message
            messagebox.showinfo("Success", "Order created successfully!")
            # Reset the form
            self.customer_name_var.set('')
            self.email_var.set('')
            self.cep_var.set('')
            self.phone_var.set('')
            self.items_var.set('')

        except requests.exceptions.RequestException as e:
            # Display error message
            messagebox.showerror("Error", f"Error creating order: {e}")

        except json.JSONDecodeError as e:
            # Display error message if the JSON parsing fails
            messagebox.showerror("Error", f"Error parsing JSON: {e}")

        except Exception as e:
            # Display generic error message
            messagebox.showerror("Error", f"Error: {e}")
        
        finally:
            # Refresh list
            self.populate_order_tree()

if __name__ == "__main__":
    root = tk.Tk()
    CreateOrderWindow(root)
    root.mainloop()