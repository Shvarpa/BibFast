import click
from db_classes import Project, Citation
from firebase import Firebase

pass_Firebase = click.make_pass_decorator(Firebase, ensure=True)


# connect cli commands
@click.group()
@pass_Firebase
def cli(Firebase):
    pass


@cli.command()
@click.pass_obj
@click.argument('name',type=str)
def create_project(Firebase, name):
    """
    recieve name and add project
    """
    key = Firebase.generate_possible_key("project")
    Firebase.set(("project", key), {"name": name, "status": "active"})
    click.echo('project added')


@cli.command()
@click.pass_obj
@click.argument('key',type=int)
def delete_project(Firebase, key):
    if Firebase.find("projects",key)==None:
        click.echo('Error project dont exist',err=True)
    else:
        Firebase.remove(("projects",key))
        click.echo('project #{} removed'.format(key),err=True)

#########################################################################################

@cli.command()
@click.pass_obj
@click.argument('key',type=int)
@click.argument('status',type=str)
def project_status_set(Firebase, key, status):
    if Firebase.find("projects", key) == None:

    if_exist = False
    for n in Firebase.db.child("project").get(Firebase.authkey).each():
        if key == n.key():
            if_exist = True
            Firebase.db.child("project").child(key).update({'status': status}, Firebase.authkey)
            print('status updated')

    if not if_exist:
        print('Error project dont exist')


@cli.command()
@click.pass_obj
def print_projects(Firebase):
    print('projects:')
    for n in Firebase.db.child("project").get(Firebase.authkey).each():
        print(n.key())


@cli.command()
@click.pass_obj
@click.argument('citation_id')
@click.argument(Firebase, 'project_name')
def create_citation(citation_id, project_name):
    data = {}
    for k in ["project", "status", "type", "auther", "year", "publisher"]:
        if k == "project":
            data[k] = {"name": project_name}
        elif k == "auther":
            data[k] = {"first": None, "last": None}
        elif k == "status":
            data[k] = "active"
        else:
            data[k] = ""
        Firebase.db.child("citation").child(citation_id).set(data, Firebase.authkey)


@cli.command()
@click.pass_obj
def password_init(Firebase):
    Firebase.db.child("user").set({"password": "1234"}, Firebase.authkey)


@cli.command()
@click.pass_obj
@click.argument('password')
def set_password(Firebase, password):
    Firebase.db.child("user").update({"password": password}, Firebase.authkey)


@cli.command()
@click.pass_obj
@click.argument('id')
@click.argument('status')
def project_status_set(Firebase, id, status):
    """change id status by id"""
    if status not in {"active", "projected", "archived"}:
        print("bad status")
        return
    for n in Firebase.get(["projects"]).each():
        if int(id) == int(n.key()):
            Firebase.update(["projects", id], {"status": status})
            print('status updated')
            return
    print('Error project dont exist')


@cli.command()
@click.pass_obj
@click.argument('id')
@click.argument('status')
def project_status_set(Firebase, id, status):
    """change id status by id"""
    if status not in ("active", "projected", "archived"):
        print("bad status")
        return
    for n in Firebase.get(["projects"]).each():
        if int(id) == int(n.key()):
            Firebase.update(["projects", id], {"status": status})
            print('status updated')
            return
    print('Error project dont exist')


@cli.command()
@click.pass_obj
@click.argument('project_id')
@click.argument('status')
@click.argument('type')
def create_citation(Firebase, project_id, status, type):
    """add dataless citation to database linked to a project and status"""
    for x in Firebase.f_get(['projects']).each():
        if x.key == project_id:
            print("bad project id")
            return
    if status not in ("active", "inactive"):
        print("bad status")
        return
    cit_type_details_table = {
        "book": [
            "title", "publisher", "city", "state", "vol", "editiotext", "year", "start", "end"
        ]
        ,
        "chapter": [
            "title", "publisher", "city", "state", "vol", "editiotext", "year", "start", "end"
        ]
        ,
        "magazine": [
            "title", "vol", "day", "month", "year", "start", "end"
        ],
        "newspaper": [
            "title", "edition", "section", "city", "day", "month", "year", "start", "end", "nonconsecutive"
        ],
        "journal": [
            "title", "issue", "volume", "restarts", "series", "year", "start", "end", "nonconsecutive"
        ],
        "website": [
            "title", "inst", "day", "month", "year", "url", "dayaccessed", "monthaccssed", "yearaccessed"
        ],
    }
    if type not in cit_type_details_table.keys():
        print("bad type")
        return
    citations = Firebase.f_get(["citations"]).each()
    if not citations: return
    id = 0
    for n in citations:
        if id == n.key() and n.val():
            id += 1
        else:
            break
    Firebase.f_set(["citations", id], {"projects": {project_id: status}, "type": type})
    data = {}
    for k in cit_type_details_table[type]:
        data[k] = ""
    Firebase.f_set(["citations", id, "data"], data)


@cli.command()
@click.pass_obj
@click.argument('id')
def fill_citation(Firebase, id):
    exist = False
    for x in Firebase.f_get(['citations']).each():
        if int(x.key()) == int(id):
            exist = True
            break
    if not exist:
        print("bad id")
        return
    data = Firebase.f_get(["citations", id, "data"])
    dict_from_data = {}
    for x in data.each():
        dict_from_data[x.key()] = x.val()
    for x in dict_from_data:
        if dict_from_data[x] == '':
            dict_from_data[x] = input("enter {}:".format(x))
    Firebase.f_update(["citations", id, "data"], dict_from_data)
    print("citation id={} updated".format(id))


@cli.command()
@click.pass_obj
@click.argument('id')
@click.argument('status')
def project_status_set(Firebase, id, status):
    """change id status by id"""
    if status not in ("active", "projected", "archived"):
        print("bad status")
        return
    for n in Firebase.get(["projects"]).each():
        if int(id) == int(n.key()):
            Firebase.update(["projects", id], {"status": status})
            print('status updated')
            return
    print('Error project dont exist')


@cli.command()
@click.pass_obj
@click.argument('project_id')
@click.argument('status')
@click.argument('type')
def create_citation(Firebase, project_id, status, type):
    """add dataless citation to database linked to a project and status"""
    for x in Firebase.f_get(['projects']).each():
        if x.key == project_id:
            print("bad project id")
            return
    if status not in ("active", "inactive"):
        print("bad status")
        return
    cit_type_details_table = {
        "book": [
            "title", "publisher", "city", "state", "vol", "editiotext", "year", "start", "end"
        ]
        ,
        "chapter": [
            "title", "publisher", "city", "state", "vol", "editiotext", "year", "start", "end"
        ]
        ,
        "magazine": [
            "title", "vol", "day", "month", "year", "start", "end"
        ],
        "newspaper": [
            "title", "edition", "section", "city", "day", "month", "year", "start", "end", "nonconsecutive"
        ],
        "journal": [
            "title", "issue", "volume", "restarts", "series", "year", "start", "end", "nonconsecutive"
        ],
        "website": [
            "title", "inst", "day", "month", "year", "url", "dayaccessed", "monthaccssed", "yearaccessed"
        ],
    }
    if type not in cit_type_details_table.keys():
        print("bad type")
        return
    citations = Firebase.f_get(["citations"]).each()
    if not citations: return
    id = 0
    for n in citations:
        if id == n.key() and n.val():
            id += 1
        else:
            break
    Firebase.f_set(["citations", id], {"projects": {project_id: status}, "type": type})
    data = {}
    for k in cit_type_details_table[type]:
        data[k] = input("enter {}:".format(k))
    Firebase.f_set(["citations", id, "data"], data)


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
