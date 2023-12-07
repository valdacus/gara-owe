import tkinter as tk
from login_window import LoginWindow
from data_entry_window import DataEntryWindow

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Moja Aplikacja")

        # Lista do przechowywania danych
        self.data_list = []

        # Utwórz instancje widoków
        self.login_view = LoginWindow(self, self.show_data_entry_window)
        self.data_entry_view = DataEntryWindow(self, self.add_data, self.show_main_window)

        # Pokaż widok logowania
        self.show_login_view()

    def show_main_window(self):
        # Tutaj możesz dodać kod do otwierania głównego widoku aplikacji
        # Na razie możemy po prostu zakończyć program
        self.destroy()

    def show_login_view(self):
        # Pokaż widok logowania
        self.login_view.show()
        # Ukryj widok danych
        self.data_entry_view.hide()

    def show_data_entry_window(self):
        # Pokaż widok dodawania danych
        self.data_entry_view.show()
        # Ukryj widok logowania
        self.login_view.hide()

    def add_data(self):
        # Tutaj możesz dodać logikę do obsługi danych (np. zapis do listy)
        # Później możesz dodać logikę do otwierania innego widoku lub
        # wykonania innych działań w zależności od potrzeb
        self.show_main_window()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
