from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
import bcrypt
import logging

# Konfiguracja logowania
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn
def add_record(conn, name, contact):
    sql = ''' INSERT INTO clients(name, contact) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, contact))
    conn.commit() 
    return cur.lastrowid

def read_record(conn, name):
    sql = 'SELECT * FROM clients WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (name,))
    return cur.fetchall()

def update_record(conn, id, name, contact):
    sql = ''' UPDATE clients SET name = ? , contact = ? WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (name, contact, id))
    conn.commit()

def delete_record(conn, id):
    sql = 'DELETE FROM clients WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
def find_user_by_username(conn, username):
    try:
        sql = 'SELECT * FROM users WHERE username=?'
        cur = conn.cursor()
        cur.execute(sql, (username,))
        return cur.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Exception in find_user_by_username: {e}")
        return None
	
class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.create_users_table(self.conn)  # Utwórz tabelę users przy każdym połączeniu
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create_users_table(self, conn):
        try:
            sql_create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
            """
            cur = conn.cursor()
            cur.execute(sql_create_users_table)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in create_users_table: {e}")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Username')
        self.password = TextInput(hint_text='Password', password=True)
        self.login_btn = Button(text='Login')
        self.login_btn.bind(on_press=self.validate_credentials)
        self.layout.add_widget(self.username)
        self.layout.add_widget(self.password)
        self.layout.add_widget(self.login_btn)
        self.add_widget(self.layout)

    def validate_credentials(self, instance):
        username = self.username.text
        password = self.password.text

        with DatabaseConnection('my_database.db') as conn:
            user = find_user_by_username(conn, username)
            if user and check_password(user['password'], password.encode('utf-8')):
                print("Logowanie pomyślne. Przejście do głównego ekranu.")
                self.manager.current = 'main'
            else:
                print("Nieprawidłowa nazwa użytkownika lub hasło.")

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.menu_layout = BoxLayout(size_hint_y=None, height=50)
        self.menu_layout.add_widget(Button(text='Klienci'))
        self.menu_layout.add_widget(Button(text='Pojazdy'))
        self.menu_layout.add_widget(Button(text='Naprawy'))
        self.layout.add_widget(self.menu_layout)

        # Formularz Danych
        self.form_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        self.form_layout.add_widget(Label(text='Imię i Nazwisko'))
        self.form_layout.add_widget(TextInput())
        self.form_layout.add_widget(Label(text='Kontakt'))
        self.form_layout.add_widget(TextInput())
        self.layout.add_widget(self.form_layout)

        # Przyciski Akcji
        self.action_btns_layout = BoxLayout(size_hint_y=None, height=50)
        self.action_btns_layout.add_widget(Button(text='Dodaj'))
        self.action_btns_layout.add_widget(Button(text='Edytuj'))
        self.action_btns_layout.add_widget(Button(text='Usuń'))
        self.layout.add_widget(self.action_btns_layout)

        # Lista Rekordów
        self.list_view = ListView()
        self.layout.add_widget(self.list_view)
        self.add_widget(self.layout)

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.confirm_password_input = TextInput(hint_text='Confirm Password', password=True)
        self.register_btn = Button(text='Register')
        self.register_btn.bind(on_press=self.register_user)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.confirm_password_input)
        self.layout.add_widget(self.register_btn)
        self.add_widget(self.layout)

    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if not self.is_password_strong(password):
            print("Hasło nie spełnia wymagań bezpieczeństwa.")
            return

        if password != confirm_password:
            print("Hasła nie są identyczne.")
            return

        with DatabaseConnection('my_database.db') as conn:
            if not self.is_username_unique(conn, username):
                print("Nazwa użytkownika jest już zajęta.")
                return

            hashed_password = hash_password(password.encode('utf-8'))
            try:
                sql = ''' INSERT INTO users(username, password) VALUES(?,?) '''
                cur = conn.cursor()
                cur.execute(sql, (username, hashed_password))
                conn.commit()
                print("Rejestracja zakończona sukcesem.")
            except sqlite3.Error as e:
                print(f"Błąd bazy danych: {e}")
            except Exception as e:
                print(f"Wyjątek w trakcie rejestracji: {e}")

def is_password_strong(self, password):
        # Przykładowe kryteria: minimalna długość 8 znaków, zawiera litery i cyfry
        if len(password) < 4:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        return True

def is_username_unique(self, conn, username):
        try:
            sql = 'SELECT * FROM users WHERE username=?'
            cur = conn.cursor()
            cur.execute(sql, (username,))
            return cur.fetchone() is None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        except Exception as e:
            print(f"Exception in is_username_unique: {e}")
            return False

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.menu_layout = BoxLayout(size_hint_y=None, height=50)
        self.menu_layout.add_widget(Button(text='Klienci'))
        self.menu_layout.add_widget(Button(text='Pojazdy'))
        self.menu_layout.add_widget(Button(text='Naprawy'))
        self.layout.add_widget(self.menu_layout)

        # Formularz Danych
        self.form_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        self.form_layout.add_widget(Label(text='Imię i Nazwisko'))
        self.form_layout.add_widget(TextInput())
        self.form_layout.add_widget(Label(text='Kontakt'))
        self.form_layout.add_widget(TextInput())
        self.layout.add_widget(self.form_layout)

        # Przyciski Akcji
        self.action_btns_layout = BoxLayout(size_hint_y=None, height=50)
        self.action_btns_layout.add_widget(Button(text='Dodaj'))
        self.action_btns_layout.add_widget(Button(text='Edytuj'))
        self.action_btns_layout.add_widget(Button(text='Usuń'))
        self.layout.add_widget(self.action_btns_layout)

        # Lista Rekordów
        self.list_view = RecycleView()
        self.layout.add_widget(self.list_view)
        self.add_widget(self.layout)
#         self.update_list_view()

        # Menu
        menu_layout = BoxLayout(size_hint_y=None, height=50)
        menu_layout.add_widget(Button(text='Klienci'))
        menu_layout.add_widget(Button(text='Pojazdy'))
        menu_layout.add_widget(Button(text='Naprawy'))
        self.add_widget(menu_layout)

        # Formularz Danych
        form_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        form_layout.add_widget(Label(text='Imię i Nazwisko'))
        form_layout.add_widget(TextInput())
        form_layout.add_widget(Label(text='Kontakt'))
        form_layout.add_widget(TextInput())
        self.add_widget(form_layout)

        # Przyciski Akcji
        action_btns_layout = BoxLayout(size_hint_y=None, height=50)
        action_btns_layout.add_widget(Button(text='Dodaj'))
        action_btns_layout.add_widget(Button(text='Edytuj'))
        action_btns_layout.add_widget(Button(text='Usuń'))
        self.add_widget(action_btns_layout)

        # Lista Rekordów
        self.list_view = RecycleView()
        self.add_widget(self.list_view)
#         self.update_list_view()

    def update_list_view(self):
        # Połączenie z bazą danych SQLite
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Przykładowe zapytanie SQL, dostosuj je do swoich potrzeb
        cursor.execute("SELECT * FROM TwojaTabela")
        rows = cursor.fetchall()
        
        # Zamknij połączenie z bazą danych
        conn.close()

        # Tworzenie listy danych do wyświetlenia na liście
        data = [{'text': f'{row[0]} {row[1]}'} for row in rows]  # Przykładowa konwersja danych
        
        # Aktualizacja adaptera listy
        list_adapter = self.list_view.adapter
        list_adapter.data = data

        # Odśwież widok listy
        list_adapter.get_view(None)  # None oznacza odświeżenie całej listy

class CRMApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    CRMApp().run()
