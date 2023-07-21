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

class OrderForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.customer_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cep_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.items_var = tk.StringVar()

        self.cep_var.trace_add('write', self.format_cep)
        self.phone_var.trace_add('write', self.format_phone_number)

        self.create_widgets()
    
    def create_widgets(self):
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

    def format_cep(self, *args):
        cep = self.cep_var.get()
        cep = re.sub(r'[^0-9]', '', cep)[:8]
        self.cep_var.set(cep)

    def format_phone_number(self, *args):
        phone_number = self.phone_var.get()
        phone_number = re.sub(r'[^0-9]', '', phone_number)[:11]
        self.phone_var.set(phone_number)

class AddOrdermWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Create Order")
        self.geometry("300x400")
        self.transient(master)

        self.order_form = OrderForm(self)
        self.order_form.pack(padx=10, pady=10)

        self.add_button = tk.Button(self, text="Create Order", command=self.create_order)
        self.add_button.pack(pady=10)


    def create_order(self):
        try:            
            order_data = OrderWrite(
                customer_name=self.order_form.customer_name_var.get(),
                email=self.order_form.email_var.get(),
                cep=self.order_form.cep_var.get(),
                phone_number=self.order_form.phone_var.get(),
                items=json.loads(self.order_form.items_var.get()),
            )            

            response = requests.post("http://127.0.0.1:8001/orders/", json=order_data.dict())
            response.raise_for_status()  # Raise an exception for non-2xx responses

            # Display success message
            messagebox.showinfo("Success", "Order created successfully!")
        
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
            self.master.populate_order_tree()
    

class OrderWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Orders")
        self.geometry("900x400")
        self.transient(master)

        self.master = master

        self.item_list = get_all_items()

        self.add_order_window = None

        # Create a treeview to display orders
        self.order_tree = ttk.Treeview(self)
        self.order_tree["columns"] = ("Customer Name", "Email", "CEP", "Phone Number", "Items", "Total", "Status")
        self.order_tree.heading("#0", text="ID",)
        self.order_tree.heading("Customer Name", text="Customer Name")
        self.order_tree.heading("Email", text="Email")
        self.order_tree.heading("CEP", text="CEP")
        self.order_tree.heading("Phone Number", text="Phone Number")
        self.order_tree.heading("Items", text="Items")
        self.order_tree.heading("Total", text="Total")
        self.order_tree.heading("Status", text="Staus")
        self.order_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Reduce the width of each column
        self.order_tree.column("#0", width=40)  # Order ID column
        self.order_tree.column("Customer Name", width=80)
        self.order_tree.column("Email", width=120)
        self.order_tree.column("CEP", width=80)
        self.order_tree.column("Phone Number", width=100)
        self.order_tree.column("Items", width=60)
        self.order_tree.column("Total", width=40)
        self.order_tree.column("Status", width=40)

        # Create a scrollbar for the treeview
        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button = tk.Button(self, text="Create Order", command=self.open_add_order_window)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.add_random_order_button = tk.Button(self, text="Create Random Order", command= self.create_random_order)
        self.add_random_order_button.pack(side=tk.LEFT, padx=10, pady=5)

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
                                               order["total"],
                                                order["status"]))

        except Exception as e:
            print(f"Error populating order tree: {e}")

    def open_add_order_window(self):        
        if not self.add_order_window:
            self.add_order_window = AddOrdermWindow(self)
            self.add_order_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(self.add_order_window))
    
    def on_window_close(self, window):
        if window is self.add_order_window:
            self.add_order_window.destroy()
            self.add_order_window = None

    def create_random_order(self):
        try:
            names = ["Ana", "Pedro", "Beatriz", "Lucas", "Carla", "Gabriel", "Mariana", "Bruno", "Isabela", "Rafael"]
            surnames = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida", "Pereira", "Gomes", "Ribeiro"]
            random_name = random.choice(names)
            random_surname = random.choice(surnames)
            
            random_cep = "".join(random.choices("0123456789", k=8))
            random_phone_number = "".join(random.choices("0123456789", k=11))
            
            item_ids = [item["id"] for item in self.item_list]            
            selected_ids = random.choices(item_ids, k = random.randint(1, 5))
            selected_ids = set(selected_ids)
            random_items = {id: random.randint(1, 10) for id in selected_ids}

            order_data = OrderWrite(
                customer_name= random_name + " " + random_surname,
                email="random@random.rd",
                cep=random_cep,
                phone_number=random_phone_number,
                items=random_items,
            )
            response = requests.post("http://127.0.0.1:8001/orders/", json=order_data.dict())
            response.raise_for_status()  # Raise an exception for non-2xx responses

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
    OrderWindow(root)
    root.mainloop()