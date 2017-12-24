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
        "projects": {
            'project_id': 'citation_status',
        },
        "type": ['book', 'chapter', 'magazine', 'newspaper', 'journal', 'website'],
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
            "style": ['mla7', 'chicagob'],
            "contributors": {
                'function': ['auther', 'editor', 'compiler', 'translator'],
                'first': '',
                'middle': '',
                'last': '',
            },
            "publisher": '',
        },
    },
