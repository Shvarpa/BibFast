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

    def __init__(self):
        #####verbose
        self.verbose = True
        #####verbose
        self.firebase = pyrebase.initialize_app(Firebase.config)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()
        self.token = None
        self.refresh_token()

    def refresh_token(self, new=False):
        tries = 3
        if not new:
            try:
                file = open('.token', 'r')
                self.token = file.readline()
                file.close()
                return
            except:
                pass
        while tries:
            try:
                if 'email' in Firebase.config:
                    username = Firebase.config['email']
                else:
                    username = input('Email:')
                if 'password' in Firebase.config:
                    password = Firebase.config['password']
                else:
                    password = input('Password:')  ##getpass.getpass()
                self.token = self.auth.sign_in_with_email_and_password(username, password)['idToken']
                try:
                    os.remove('.token')
                except:
                    pass
                file = open('.token', 'w')
                file.write(self.token)
                hide_file('.token')
                file.close()
            except requests.exceptions.HTTPError:
                self.token = None
            try:
                self.get('a')
                return True
            except:
                tries -= 1
        self.eprint('out of tries')
        return False

    # def refreash_token(self):

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

    def change_password(self, password):
        print('Enter old password')
        self.refresh_token(new=True)
        try:
            self.auth.delete_user(self.token)
        except:
            pass
        if 'email' in Firebase.config:
            self.auth.create_user_with_email_and_password(Firebase.config['email'], password)
        else:
            self.auth.create_user_with_email_and_password('rand@gmail.com', password)
