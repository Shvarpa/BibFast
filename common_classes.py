import json
from collections import OrderedDict
import requests


class Project(object):
    fields = {'name': None,
              'status': ['active', 'archived', 'projected']
              }

    @staticmethod
    def check_status(status):
        return status if status in Project.fields['status'] else None

    def __init__(self, name, status='active'):
        status = Project.check_status(status)
        self.data = {'name': name, 'status': status}

    @classmethod
    def fromdict(cls, data):
        return cls(data['name'], data['status'])

    def set_name(self, name):
        self.data['name'] = name

    def set_status(self, status):
        if not Project.check_status(status):
            return 'bad status'
        self.data['status'] = status


############################################################

class Citation(object):
    fields = {
        "status": ['active', 'inactive'],
        "type": ['book', 'chapter', 'magazine', 'newspaper', 'journal', 'website'],
        "get pubtype": {
            'book': 'pubnonperiodical',
            'chapter': 'pubnonperiodical',
            'magazine': 'pubmagazine',
            'newspaper': 'pubnewspaper',
            'journal': 'pubjournal',
            'website': 'pubonline',
        },
        "source": {
            'book': {},
            'chapter': {'title': 'name of chapter/story', 'type': 'two options: story/essay'},
            'magazine': {'title': 'article title'},
            'newspaper': {'title': 'article title'},
            'journal': {'title': 'article title'},
            'website': {'title': 'web page title'},
        },
        "pubtype": {
            'pubnonperiodical': OrderedDict([
                ('title', 'Book title'),
                ('publisher', 'Publisher name'),
                ('city', 'City published'),
                ('state', 'State published'),
                ('vol', 'Volume'),
                ('editiontext', 'Edition'),
                ('year', 'Year published (four digits: ie 2000)'),
                ('start', 'Start page (for chapter sources)'),
                ('end', 'End page (for chapter sources)')]),
            'pubmagazine': OrderedDict([
                ('title', 'Book title'),
                ('vol', 'Magazine volume'),
                ('day', 'Day published (1-31)'),
                ('month', 'Month published (full month names: January through December)'),
                ('year', 'Year published (four digits: ie. 2000)'),
                ('start', 'Start page of article'),
                ('end', 'End page of article'),
                ('nonconsecutive', '1 if article is on nonconsecutive pages, blank or 0 if not')]),

            'pubnewspaper': OrderedDict([
                ('title', 'Newspaper title'),
                ('edition', 'Newspaper edition (late, etc.)'),
                ('section', 'Newspaper section'),
                ('city', 'City published'),
                ('day', 'Day published (1-31)'),
                ('month', 'Month published (full month names: January through December)'),
                ('year', 'Year published (four digits: ie. 2000)'),
                ('start', 'Start page of article'),
                ('end', 'End page of article'),
                ('nonconsecutive', '1 if article is on nonconsecutive pages, blank if not',)]),
            'pubjournal': OrderedDict([
                ('title', 'Journal title'),
                ('issue', 'Journal issue number'),
                ('volume', 'Journal volume number'),
                ('restarts',
                 'Do journal issues restart their page numbering? If yes, use 1, if no, leave blank.'),
                ('series', 'Journal series'),
                ('year', 'Year published (four digits: ie. 2000)'),
                ('start', 'Start page of article'),
                ('end', 'End page of article'),
                ('nonconsecutive', '1 if article is on nonconsecutive pages, blank if not')]),
            'pubonline': OrderedDict([
                ('title', 'Web site title'),
                ('inst', 'Institution associated with'),
                ('day', 'Day published (1-31)'),
                ('month', 'Month published (full month names: January through December)'),
                ('year', 'Year published (four digits: ie. 2000)'),
                ('url', 'URL of Web site (ie. http://www.google.com)'),
                ('dayaccessed', 'Day Web page was accessed'),
                ('monthaccessed', 'Month Web page was accessed'),
                ('yearaccessed', 'Year Web page was accessed')]),
        },
        "style": ['mla7', 'chicagob'],
        "contributors": {
            'function': ['author', 'editor', 'compiler', 'translator'],
            'name': ['first', 'middle', 'last'],
        },
    }

    def __init__(self, param):
        """init either from dict or number"""
        if isinstance(param, dict):
            self.data = param
        else:
            self.data = {}
            self.data['projects'] = {param: 'active'}

    @classmethod
    def fromdict(cls, data):
        return cls(data)

    def check_path(self, path):
        x = self.data
        if isinstance(path, str):
            path = path.replace(',', '/').split("/")
        for p in path:
            x.get(p, None)
            if x == None:
                return False
        return True

    def add_project(self, project_id):
        if isinstance(self.data['projects'], list):
            try:
                self.data['projects'].pop(project_id)
            except:
                pass
            self.data['projects'].insert(project_id, 'active')
        elif isinstance(self.data['projects'], dict):
            self.data['projects'][project_id] = 'active'

    def change_project_status(self, project_id, status):
        print(self.data['projects'])
        if status not in ['active', 'inactive']:
            return 'bad status'
        if project_id not in self.data['projects']:
            return "has no project with id #{}".format(project_id)
        if isinstance(self.data['projects'], list):
            if project_id > len(self.data['projects']):
                return "has no project with id #{}".format(project_id)
            try:
                self.data['projects'].pop(project_id)
            except:
                pass
            self.data['projects'].insert(project_id,status)
        else:
            if project_id not in self.data['projects']:
                return "has no project with id #{}".format(project_id)
            self.data["projects"][project_id] = status

    def remove_project(self, project_id):
        if isinstance(self.data['projects'], list):
            if project_id > len(self.data['projects']):
                return "has no project with id #{}".format(project_id)
            self.data['projects'].pop(project_id)
        else:
            if project_id not in self.data['projects']:
                return "has no project with id #{}".format(project_id)
            self.data["projects"].remove(project_id)
        if self.data['projects'] == {} or self.data['projects'] == []:
            self.data = None

    def set_type(self, type):
        if type not in Citation.fields['get pubtype']:
            return "bad type"
        self.data['type'] = type
        pub_type = Citation.fields['get pubtype'][type]
        if not 'data' in self.data:
            self.data['data'] = {}
        self.data['data']['pubtype'] = {key: '' for key, _ in Citation.fields['pubtype'][pub_type].items()}
        self.data['data']['source'] = {key: '' for key, _ in Citation.fields['source'][type].items()}

    def fill_data(self):
        if 'type' not in self.data:
            return "citation type not set"
        type = self.data['type']
        pub_type = Citation.fields['get pubtype'][type]
        if not 'data' in self.data:
            self.data['data'] = {}
        self.data['data']['pubtype'] = {key: input("Enter {} ({}):".format(key, info)) for key, info in
                                        Citation.fields['pubtype'][pub_type].items()}
        self.data['data']['source'] = {key: input("Enter {} ({}):".format(key, info)) for key, info in
                                       Citation.fields['source'][type].items()}

    @staticmethod
    def create_contributor(function, name):
        if function not in Citation.fields['contributors']['function']:
            return "bad contributor type"
        if isinstance(name, str):
            name = name.split(' ')
        elif not isinstance(name, tuple) or isinstance(name, list):
            return "bad name"
        name_size = name.__len__()
        if name_size < 1:
            return "empty name"
        contributor = {}
        contributor['function'] = function
        contributor['first'] = name[0]
        if name_size == 2:
            contributor['last'] = name[1]
        elif name_size >= 3:
            contributor['middle'] = name[1]
            contributor['last'] = name[2]
        return contributor

    def add_contributor(self, function, name):
        contributor = Citation.create_contributor(function, name)
        if not isinstance(contributor, dict):
            return contributor
        if 'data' not in self.data:
            self.data['data'] = {}
        if 'contributors' not in self.data['data']:
            self.data['data']['contributors'] = []
        self.data['data']['contributors'].append(contributor)
        return True

    def remove_contributor(self, function):
        if not 'data' in self.data:
            return 'no contributers'
        if not 'contributors' in self.data['data']:
            return 'no contributers'
        for c in self.data['data']['contributors']:
            if c['function'] == function:
                self.data['data']['contributors'].remove(c)
                break
        return True

    def reformat_easybib(self, style='mla7'):
        if 'type' not in self.data:
            return None
        type = self.data['type']
        pubtype = Citation.fields["get pubtype"][type]
        reformated_data = {
            'key': "0bacd70c03c401a5b74fb39bcdeec6f4",
            'source': self.data['type'],
            'style': style,
            type: self.data['data']['source'] if self.check_path(('data', 'source')) else {},
            pubtype: self.data['data']['pubtype'] if self.check_path(('data', 'source')) else {},
            'contributors': self.data['data']['contributors'] if self.check_path(('data', 'contributors')) else [{}]
        }
        return reformated_data

    def export_easybib(self):
        test = requests.post('https://api.citation-api.com/rest/cite', json=self.reformat_easybib())
        print(test.json())
