import tkinter as tk
from tkinter import ttk
import sqlite3

class DataDisplayWindow(tk.Frame):
    def __init__(self, root, return_callback):
        super().__init__(root)
        self.root = root
        self.root.title("Wyświetlanie Danych")

        # Dodaj elementy do okna wyświetlania danych
        self.tree = ttk.Treeview(self, columns=("Imię", "Nazwisko", "Telefon", "VIN", "Szczegóły", "Opis"), show="headings")

#         self.tree.heading("ID", text="ID")
        self.tree.heading("Imię", text="Imię")
        self.tree.heading("Nazwisko", text="Nazwisko")
        self.tree.heading("Telefon", text="Telefon")
        self.tree.heading("VIN", text="VIN")
        self.tree.heading("Szczegóły", text="Szczegóły")
        self.tree.heading("Opis", text="Opis")

        self.button_return = tk.Button(self, text="Powrót", command=return_callback)

        # Rozmieszczenie elementów w oknie
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.button_return.pack()

        # Wczytaj dane do widoku
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM entries
            WHERE date_deleted IS NULL
        """)

        data = cursor.fetchall()

        for row in data:
            self.tree.insert("", "end", values=row)

        connection.close()

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("Wyświetlanie Danych")

    def hide(self):
        self.pack_forget()
