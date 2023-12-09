import tkinter as tk
import sqlite3


from login_window import LoginWindow
from data_entry_window import DataEntryWindow
from data_display_window import DataDisplayWindow

def create_table():
    connection = sqlite3.connect("app_data.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname VARCHAR(40),
            lastname VARCHAR(40),
            phone VARCHAR(20),
            vin VARCHAR(20),
            details VARCHAR(100),
            description TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_deleted DATETIME
        )
    """)

    connection.commit()
    connection.close()

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplikacja Tkinter")
#         self.geometry("600x400")

        # Utwórz instancję widoku wyświetlania danych
        self.data_display_view = DataDisplayWindow(self, self.show_data_entry_window)

        # Utwórz instancję widoku wprowadzania danych
        self.data_entry_view = DataEntryWindow(self, self.add_data, self.show_main_window, self.show_data_display_window)

        # Pokaż widok logowania
        self.show_login_view()

    def show_login_view(self):
        self.login_window = LoginWindow(self, self.show_data_entry_window)
        self.login_window.show()

    def show_data_entry_window(self):
        self.login_window.hide()
        self.data_entry_view.show()

    def show_data_display_window(self):
        self.data_entry_view.hide()
        self.data_display_view.show()

    def show_main_window(self):
        self.data_display_view.hide()
        self.show_login_view()

    def add_data(self):
        print("Dane dodane.")
        self.show_data_display_window()

if __name__ == "__main__":
    create_table()
    app = MainApplication()
    app.mainloop()
