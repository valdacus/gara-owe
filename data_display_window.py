import tkinter as tk
from tkinter import ttk

class DataDisplayWindow:
    def __init__(self, root, data_list):
        self.root = root
        self.root.title("Wyświetlanie Danych")

        self.data_list = data_list

        # Dodaj elementy do okna wyświetlania danych
        self.tree = ttk.Treeview(root, columns=("Data"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Data", text="Dane")

        self.button_return = tk.Button(root, text="Powrót", command=self.return_to_data_entry_window)

        # Rozmieszczenie elementów w oknie
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.button_return.grid(row=1, column=0, columnspan=2)

    def return_to_data_entry_window(self):
        self.root.withdraw()

if __name__ == "__main__":
    root = tk.Tk()
    data_list = ["Dane 1", "Dane 2", "Dane 3"]  # Przykładowe dane
    app = DataDisplayWindow(root, data_list)
    root.mainloop()
