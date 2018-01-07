import pyrebase
import requests
from common_func import *
import os


class Firebase(object):
    config = {
        "apiKey": "AIzaSyCiCf_FZfbIuNe1pbG2ZRYw35dzFYrkTIU",
        "authDomain": "bibfast-6a6a9.firebaseapp.com",
        "databaseURL": "https://bibfast-6a6a9.firebaseio.com/",
        "storageBucket": "bibfast-6a6a9.appspot.com",
        "email": "rand@gmail.com"
    }

    def __init__(self, gui=False):
        #####verbose
        self.verbose = True
        #####verbose
        self.firebase = pyrebase.initialize_app(Firebase.config)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()
        self.token = None
        if not gui:
            self.refresh_token_retries()

    def refresh_token_retries(self):
        retries = 3
        while retries > 0:
            self.refresh_token(True)
            if self.token != None:
                return
            retries -= 1
        print("out of retries, quitting")
        quit()

    def refresh_token(self, new=False, password=None):
        if not new:
            try:
                file = open('.token', 'r')
                self.token = file.readline()
                file.close()
                self.get('a')
            except:
                self.token = None
                self.refresh_token(new=True)
        else:
            try:
                if 'email' in Firebase.config:
                    email = Firebase.config['email']
                else:
                    email = input('Email:')
                if password == None:
                    if 'password' in Firebase.config and password == None:
                        password = Firebase.config['password']
                    else:
                        password = input('Password:')  ##getpass.getpass()
                self.token = self.auth.sign_in_with_email_and_password(email, password)['idToken']
                self.get('a')
                try:
                    os.remove('.token')
                except:
                    pass
                file = open('.token', 'w')
                file.write(self.token)
                hide_file('.token')
                file.close()
            except:
                self.token = None

    def generate_possible_key(self, path):
        data = self.get(path)
        if data == None: return '0'
        key = 0
        while key <= data.__len__():
            if str(key) not in data or data[str(key)] == None:
                return str(key)
            else:
                key += 1
        return key

    def exists(self, path, key):
        data = self.get(path)
        if data == None: return False
        key = str(key)
        return key in data and data[key] != None

    def get(self, path=()):
        data = self.db.child(path).get(self.token)
        data = fix_list_to_dict(data) if isinstance(data, list) else data
        data = iterate_dicts(data, fix_list_to_dict) if data else data
        return data

    def print_pyrebase(self, path):
        data = self.get(path)
        try:
            pretty(data)
        except:
            print(data)

    def eprint(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def change_password(self, password,old_pass=None):
        if old_pass:
            self.refresh_token(new=True, password=old_pass)
        else:
            self.refresh_token_retries()
        try:
            self.auth.delete_user(self.token)
        except:
            pass
        if 'email' in Firebase.config:
            self.auth.create_user_with_email_and_password(Firebase.config['email'], password)
        else:
            self.auth.create_user_with_email_and_password('rand@gmail.com', password)
