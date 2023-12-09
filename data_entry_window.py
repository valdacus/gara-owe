import tkinter as tk
import sqlite3

class DataEntryWindow(tk.Frame):
    def __init__(self, root, data_callback, return_callback, display_callback):
#     def __init__(self, root, data_callback, return_callback):
        super().__init__(root)
        self.root = root
        self.root.title("Okno Dodawania Danych")

        # Dodaj elementy do okna dodawania danych
        self.label_firstname = tk.Label(self, text="Imię:")
        self.entry_firstname = tk.Entry(self)

        self.label_lastname = tk.Label(self, text="Nazwisko:")
        self.entry_lastname = tk.Entry(self)

        self.label_phone = tk.Label(self, text="Numer telefonu:")
        self.entry_phone = tk.Entry(self)

        self.label_vin = tk.Label(self, text="Numer VIN:")
        self.entry_vin = tk.Entry(self)

        self.label_details = tk.Label(self, text="Marka/Rodzaj/Kolor:")
        self.entry_details = tk.Entry(self)

        self.label_description = tk.Label(self, text="Opis:")
        self.entry_description = tk.Text(self, height=5, wrap=tk.WORD)

        self.button_add = tk.Button(self, text="Dodaj", command=self.add_data)
        self.button_return = tk.Button(self, text="Powrót", command=return_callback)

        self.button_show_data = tk.Button(self, text="Wyświetl Dane", command=display_callback)


        # Rozmieszczenie elementów w oknie
        self.label_firstname.grid(row=0, column=0)
        self.entry_firstname.grid(row=0, column=1)

        self.label_lastname.grid(row=1, column=0)
        self.entry_lastname.grid(row=1, column=1)

        self.label_phone.grid(row=2, column=0)
        self.entry_phone.grid(row=2, column=1)

        self.label_vin.grid(row=3, column=0)
        self.entry_vin.grid(row=3, column=1)

        self.label_details.grid(row=4, column=0)
        self.entry_details.grid(row=4, column=1)

        self.label_description.grid(row=5, column=0)
        self.entry_description.grid(row=5, column=1)

        self.button_add.grid(row=6, column=0, columnspan=2)
        self.button_return.grid(row=7, column=0, columnspan=2)
        self.button_show_data.grid(row=8, column=0, columnspan=2)

        # Przekazanie funkcji wywołania po dodaniu danych
        self.data_callback = data_callback

    def add_data(self):
        # Pobieranie danych z pól wprowadzania
        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()
        phone = self.entry_phone.get()
        vin = self.entry_vin.get()
        details = self.entry_details.get()
        description = self.entry_description.get("1.0", tk.END).strip()

        # Zapisywanie danych do bazy SQLite
        self.save_to_database(firstname, lastname, phone, vin, details, description)

        # Wywołaj funkcję callback po dodaniu danych
        self.data_callback()

    def save_to_database(self, firstname, lastname, phone, vin, details, description):
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()

        cursor.execute("""
                INSERT INTO entries (firstname, lastname, phone, vin, details, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (firstname, lastname, phone, vin, details, description))

        connection.commit()
        connection.close()

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("Okno Dodawania Danych")

    def hide(self):
        self.pack_forget()
