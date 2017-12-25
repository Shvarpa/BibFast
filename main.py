from common_classes import Projects, Citation
from firebase import Firebase

#ref=Firebase()


def create_project(ref, name):
    """add project to database by name
    :param ref:Firebase
    :param name:str
    """
    project_id = ref.generate_possible_key("projects")
    ref.set(("projects", project_id), Projects(name).data)
    ref.eprint('project added')


def project_status_set(ref, project_id, status):
    """change project status by his project id
    :param ref:Firebase
    :param project_id:str
    :param status:str
    """
    if ref.find("projects", project_id) == None:
        ref.eprint("Error - project does'nt exist")
        return
    ref.update(('projects', project_id), {"status": status})
    ref.eprint('project #{} updated'.format(project_id))



def delete_project(ref, project_id):
    """delete project from database by his project id
    :param ref:Firebase
    :param project_id:str
    """
    if ref.find("projects", project_id) == None:
        ref.eprint("Error - project does'nt exist")
        return
    else:
        ref.remove(("projects", project_id))
        ref.eprint('project #{} removed'.format(project_id))


def project_update(ref, project_id, name=None, status=None):
    """update project from database by his project id, name and/or status
    :param ref:Firebase
    :param project_id:str
    :param name:str
    :param status:str
    """
    data = ref.find("projects", project_id)
    if data == None:
        ref.eprint("Error - project does'nt exist")
        return
    current_project = Projects.fromdict(data)
    if name != None:
        current_project.set_name(name)
    if status != None:
        current_project.set_status(status)
    ref.update(('projects', project_id), current_project.data)
    ref.eprint('project #{} updated'.format(project_id))



def print_projects(ref):
    """prints out all projects in database
    :param ref:Firebase
    """
    ref.print_pyrebase(ref.get("projects"))
    ref.eprint("projects printed successfully")



def create_citation(ref, project_id):
    """add citation to database by id
    :param ref:Firebase
    :param project_id:str
    """
    citation_id = ref.generate_possible_key("citations")
    citation = Citation(project_id)
    ref.set(['citations', citation_id], citation.data)
    ref.eprint('citation #{} created'.format(citation_id))


def password_init(ref):
    """initializes password in user database
    :param ref:Firebase
    """
    ref.set("user", {"password": "1234"})
    ref.eprint('password initialized')


def set_password(ref, password):
    """changes password in user database
    :param ref:Firebase
    :param password:str
    """
    ref.update("user", {'password': password})
    ref.eprint('password updated')



def citation_add_contributor(ref, citation_id, type, name):
    """add contributor to citation by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    :param name:str
    """
    citation = Citation.fromdict(ref.find(("citations"), citation_id))
    status = citation.add_contributor(type, name)
    if isinstance(status, str):
        ref.eprint('could not add contributor ({})'.format(status))
        return
    ref.set(("citations", citation_id), citation.data)
    ref.eprint('add contributor to citation #{}'.format(citation_id))


def citation_remove_contributor(ref, citation_id, type):
    """remove first appearance of contributor of the same type in citation by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    """
    if ref.find("citations", citation_id) == None:
        ref.eprint("Error - citation #{} does'nt exist".format(citation_id))
        return
    citation = Citation.fromdict(ref.find(("citations"), citation_id))
    status = citation.remove_contributor(type)
    if isinstance(status, str):
        ref.eprint('could not remove contributor ({})'.format(status))
        return
    ref.set(("citations", citation_id), citation.data)
    ref.eprint('removed contributor from citation #{}'.format(citation_id))


def citation_set_type(ref, citation_id, type):
    """change citation type in database by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    """
    if ref.find("citations", citation_id) == None:
        ref.eprint("Error - citation #{} does'nt exist".format(citation_id))
        return
    citation = Citation.fromdict(ref.find(("citations"), citation_id))
    status = citation.set_type(type)
    if isinstance(status, str):
        ref.eprint('could not set publication type ({})'.format(status))
        return
    ref.set(("citations", citation_id), citation.data)
    ref.eprint('removed contributor from citation #{}'.format(citation_id))

def citation_fill_data(ref, citation_id):
    """fill citation data in database by its id
    :param ref:Firebase
    :param citation_id:str
    """
    if ref.find("citations", citation_id) == None:
        ref.eprint("Error - citation #{} does'nt exist".format(citation_id))
        return
    citation = Citation.fromdict(ref.find(("citations"), citation_id))
    status = citation.fill_data()
    if isinstance(status, str):
        ref.eprint('could not fill citation data ({})'.format(status))
        return
    ref.set(("citations", citation_id), citation.data)
    ref.eprint('citation #{} updated'.format(citation_id))

