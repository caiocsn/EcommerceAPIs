import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import tkinter as tk
from tkinter import filedialog
import pandas as pd

from models.db_models import ItemDB, OrderDB
from db.db import SessionLocal
from .utils import *

class ExcelExportWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Export to Excel")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        db = SessionLocal()

        # Query all objects from ItemDB class
        items = get_all_items()
        df_items = pd.DataFrame([item for item in items])
        
        # Query all objects from OrderDB class
        orders = get_all_orders()
        df_orders = pd.DataFrame([order for order in orders])
        
        db.close()

        # Open a Tkinter file dialog to select the save path
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            self.destroy()
            return

        # Save the DataFrames to separate tabs in the selected Excel file
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:

            df_items.to_excel(writer, sheet_name='Items', index=False)
            df_orders.to_excel(writer, sheet_name='Orders', index=False)
            
            items_sheet = writer.sheets['Items']
            (max_row, max_col) = df_items.shape
            items_sheet.set_column(0, max_col - 1, 12)
            items_sheet.autofilter(0, 0, max_row, max_col - 1)

            orders_sheet = writer.sheets['Orders']
            (max_row, max_col) = df_orders.shape
            orders_sheet.set_column(0, max_col - 1, 12)
            orders_sheet.autofilter(0, 0, max_row, max_col - 1)

        
        self.destroy()
        
    def on_close(self):
        self.parent.focus_set()
        self.destroy()

