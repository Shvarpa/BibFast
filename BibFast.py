import click
from common_classes import Project, Citation
import main
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
    main.create_project(Firebase, name)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.argument('status', type=str)
def project_status_set(Firebase, project_id, status):
    main.project_status_set(Firebase, project_id, status)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=int)
def delete_project(Firebase, project_id):
    main.delete_project(Firebase, project_id)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.option('--name', default=None, type=str)
@click.option('--status', default=None, type=str)
def project_update(Firebase, project_id, name, status):
    main.project_update(Firebase, project_id, name, status)


@cli.command()
@click.pass_obj
def print_projects(Firebase):
    main.print_projects(Firebase)


@cli.command()
@click.pass_obj
def password_init(Firebase):
    main.password_init(Firebase)


@cli.command()
@click.pass_obj
@click.argument('password', type=str)
def set_password(Firebase, password):
    main.set_password(Firebase, password)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
def create_citation(Firebase, project_id):
    main.create_citation(Firebase, project_id)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
@click.argument('name', type=str)
def citation_add_contributor(Firebase, citation_id, type, name):
    main.citation_add_contributor(Firebase, citation_id, type, name)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
def citation_remove_contributor(Firebase, citation_id, type):
    main.citation_remove_contributor(Firebase, citation_id, type)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('type', type=str)
def citation_set_type(Firebase, citation_id, type):
    main.citation_set_type(Firebase, citation_id, type)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
def citation_fill_data(Firebase, citation_id):
    main.citation_fill_data(Firebase, citation_id)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('project_id', type=str)
def citation_add_project(Firebase, citation_id, project_id):
    main.citation_add_project(Firebase, citation_id, project_id)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('project_id', type=str)
@click.argument('project_status', type=str)
def citation_change_project_status(Firebase, citation_id, project_id, project_status):
    main.citation_change_project_status(Firebase, citation_id, project_id, project_status)


@cli.command()
@click.pass_obj
@click.argument('citation_id', type=str)
@click.argument('project_id', type=str)
def citation_remove_project(Firebase, citation_id, project_id):
    main.citation_remove_project(Firebase, citation_id, project_id)


@cli.command()
@click.pass_obj
@click.argument('project_id', type=str)
@click.option('--style', type=str)
@click.option('--filename', type=str)
def project_export_citations(Firebase, project_id, style, filename):
    main.project_export_citations(Firebase, project_id, style, filename)


@cli.command()
@click.pass_obj
@click.argument('request', type=str)
@click.option('--style', default='popular', type=str)
@click.option('--limit', default=10, type=int)
def get_styles(request, limit):
    main.get_styles(request, limit)


cli()
