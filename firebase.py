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
        return x.get(self.authkey)

    def set(self, path, data):
        x = self.reach(path)
        x.update(data, self.authkey)

    def remove(self, path):
        x = self.reach(path)
        x.remove(self.authkey)

    def find(self, path, value):
        x = self.reach(path)
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                return 'bad value'
        result = x.order_by_key().equal_to(value).get(self.authkey)
        if isinstance(result, pyrebase.pyrebase.PyreResponse):
            try:
                result = result.val()
            except:
                try:
                    result = result.each()
                except:
                    return None
        else:
            result = None
        if result == []:
            result = None
        return result

    def complex_find(self, start_path, ord, value, ord_type='key'):
        result = self.reach(start_path)
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                return 'bad value'
        result = result.order_by_child(ord)
        if ord_type == 'val' or ord_type == 'value':
            result = result.order_by_value()
        else:
            result = result.order_by_key().equal_to(value).get(self.authkey)
        if isinstance(result, pyrebase.pyrebase.PyreResponse):
            try:
                result = result.val()
            except:
                try:
                    result = result.each()
                except:
                    return None
        else:
            result = None
        if result == []:
            result = None
        return result

    def generate_possible_key(self, path):
        data = self.get(path)
        data = data.each()
        key = 0
        if data != None:
            for n in data:
                if n.val() != None:
                    key += 1
                else:
                    break
        return key

    def print_pyrebase(self, data):
        if isinstance(data, pyrebase.pyrebase.Database):
            data = data.get(self.authkey)
        if isinstance(data, pyrebase.pyrebase.PyreResponse):
            data = data.each()
            for k in data:
                print("{} , {}".format(k.key(), k.val()))
                return
        if isinstance(data, dict):
            for k in data:
                print("{} , {}".format(k, data[k]))
