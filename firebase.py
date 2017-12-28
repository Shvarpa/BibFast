import pyrebase
import requests

# DONE change all id's to strings instead of ints

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

    def generate_possible_key(self, path):
        data = self.db.child(path).get(self.token)
        if data == None: return '0'
        key = 0
        for val in data:
            if val != None:
                key = key + 1
            else:
                break
        return str(key)

    def exists(self, path, value):
        data = self.convert_to_dict(path)
        if data == None: return False
        try:
            value = str(value)
        except:
            value = value
        return value in data

    def convert_to_dict(self, path, filter_path=None, filter_item=None):
        data = self.db.child(path).get(self.token)

        def fix_list_to_dict(curr):
            return {str(index): curr[index] for index in range(len(curr))}

        def iterate_dicts(curr, func):
            for key, value in curr.items():
                if isinstance(value, list):
                    curr[key] = func(value)
                if isinstance(value, dict):
                    iterate_dicts(value, func)
            return curr

        def dict_pather(dict_data, path):
            if isinstance(path, str): path = path.split('/')
            for p in path:
                dict_data = dict_data.get(p)
                if dict_data == None:
                    return {}
            return dict_data

        data = fix_list_to_dict(data) if isinstance(data, list) else data
        data = iterate_dicts(data, fix_list_to_dict)
        if isinstance(filter_item, str): filter_item = tuple(None if x == '' else x for x in filter_item.split(':'))
        if filter_path:
            if filter_item[0] and filter_item[1]:
                data = {k: v for k, v in data.items() if filter_item in dict_pather(data[k], filter_path).items()}
            elif filter_item[1]:
                data = {k: v for k, v in data.items() if filter_item[1]==dict_pather(data[k], filter_path).get(filter_item[0])}
            elif filter_item[0]:
                data = {k: v for k, v in data.items() if filter_item[0] in dict_pather(data[k], filter_path)}
        return data

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
