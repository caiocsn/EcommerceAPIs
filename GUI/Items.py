import random
import tkinter as tk
from tkinter import ttk, messagebox
import requests

def get_all_items():
    try:
        response = requests.get("http://127.0.0.1:8000/items/")
        response.raise_for_status()
        items_data = response.json()
        return items_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching items from the API: {e}")
        return []
    

class ItemForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.id_var = tk.IntVar()
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.price_var = tk.DoubleVar()
        self.quantity_var = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="ID:").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.id_var).grid(row=0, column=1)

        tk.Label(self, text="Name:").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.name_var).grid(row=1, column=1)

        tk.Label(self, text="Description:").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.description_var).grid(row=2, column=1)

        tk.Label(self, text="Price:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.price_var).grid(row=3, column=1)

        tk.Label(self, text="Quantity:").grid(row=4, column=0)
        tk.Entry(self, textvariable=self.quantity_var).grid(row=4, column=1)

class AddItemWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Item")
        self.geometry("300x200")
        self.transient(master)

        self.item_form = ItemForm(self)
        self.item_form.pack(padx=10, pady=10)

        self.add_button = tk.Button(self, text="Add item", command=self.add_item)
        self.add_button.pack(pady=10)

    def add_item(self):
        item_data = {
            "id": self.item_form.id_var.get(),
            "name": self.item_form.name_var.get(),
            "description": self.item_form.description_var.get(),
            "price": self.item_form.price_var.get(),
            "quantity": self.item_form.quantity_var.get(),
        }

        try:
            response = requests.post("http://127.0.0.1:8000/items/", json=item_data)
            response.raise_for_status()

            # Display success message
            messagebox.showinfo("Success", "Item created successfully!")
             # Refresh the item treeview in the main window to display the updated item
            self.master.load_items()     

        except requests.exceptions.RequestException as e:
            # Display error message
            messagebox.showerror("Error", f"Error adding item: {e}")

class EditItemWindow(tk.Toplevel):
    def __init__(self, master, item_data):
        super().__init__(master)
        self.title("Edit Item")
        self.geometry("300x200")
        self.transient(master)

        self.item_form = ItemForm(self)
        self.item_form.pack(padx=10, pady=10)

        # Set default values in the form based on the item_data
        self.item_form.id_var.set(item_data["id"])
        self.item_form.name_var.set(item_data["name"])
        self.item_form.description_var.set(item_data["description"])
        self.item_form.price_var.set(item_data["price"])
        self.item_form.quantity_var.set(item_data["quantity"])

        self.edit_button = tk.Button(self, text="Edit", command=self.edit_item)
        self.edit_button.pack(pady=10)

    def edit_item(self):
        item_data = {
            "id": self.item_form.id_var.get(),
            "name": self.item_form.name_var.get(),
            "description": self.item_form.description_var.get(),
            "price": self.item_form.price_var.get(),
            "quantity": self.item_form.quantity_var.get(),
        }

        try:
            response = requests.put(f"http://127.0.0.1:8000/items/{item_data['id']}", json=item_data)
            response.raise_for_status()

            # Display success message
            messagebox.showinfo("Success", "Item edited successfully!")
            # Refresh the item treeview in the main window to display the updated item
            self.master.load_items()  

        except requests.exceptions.RequestException as e:
            # Display error message
            messagebox.showerror("Error", f"Error editing item: {e}")

class ItemWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Items")
        self.geometry("900x400")
        self.transient(master)

        self.add_item_window = None
        self.edit_item_window = None

        self.item_tree = ttk.Treeview(self, columns=("ID", "Name", "Description", "Price", "Quantity"), show="headings")
        self.item_tree.heading("ID", text="ID")
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Description", text="Description")
        self.item_tree.heading("Price", text="Price")
        self.item_tree.heading("Quantity", text="Quantity")
        self.item_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.item_tree.column("ID", width=50)
        self.item_tree.column("Name", width=100)
        self.item_tree.column("Description", width=150)
        self.item_tree.column("Price", width=50)
        self.item_tree.column("Quantity", width=50)

        # Create a scrollbar for the treeview
        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button = tk.Button(self, text="Add Item", command=self.open_add_item_window)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.edit_button = tk.Button(self, text="Edit Item", command=self.open_edit_item_window)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.delete_button = tk.Button(self, text="Delete Item", command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.add_random_button = tk.Button(self, text="Add random Item", command=self.add_random_item)
        self.add_random_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.load_items()

    def load_items(self):
        try:
            items_data = get_all_items()
            self.item_tree.delete(*self.item_tree.get_children())
            for item in items_data:
                self.item_tree.insert("", "end", values=(item["id"], item["name"], item["description"],
                                                        item["price"], item["quantity"]))

        except requests.exceptions.RequestException as e:
            print(f"Error fetching items: {e}")

    def delete_item(self):
            selected_item = self.item_tree.focus()
            if selected_item:
                item_id = self.item_tree.item(selected_item, "values")[0]
                if tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this item?"):
                    try:
                        response = requests.delete(f"http://127.0.0.1:8000/items/{item_id}")
                        response.raise_for_status()
                        tk.messagebox.showinfo("Success", "Item deleted successfully!")
                        self.load_items()

                    except requests.exceptions.RequestException as e:
                        tk.messagebox.showerror("Error", f"Error deleting item: {e}")

    def add_random_item(self):
        items = get_all_items()
        items_ids = [item["id"] for item in items]

        objects = ["Chair", "Book", "Laptop", "Table", "Cup", "Bicycle", "Clock", "Plant", "Umbrella", "Shoes"]
        adjectives = ["Brave", "Calm", "Energetic", "Gentle", "Happy", "Lucky", "Silly", "Tall", "Witty", "Charming"]
        
        try:
            random_id = max(items_ids) + 1
        except ValueError:
            random_id = 1
            
        random_name = random.choice(adjectives) + " " + random.choice(objects)
        random_description = "Just a random object"
        random_price = round(random.random() * 1000,2)
        random_quantity = random.randint(100, 2000)

        item_data = {
            "id": random_id,
            "name": random_name,
            "description": random_description,
            "price": random_price,
            "quantity":  random_quantity,
        }

        try:
            response = requests.post("http://127.0.0.1:8000/items/", json=item_data)
            response.raise_for_status()
            self.load_items()     

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error adding item: {e}")

    
    def open_edit_item_window(self):
        if not self.edit_item_window:
            selected_item = self.item_tree.focus()
            if selected_item:
                item_data = {
                    "id": self.item_tree.item(selected_item, "values")[0],
                    "name": self.item_tree.item(selected_item, "values")[1],
                    "description": self.item_tree.item(selected_item, "values")[2],
                    "price": self.item_tree.item(selected_item, "values")[3],
                    "quantity": self.item_tree.item(selected_item, "values")[4],
                }
                self.edit_item_window = EditItemWindow(self, item_data)
                self.edit_item_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(self.edit_item_window))

    def open_add_item_window(self):        
        if not self.add_item_window:
            self.add_item_window = AddItemWindow(self)
            self.add_item_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(self.add_item_window))
    
    def on_window_close(self, window):
        if window is self.add_item_window:
            self.add_item_window.destroy()
            self.add_item_window = None
        elif window is self.edit_item_window:
            self.edit_item_window.destroy()
            self.edit_item_window = None

if __name__ == "__main__":
    root = tk.Tk()
    item_window = ItemWindow(root)
    root.mainloop()
