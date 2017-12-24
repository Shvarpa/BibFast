import pyrebase
import requests


class Firebase(object):
    def __init__(self, username='shvarpa@gmail.com', password='123456'):
        config = {
            "apiKey": "AIzaSyCiCf_FZfbIuNe1pbG2ZRYw35dzFYrkTIU",
            "authDomain": "bibfast-6a6a9.firebaseapp.com",
            "databaseURL": "https://bibfast-6a6a9.firebaseio.com/",
            "storageBucket": "bibfast-6a6a9.appspot.com",
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()
        try:
            self.authkey = self.auth.sign_in_with_email_and_password(username, password)['idToken']
        except requests.exceptions.HTTPError:
            self.authkey = None

    def login(self, username='shvarpa@gmail.com', password='123456'):
        try:
            self.authkey = self.auth.sign_in_with_email_and_password(username, password)['idToken']
        except requests.exceptions.HTTPError:
            self.authkey = None

    def reach(self, path):
        x = self.db
        if isinstance(path, str):
            path = path.replace(',', '/').split("/")
        for p in path:
            x = x.child(p)
        return x

    def update(self, path, data):
        x = self.reach(path)
        x.update(data, self.authkey)

    def get(self, path):
        x = self.reach(path)
        return x.get(self.authkey).each()

    def set(self, path, data):
        x = self.reach(path)
        x.update(data, self.authkey)

    def remove(self, path):
        x = self.reach(path)
        x.remove(self.authkey)

    def find(self, path, value, ord='key'):
        x = self.reach(path)
        ord_table = {'key': x.order_by_key, 'val': x.order_by_value()}
        result = ord_table[ord]().equal_to(value) if ord in ord_table else x.order_by_child(ord)
        return result.get(self.authkey).each()

    def generate_possible_key(self, path):
        data = self.get(path).each()
        key = 0
        if data != None:
            for n in data:
                if n.val() != None:
                    key += 1
                else:
                    break
        return key
