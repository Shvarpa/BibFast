from common_classes import Project, Citation
from common_func import filter_dict
from firebase import Firebase
import requests
import os
import json


# ref=Firebase()


def create_project(ref, name):
    """add project to database by name
    :param ref:Firebase
    :param name:str
    """
    if len(name)>20:
        ref.eprint('Error- name too long')
        return
    if len(name)<1:
        ref.eprint('Error-too short')
        return
    project_id = ref.generate_possible_key("projects")
    ref.db.child("projects/{}".format(project_id)).set(Project(name).data, ref.token)
    ref.eprint('project #{} added'.format(project_id))


def project_status_set(ref, project_id, status):
    """change project status by his project id
    :param ref:Firebase
    :param project_id:int
    :param status:int
    """
    if status != 'active' and status != 'projected' and status!= 'archived':
        ref.eprint('Error - valid statuses are: active, projected ,archived')
        return
    try:
        project_id = str(project_id)
    except:
        ref.eprint("bad project id, unstringable")
        return
    if not ref.exists("projects", project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    data = ref.get("projects/{}".format(project_id))
    curr_project = Project.fromdict(data)
    report = curr_project.set_status(status)
    if isinstance(report, str):
        ref.eprint("could not set status ({})".format(report))
        return
    ref.db.child('projects/{}'.format(project_id)).set(curr_project.data, ref.token)
    ref.eprint('project #{} updated'.format(project_id))


def delete_project(ref, project_id):
    """delete project from database by his project id
    :param ref:Firebase
    :param project_id:str
    """
    project_id = str(project_id)
    if not ref.exists("projects", project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    ref.db.child('projects/{}'.format(project_id)).remove(ref.token)
    citations = ref.get('citations')
    if isinstance(citations, dict):
        citations = filter_dict(citations, 'projects', "{}:".format(project_id), False)
        ref.db.child("citations").set(citations, ref.token)
    ref.eprint('project #{} removed'.format(project_id))


def project_update(ref, project_id, name=None, status=None):
    """update project from database by his project id, name and/or status
    :param ref:Firebase
    :param project_id:str
    :param name:str
    :param status:str
    """
    project_id = str(project_id)
    if not ref.exists("projects", project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    data = ref.get("projects/{}".format(project_id))
    current_project = Project.fromdict(data)
    current_project.set_name(name) if name != None else None
    report = current_project.set_status(status) if status != None else None
    if isinstance(report, str):
        ref.eprint('cannot change status ({})'.format(report))
        return
    ref.db.child('projects/{}'.format(project_id)).set(current_project.data, ref.token)
    ref.eprint('project #{} updated'.format(project_id))


def print_projects(ref):
    """prints out all projects in database
    :param ref:Firebase
    """
    ref.print_pyrebase("projects")
    ref.eprint("projects printed successfully")


def login(ref,password):
    ref.refresh_token(new=True,password=password)
    if ref.token==None:
        ref.eprint('incorrect password')
        return
    ref.eprint('logged in')


def password_init(ref):
    """initializes password in user database
    :param ref:Firebase
    """
    new_pass = '123456'
    ref.change_password(new_pass)
    ref.db.child("user").set({"password": new_pass}, ref.token)
    ref.eprint('password initialized')


def set_password(ref, new_pass):
    """changes password in user database
    :param ref:Firebase
    :param password:str
    """
    if not isinstance(newpass,int):
        ref.eprint('bad password- please enter only numbers! ')
        return
    if len(new_pass) < 6:
        ref.eprint('bad password-too short')
        return
    if len(new_pass)> 8:
        ref.eprint('bad password- too long')
        return

    ref.change_password(new_pass)
    ref.db.child("user").set({'password': new_pass}, ref.token)
    ref.eprint('password updated')


def create_citation(ref, project_id):
    """add citation to database by id
    :param ref:Firebase
    :param project_id:str
    """
    project_id = str(project_id)
    if project_id>'9' and project_id <'0':
        ref.eprint('bad id- please enter only numbers! ')
        return
        
    if not ref.exists("projects", project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    citation_id = ref.generate_possible_key("citations")
    curr_citation = Citation(project_id)
    ref.db.child('citations/{}'.format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('citation #{} created'.format(citation_id))


def citation_add_contributor(ref, citation_id, type, name):
    """add contributor to citation by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    :param name:str
    """
    citation_id = str(citation_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.add_contributor(type, name)
    if isinstance(report, str):
        ref.eprint('could not add contributor ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('add contributor to citation #{}'.format(citation_id))


def citation_remove_contributor(ref, citation_id, type):
    """remove first appearance of contributor of the same type in citation by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    """
    citation_id = str(citation_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.remove_contributor(type)
    if isinstance(report, str):
        ref.eprint('could not remove contributor ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('removed contributor from citation #{}'.format(citation_id))


def citation_set_type(ref, citation_id, type):
    """change citation type in database by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    """
    citation_id = str(citation_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.set_type(type)
    if isinstance(report, str):
        ref.eprint('could not set publication type ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('changed citation #{} type to {}'.format(citation_id, type))


def citation_fill_data(ref, citation_id):
    """fill citation data in database by its id
    :param ref:Firebase
    :param citation_id:str
    """
    citation_id = str(citation_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.fill_data()
    if isinstance(report, str):
        ref.eprint('could not fill citation data ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('citation #{} updated'.format(citation_id))


def citation_add_project(ref, citation_id, project_id):
    """add project to citation
    :param ref:Firebase
    :param citation_id:str
    :param project_id:str
    """
    
    citation_id = str(citation_id)
    project_id = str(project_id)

    try:int(citation_id)
    except:
        ref.eprint('bad id - use only numbers')
        return
    try: int(project_id)
    except:
        ref.eprint('bad id - use only numbers')
        return
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    if not ref.exists('projects', project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    if ref.exists('citations/{}/projects'.format(citation_id), project_id):
        ref.eprint("project #{} allready in citation #{}".format(project_id, citation_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.add_project(project_id)
    if isinstance(report, str):
        ref.eprint('could not add project ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('citation #{} updated'.format(citation_id))


def citation_change_project_status(ref, citation_id, project_id, project_status):
    """change status of project in citation
    :param ref:Firebase
    :param citation_id:str
    :param project_id:str
    :param project_status:str
    """
    if project_status != 'active' and project_status!= 'projected' and project_status != 'archived':
        ref.eprint('Error- choose between: active, projeted, archived')
        return
    citation_id = str(citation_id)
    project_id = str(project_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    if not ref.exists('projects', project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.change_project_status(project_id, project_status)
    if isinstance(report, str):
        ref.eprint('could not change project status ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('citation #{} updated'.format(citation_id))


def citation_remove_project(ref, citation_id, project_id):
    """remove project from citation
    :param ref:Firebase
    :param citation_id:str
    :param project_id:str
    """
    citation_id = str(citation_id)
    project_id = str(project_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    if not ref.exists('projects', project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.remove_project(project_id)
    if isinstance(report, str):
        ref.eprint('could not remove project ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('citation #{} updated'.format(citation_id))


def project_get_citations(ref, project_id):  #####not in cli######################
    """remove project from citation
    :param ref:Firebase
    :param project_id:str
    """
    project_id = str(project_id)
    if not ref.exists('projects', project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    data = ref.get('citations')
    data = filter_dict(data, 'projects', '{}:{}'.format(project_id, 'active'))
    return data


def project_export_citations(ref, project_id, style='mla7', filename='export.txt'):
    """remove project from citation
    :param ref:Firebase
    :param citation_id:str
    :param project_id:str
    """
    if not isinstance(filename, str):
        filename = 'export.txt'
    else:
        filename += '.txt' if filename[-4:] != '.txt' else ''
    project_id = str(project_id)
    if not ref.exists('projects', project_id):
        ref.eprint("project #{} does'nt exist".format(project_id))
        return
    data = ref.get('citations')
    data = filter_dict(data, 'projects', '{}:{}'.format(project_id, 'active'))
    formatted = [Citation(data[item]).export_easybib(style) for item in data]
    file = open(filename, 'w')
    for formatted_citation in formatted:
        json.dump(formatted_citation, file, ensure_ascii=False)
        file.write('\n')
    file.close()
    os.startfile(filename)


def get_styles(request='popular', limit=10):
    if request == 'popular':
        data = requests.post(url='http://api.citation-api.com/2.1/rest/popular-styles').json()['data']
        return ''.join("{}, ".format(i) for i in data.keys())
    elif request == 'all':
        data = requests.post(url='http://api.citation-api.com/2.1/rest/styles').json()['data']
        if limit:
            return ''.join("{}, ".format(k) for k in list(data.keys())[0:limit])
        else:
            return ''.join("{}, ".format(k) for k in data.keys())
