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
        if not new:
            try:
                file = open('.token', 'r')
                self.token = file.readline()
                file.close()
                return
            except:
                pass
        try:
            if 'username' in Firebase.config:
                username = Firebase.config['username']
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

    def get(self, path):
        while True:
            try:
                data = self.db.child(path).get(self.token)
                break
            except:
                self.refresh_token(new=True)
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
