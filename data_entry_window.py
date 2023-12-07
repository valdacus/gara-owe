import tkinter as tk

class DataEntryWindow(tk.Frame):
    def __init__(self, root, data_callback, return_callback):
        super().__init__(root)
        self.root = root
        self.root.title("Okno Dodawania Danych")

        # Dodaj elementy do okna dodawania danych
        self.label_data = tk.Label(self, text="Wprowadź dane:")
        self.entry_data = tk.Entry(self)
        self.button_add = tk.Button(self, text="Dodaj", command=self.add_data)
        self.button_return = tk.Button(self, text="Powrót", command=return_callback)

        # Rozmieszczenie elementów w oknie
        self.label_data.grid(row=0, column=0)
        self.entry_data.grid(row=0, column=1)
        self.button_add.grid(row=1, column=0, columnspan=2)
        self.button_return.grid(row=2, column=0, columnspan=2)

        # Przekazanie funkcji wywołania po dodaniu danych
        self.data_callback = data_callback

    def add_data(self):
        data = self.entry_data.get()
        # Tutaj możesz dodać logikę do obsługi danych (np. zapis do listy)
        print(f"Dane dodane: {data}")

        # Wywołaj funkcję callback po dodaniu danych
        self.data_callback()

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("Okno Dodawania Danych")

    def hide(self):
        self.pack_forget()
