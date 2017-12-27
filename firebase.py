import pyrebase
import requests

# DONE change all id's to strings instead of ints
#TODO check if convert fixes string values for sub dictionaries

config = {
    "apiKey": "AIzaSyCiCf_FZfbIuNe1pbG2ZRYw35dzFYrkTIU",
    "authDomain": "bibfast-6a6a9.firebaseapp.com",
    "databaseURL": "https://bibfast-6a6a9.firebaseio.com/",
    "storageBucket": "bibfast-6a6a9.appspot.com",
    "username": "shvarpa@gmail.com",
    "password": "123456",
}


class Firebase(object):
    def __init__(self):
        #####verbose
        self.verbose = True
        #####verbose
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()
        self.login(config['username'], config['password'])

    def login(self, username, password):
        try:
            self.token = self.auth.sign_in_with_email_and_password(username, password)['idToken']
        except requests.exceptions.HTTPError:
            self.token = None

    # def reach(self, path):
    #     x = self.db
    #     if isinstance(path, str):
    #         path = path.replace(',', '/').split("/")
    #     for p in path:
    #         x = x.child(p)
    #     return x
    #
    # def update(self, path, data):
    #     x = self.reach(path)
    #     x.update(data, self.authkey)
    #
    # def get(self, path):
    #     x = self.reach(path)
    #     return x.get(self.authkey)
    #
    # def set(self, path, data):
    #     x = self.reach(path)
    #     x.update(data, self.authkey)
    #
    # def remove(self, path):
    #     x = self.reach(path)
    #     x.remove(self.authkey)
    #
    # def find(self, path, value):
    #     x = self.reach(path)
    #     if not isinstance(value, str):
    #         try:
    #             value = str(value)
    #         except:
    #             return 'bad value'
    #     result = x.order_by_key().equal_to(value).get(self.authkey)
    #     if isinstance(result, pyrebase.pyrebase.PyreResponse):
    #         try:
    #             result = result.val()
    #             if value in result:
    #                 result = result[value]
    #         except:
    #             try:
    #                 result = result.each()
    #             except:
    #                 return None
    #     else:
    #         result = None
    #     if result == []:
    #         result = None
    #     return result
    #
    # def complex_find(self, base, ord, value, ord_type='key'):
    #     result = self.reach(base)
    #     if isinstance(ord,str):
    #         ord = ord.replace(',', '/').split("/")
    #     result = result.order_by_child(ord)
    #     if ord_type == 'val' or ord_type == 'value':
    #         result = result.order_by_value()
    #     else:
    #         result = result.order_by_key().equal_to(value).get(self.authkey)
    #     if isinstance(result, pyrebase.pyrebase.PyreResponse):
    #         try:
    #             result = result.val()
    #             if value in result:
    #                 result=result[value]
    #         except:
    #             try:
    #                 result = result.each()
    #             except:
    #                 return None
    #     else:
    #         result = None
    #     if result == []:
    #         result = None
    #     return result

    def generate_possible_key(self, path):
        data = self.db.child(path).get(self.token).each()
        if data == None: return '0'
        key = 0
        for n in data:
            if n.val() != None:
                key += 1
            else:
                break
        return str(key)

    def exists(self, path, value):
        data = self.convert_to_dict(path)
        if data == None: return False
        try:
            value=str(value)
        except:
            value=value
        return value in data

    def convert_to_dict(self, path):
        data = self.db.child(path).get(self.token).each()
        if data == None: return None
        converted = {}
        for item in data:
            key=item.key()
            try: key=str(key)
            except:pass
            converted[key] = item.val()
        return converted

    def print_pyrebase(self, path):
        def pretty(d, indent=0):
            for key, value in d.items():
                print('\t' * indent + str(key))
                if isinstance(value, dict):
                    pretty(value, indent + 1)
                else:
                    print('\t' * (indent + 1) + str(value))

        data = self.convert_to_dict(path)
        try:
            pretty(data)
        except:
            print(data)

    def eprint(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)
