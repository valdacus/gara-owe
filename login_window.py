import tkinter as tk

class LoginWindow(tk.Frame):
    def __init__(self, root, login_callback):
        super().__init__(root)
        self.root = root
        self.root.title("Okno Logowania")

        # Dodaj elementy do okna logowania
        self.label_username = tk.Label(self, text="Nazwa użytkownika:")
        self.entry_username = tk.Entry(self)
        self.label_password = tk.Label(self, text="Hasło:")
        self.entry_password = tk.Entry(self, show="*")
        self.button_login = tk.Button(self, text="Zaloguj", command=login_callback)

        # Rozmieszczenie elementów w oknie
        self.label_username.grid(row=0, column=0)
        self.entry_username.grid(row=0, column=1)
        self.label_password.grid(row=1, column=0)
        self.entry_password.grid(row=1, column=1)
        self.button_login.grid(row=2, column=0, columnspan=2)

        # Przekazanie funkcji wywołania po zalogowaniu
        self.login_callback = login_callback

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.root.title("Okno Logowania")

    def hide(self):
        self.pack_forget()
