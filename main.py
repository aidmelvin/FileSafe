from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

import kivy
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

# import dp

def generate_key(input):
    password_provided = str(input)
    password = password_provided.encode()
    salt = b'5D\xb5V\xcd\t\xcfQ\xa4\xaa\xf8\xa0\x9c\xc7\x1c3'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # can only use kdf once
    return key

class MyWidget(GridLayout):
    dialog = None
    password = ''
    key = b''
    filepath = ''
    def selected(self, filename):
        try:
            self.ids.label.text = 'File chosen: ' + str(filename[0].split('/')[-1])
            self.filepath = str(filename[0])
        except:
            pass
    def encrypt(self, p):
        try:
            with open(self.filepath, 'rb') as fh:
                data = fh.read()
            if self.ids.password.text == '':
                raise NameError
            self.key = generate_key(self.ids.password.text)
            fernet = Fernet(self.key)
            encrypted = fernet.encrypt(data)
            new_filename = self.filepath + str('.encrypted')
            with open(new_filename, 'wb') as fh:
                fh.write(encrypted)
            self.ids.password.text = ''
            show_popup('Success', 'Your file was encrypted to \"' + str(new_filename.split('/')[-1]) + '\"')
        except FileNotFoundError:
            show_popup('Operation Failed', 'No file was provided')
        except NameError:
            show_popup('Operation Failed', 'For security reasons, a password must be provided')
    def decrypt(self, p):
        try:
            with open(self.filepath, 'rb') as fh:
                data = fh.read()
            self.key = generate_key(self.ids.password.text)
            fernet = Fernet(self.key)
            decrypted = fernet.decrypt(data)
            new_filename = str(self.filepath)[:-10]
            with open(new_filename, 'wb') as fh:
                fh.write(decrypted)
            self.ids.password.text = ''
            show_popup('Success', 'Your file was decrypted to \"' + str(new_filename.split('/')[-1]) + '\"')
        except FileNotFoundError:
            show_popup('Operation Failed', 'No file was provided')
        except:
            show_popup('Operation Failed', 'Password incorrect')

class P(FloatLayout):
    def __init__(self, m, **kwargs):
        super().__init__(**kwargs)
        L1 = Label(text=m,
                    # size_hint=0.6, 0.2,
                    pos_hint={"x":0.05, "top":1}
                )
        self.add_widget(L1)

def show_popup(TITLE, MSG):
    show = P(MSG)
    popupWindow = Popup(title=TITLE, content=show, size_hint=(None,None),size=('500dp','400dp'))
    popupWindow.open()

class FileSafe(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    window = FileSafe()
    window.run()
