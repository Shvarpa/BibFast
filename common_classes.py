class Projects(object):
    fields = {'name': None,
              'status': ['active', 'archived', 'projected']
              }

    @staticmethod
    def check_status(status):
        return status if status in Projects.fields['status'] else 'active'

    def __init__(self,name,status='active'):
        status=Projects.check_status(status)
        self.data={'name':name,'status':status}

    @classmethod
    def fromdict(cls, data):
        return cls(data.items()[0][0],data.items()[0][1])

    def set_name(self,name):
        self.data['name']=name

    def set_status(self,status):
        status=Projects.check_status(status)
        self.data['status']=status

