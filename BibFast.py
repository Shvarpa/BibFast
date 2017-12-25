import click
from common_classes import Projects, Citation
from firebase import Firebase
import requests
import pyrebase

pass_Firebase = click.make_pass_decorator(Firebase, ensure=True)


# connect cli commands
@click.group()
@pass_Firebase
def cli(Firebase):
    pass


@cli.command()
@click.pass_obj
@click.argument('name', type=str)
def create_project(Firebase, name):
    """add project to database by name"""
    project_id = Firebase.generate_possible_key("projects")
    Firebase.set(("projects", project_id), Projects(name).data)
    click.echo('project added')


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.argument('status')
def project_status_set(Firebase, project_id, status):
    """change project status by his project id"""
    if Firebase.find("projects", project_id) == None:
        click.echo("Error - project does'nt exist", err=not Firebase.verbose)
        return
    Firebase.update(('projects', project_id), {"status": status})
    click.echo('project #{} updated'.format(project_id), err=not Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=int)
def delete_project(Firebase, project_id):
    """delete project from database by his project id"""
    if Firebase.find("projects", project_id) == None:
        click.echo("Error - project does'nt exist", err=not Firebase.verbose)
        return
    else:
        Firebase.remove(("projects", project_id))
        click.echo('project #{} removed'.format(project_id), err=Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.option('--name', default=None, type=str)
@click.option('--status', default=None, type=str)
def project_update(Firebase, project_id, name, status):
    data = Firebase.find("projects", project_id)
    if data == None:
        click.echo("Error - project does'nt exist", err=not Firebase.verbose)
        return
    current_project = Projects.fromdict(data)
    if name != None:
        current_project.set_name(name)
    if status != None:
        current_project.set_status(status)
    Firebase.update(('projects', project_id), current_project.data)
    click.echo('project #{} updated'.format(project_id), err=not Firebase.verbose)


@cli.command()
@click.pass_obj
def print_projects(Firebase):
    Firebase.print_pyrebase(Firebase.get("projects"))
    click.echo("projects printed successfully", err=not Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument(Firebase, 'project_id')
def create_citation(Firebase, project_id):
    citation_id = Firebase.generate_possible_key("citations")
    citation = Citation(project_id)
    Firebase.set(['citations', citation_id], citation.data)
    click.echo('citation #{} created'.format(citation_id), err=not Firebase.verbose)


@cli.command()
@click.pass_obj
def password_init(Firebase):
    Firebase.set("user", {"password": "1234"})
    click.echo('password initialized', err=not Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument('password', type=str)
def set_password(Firebase, password):
    Firebase.update("user", {'password': password})
    click.echo('password updated', err=not Firebase.verbose)


# @cli.command()
# @click.pass_obj
# @click.argument('id')
# def fill_citation(Firebase, id):
#     exist = False
#     for x in Firebase.f_get(['citations']).each():
#         if int(x.key()) == int(id):
#             exist = True
#             break
#     if not exist:
#         print("bad id")
#         return
#     data = Firebase.f_get(["citations", id, "data"])
#     dict_from_data = {}
#     for x in data.each():
#         dict_from_data[x.key()] = x.val()
#     for x in dict_from_data:
#         if dict_from_data[x] == '':
#             dict_from_data[x] = input("enter {}:".format(x))
#     Firebase.f_update(["citations", id, "data"], dict_from_data)
#     print("citation id={} updated".format(id))
#

@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
@click.argument('name', type=str)
def citation_add_contributor(Firebase, citation_id, type, name):
    citation = Citation.fromdict(Firebase.find(("citations"), citation_id))
    status = citation.add_contributor(type, name)
    if isinstance(status, str):
        click.echo('could not add contributor ({})'.format(status), err=not Firebase.verbose)
        return
    Firebase.set(("citations", citation_id), citation.data)
    click.echo('add contributor to citation #{}'.format(citation_id), err=not Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
def citation_remove_contributor(Firebase, citation_id, type):
    if Firebase.find("citations", citation_id) == None:
        click.echo("Error - citation #{} does'nt exist".format(citation_id), err=not Firebase.verbose)
        return
    citation = Citation.fromdict(Firebase.find(("citations"), citation_id))
    status = citation.remove_contributor(type)
    if isinstance(status, str):
        click.echo('could not remove contributor ({})'.format(status), err=not Firebase.verbose)
        return
    Firebase.set(("citations", citation_id), citation.data)
    click.echo('removed contributor from citation #{}'.format(citation_id), err=not Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
def citation_set_type(Firebase, citation_id, type):
    if Firebase.find("citations", citation_id) == None:
        click.echo("Error - citation #{} does'nt exist".format(citation_id), err=not Firebase.verbose)
        return
    citation = Citation.fromdict(Firebase.find(("citations"), citation_id))
    status = citation.set_type(type)
    if isinstance(status, str):
        click.echo('could not set publication type ({})'.format(status), err=not Firebase.verbose)
        return
    Firebase.set(("citations", citation_id), citation.data)
    click.echo('removed contributor from citation #{}'.format(citation_id), err=not Firebase.verbose)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
def citation_fill_data(Firebase, citation_id):
    if Firebase.find("citations", citation_id) == None:
        click.echo("Error - citation #{} does'nt exist".format(citation_id), err=not Firebase.verbose)
        return
    citation = Citation.fromdict(Firebase.find(("citations"), citation_id))
    status = citation.fill_data()
    if isinstance(status, str):
        click.echo('could not fill citation data ({})'.format(status), err=not Firebase.verbose)
        return
    Firebase.set(("citations", citation_id), citation.data)
    click.echo('citation #{} updated'.format(citation_id), err=not Firebase.verbose)
    

####################################################################

@cli.command()
@click.pass_obj
@click.argument('format')
@click.argument('project_id')
def export(Firebase, format, project_id):
    try:
        project_id = int(project_id)
    except:
        print("bad project id")
        return
    try:
        exist = False
        for x in Firebase.f_get(['projects']).each():
            print(x.key())
            if int(x.key()) == int(project_id):
                exist = True
                break
        if not exist:
            print("project id desnt exist")
            return
    except:
        print("Error - excpecting int variable")
    cit_ids = []
    for x in Firebase.f_get(["citations"]).each():
        if project_id < len(x.val()['projects']) and x.val()['projects'][project_id] == 'active':
            cit_ids.append(x.key())
    if len(cit_ids) <= 0:
        return
    table = {'book': 'pubnonperiodical',
             'chapter': 'pubnonperiodical',
             'magazine': 'pubmagazine',
             'newspaper': 'pubnewspaper',
             'journal': 'pubjournal',
             'website': 'pubonline',
             }
    data = {}
    for x in Firebase.f_get(["citations"]).each():
        data[x.key()] = x.val()
    url = 'https://api.citation-api.com/rest/cite'
    file = open('export.txt', 'w')
    for x in cit_ids:
        bib_data = {"key": '6f84d749966f7623e3854371391daf87', 'url': url}
        type = data[x]['type']
        bib_data['source'] = type
        bib_data['style'] = format
        bib_data['pubtype'] = {'main': table[type]}
        bib_data[type] = {}
        bib_data[table[type]] = data[x]['data']
        contributors = data[x]['author']
        contributors['function'] = 'author'
        bib_data['contributors'] = [contributors]
        up = requests.post(url, json=bib_data)
        print(up.json())
        file.write(up.json())


cli()
