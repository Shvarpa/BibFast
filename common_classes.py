import json


class Projects(object):
    fields = {'name': None,
              'status': ['active', 'archived', 'projected']
              }

    @staticmethod
    def check_status(status):
        return status if status in Projects.fields['status'] else 'active'

    def __init__(self, name, status='active'):
        status = Projects.check_status(status)
        self.data = {'name': name, 'status': status}

    @classmethod
    def fromdict(cls, data):
        return cls(data.items()[0][0], data.items()[0][1])

    def set_name(self, name):
        self.data['name'] = name

    def set_status(self, status):
        status = Projects.check_status(status)
        self.data['status'] = status


############################################################

class Citation(object):
    fields = {
        "status": ['active', 'inactive'],
        "type": ['book', 'chapter', 'magazine', 'newspaper', 'journal', 'website'],
        "get pub type": {
            'book': 'pubnonperiodical',
            'chapter': 'pubnonperiodical',
            'magazine': 'pubmagazine',
            'newspaper': 'pubnewspaper',
            'journal': 'pubjournal',
            'website': 'pubonline',
        },
        "pubtype": {
            'pubnonperiodical': {
                'title': 'Book title',
                'publisher': 'Publisher name',
                'city': 'City published',
                'state': 'State published',
                'vol': 'Volume',
                'editiontext': 'Edition',
                'year': 'Year published (four digits: ie 2000)',
                'start': 'Start page (for chapter sources)',
                'end': 'End page (for chapter sources)',
            },
            'pubmagazine': {
                'title': 'Book title',
                'vol': 'Magazine volume',
                'day': 'Day published (1-31)',
                'month': 'Month published (full month names: January through December)',
                'year': 'Year published (four digits: ie. 2000)',
                'start': 'Start page of article',
                'end': 'End page of article',
                'nonconsecutive': '1 if article is on nonconsecutive pages, blank or 0 if not',
            },
            'pubnewspaper': {
                'title': 'Newspaper title',
                'edition': 'Newspaper edition (late, etc.)',
                'section': 'Newspaper section',
                'city': 'City published',
                'day': 'Day published (1-31)',
                'month': 'Month published (full month names: January through December)',
                'year': 'Year published (four digits: ie. 2000)',
                'start': 'Start page of article',
                'end': 'End page of article',
                'nonconsecutive': '1 if article is on nonconsecutive pages, blank if not',
            },
            'pubjournal': {
                'title': 'Journal title',
                'issue': 'Journal issue number',
                'volume': 'Journal volume number',
                'restarts': 'Do journal issues restart their page numbering? If yes, use 1, if no, leave blank.',
                'series': 'Journal series',
                'year': 'Year published (four digits: ie. 2000)',
                'start': 'Start page of article',
                'end': 'End page of article',
                'nonconsecutive': '1 if article is on nonconsecutive pages, blank if not',
            },
            'pubonline': {
                'title': 'Web site title',
                'inst': 'Institution associated with',
                'day': 'Day published (1-31)',
                'month': 'Month published (full month names: January through December)',
                'year': 'Year published (four digits: ie. 2000)',
                'url': 'URL of Web site (ie. http://www.google.com)',
                'dayaccessed': 'Day Web page was accessed',
                'monthaccessed': 'Month Web page was accessed',
                'yearaccessed': 'Year Web page was accessed',
            },
        },
        "style": ['mla7', 'chicagob'],
        "contributors": {
            'function': ['author', 'editor', 'compiler', 'translator'],
            'name': ['first', 'middle', 'last'],
        },
    }

    def __init__(self, project_id):
        self.data = {}
        self.data['projects'] = (project_id, 'active')

    def set_type(self, type):
        if not type in Citation.fields['get pub type']:
            return "bad type"
        self.data['type'] = type
        pub_type = Citation.fields['get pub type'][type]
        if not 'data' in self.data:
            self.data['data'] = {}
        self.data['data']['pubdata'] = {key: '' for key, _ in Citation.fields['pubtype'][pub_type].items()}

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
            return 'bad name'
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

    def remove_contributor(self,function):
        if not 'data' in self.data:
            return 'no contributers'
        if not 'contributors' in self.data['data']:
            return 'no contributers'
        for c in self.data['data']['contributors']:
            if c['function']==function:
                self.data['data']['contributors'].remove(c)
                break
        return 'deleted contributor'

