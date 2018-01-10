import click
import main
from firebase import Firebase

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
    """
    creates new project named <name> with active status
    command interface:  "bib create_project <name>"
    example:            "bib create_project donald"
    """
    main.create_project(Firebase, name)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.argument('status', type=str)
def project_status_set(Firebase, project_id, status):
    """
    changes project with id #<project_id> status to <status>, status must be in ('active','projected','archived')
    command interface:  "bib project_status_set <project_id> <status>"
    example:            "bib project_status_set 1 projected
    """
    main.project_status_set(Firebase, project_id, status)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=int)
def delete_project(Firebase, project_id):
    """
    delete project with id #<project_id>, removes references from citations
    command interface:  "bib delete_project <project_id>"
    example:            "bib delete_project 1"
    """
    main.delete_project(Firebase, project_id)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.option('--name', default=None, type=str)
@click.option('--status', default=None, type=str)
def project_update(Firebase, project_id, name, status):
    """
    update project with id #<project_id> with the following: <name>, <status>; status must be in ('active','projected','archived')
    command interface:  "bib project_update <project_id> --name <name> --status <status>"
    example:            "bib project_update 1 --name donald --active"
    """
    main.project_update(Firebase, project_id, name, status)


@cli.command()
@click.pass_obj
def print_projects(Firebase):
    """
    prints all projects
    command interface:  "bib print_projects"
    """
    main.print_projects(Firebase)


@cli.command()
@click.pass_obj
def password_init(Firebase):
    """
    initializes password after login to '123456', uses token from firebase uid, requires relogin
    command interface:  "bib password_init"
    """
    main.password_init(Firebase)


@cli.command()
@click.pass_obj
@click.argument('password', type=str)
def set_password(Firebase, password):
    """
    changes password after login to <password>, password must be atleast 6 digits long, uses token from firebase uid, requires relogin
    command interface:  "bib set_password <password>"
    example:            "bib set_password 1234567"
    """
    main.set_password(Firebase, password)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
def create_citation(Firebase, project_id):
    """
    creates empty citaiton linked to project with <project_id>, sets it's status as active
    command interface:  "bib create_citation <project_id>"
    example:            "bib create_citation 1"
    """
    main.create_citation(Firebase, project_id)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
@click.argument('name', type=str)
def citation_add_contributor(Firebase, citation_id, type, name):
    """
    adds contributor to a citation with id #<citation_id>,
    with <type> in ('author', 'editor', 'compiler', 'translator'),
    and <name> contributor's <name> must be in contributor list
    command interface:  "bib citation_add_contributor <citation_id> <type> <name>"
    example:            "bib citation_add_contributor 1 author 'albert einstein'"
    """
    main.citation_add_contributor(Firebase, citation_id, type, name)

@cli.command()
@click.pass_obj
@click.argument('name', type=str)
def add_contributor(Firebase, name):
    """
    adds contributor's <name> to contributor list
    command interface:  "bib add_contributor <name>"
    example:            "bib add_contributor 'albert einstein'"
    """
    main.add_contributor(Firebase, name)

@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
def citation_remove_contributor(Firebase, citation_id, type):
    """
    removes contributor of type=<type> from citation with id #<citation_id>
    command interface:  "bib citation_remove_contributor <citation_id> <type>"
    example:            "bib citation_remove_contributor 1 'author'"
    """
    main.citation_remove_contributor(Firebase, citation_id, type)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
def citation_set_type(Firebase, citation_id, type):
    """
    changes citation with id#<citation_id> type to <type> in ('book', 'chapter', 'magazine', 'newspaper', 'journal', 'website'),
    creates all the fields that go along with the corresponding type
    command interface:  "bib citation_set_type <citation_id> <type>"
    example:            "bib citation_set_type 1 book"
    """
    main.citation_set_type(Firebase, citation_id, type)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
def citation_fill_data(Firebase, citation_id):
    """
    lets the user input all the fields of the citation with id #<citation_id>, must be done after citation_set_type
    will request user input for each field with explanation of the field
    command interface:  "bib citation_fill_data <citation_id>"
    example:            "bib citation_fill_data 1"
    """
    main.citation_fill_data(Firebase, citation_id)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('project_id', type=str)
def citation_add_project(Firebase, citation_id, project_id):
    """
    adds to citation with id #<citation_id> a reference to project with id #<project_id> in 'active' status
    command interface:  "bib citation_add_project <citation_id> <project_id>"
    example:            "bib citation_add_project 1 1"
    """
    main.citation_add_project(Firebase, citation_id, project_id)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('project_id', type=str)
@click.argument('project_status', type=str)
def citation_change_project_status(Firebase, citation_id, project_id, project_status):
    """
    changes citation's project's status to <status> in ('active','inactive')
    command interface:  "bib citation_change_project_status <citation_id> <project_id> <project_status>"
    example:            "bib citation_change_project_status 1 1 active"
    """
    main.citation_change_project_status(Firebase, citation_id, project_id, project_status)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('project_id', type=str)
def citation_remove_project(Firebase, citation_id, project_id):
    """
    removes project from citation
    command interface:  "bib citation_remove_project <citation_id> <project_id>"
    example:            "bib citation_remove_project 1 1"
    """
    main.citation_remove_project(Firebase, citation_id, project_id)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.option('--style',default='mla7', type=str)
@click.option('--filename',default='export.txt', type=str)
def project_export_citations(Firebase, project_id, style, filename):
    """
    exports all project citations to required format with id #<project_id> from citation with id #<citation_id>
    command interface:  "bib project_export_citations <project_id>"
    example:            "bib project_export_citations 1"
    """
    main.project_export_citations(Firebase, project_id, style, filename)



@cli.command()
@click.option('--req',default='popular', type=str)
def get_styles(req, limit):
    """
    lets user see possible easybib format styles, by default show most popular, <req> in ('all','popular')
    command interface:  "bib get_styles --req <req>"
    example:            "bib get_styles --req all"
    """
    print(main.get_styles(req))


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.option('--filename',default='export.txt', type=str)
def project_export_citations_each_style(Firebase, project_id, filename):
    """
    lets user select each citation's format style by input from user for each
    option to choose filename, by default 'export.txt'
    command interface:  "bib project_export_citations_each_style <project_id> --filename <filename>"
    example:            "bib project_export_citations_each_style 1 --filename new"
    """
    main.project_export_citations_each_style(Firebase, project_id, filename)

@cli.command()
@click.pass_obj
def print_changes(Firebase):
    """
    prints all changes made to firebase
    command interface:  "bib print_changes"
    """
    main.print_changes(Firebase)

