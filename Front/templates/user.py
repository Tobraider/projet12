from rich import print, align
from rich.console import Console
import click
import requests
from commande import initConfig, statusOK, parcoursList, optionData, argumentData, waitUser


def templateUsers(console, listItem, here):
    end = min(here + 5, len(listItem))
    for i in range(here, end):
        user = listItem[i]
        console.rule(f"Utilisateur {user['id']}", style="bold cyan", characters="=")
        console.print(f"id : {user['id']}")
        console.print(f"email : {user['email']}")
        console.print(f"first_name : {user['first_name']}")
        console.print(f"last_name : {user['last_name']}")
        console.print(f"role : {user['role']}")
    return end


def templateUser(console, user):
    console.rule(f"Utilisateur {user['id']}", style="bold cyan", characters="=")
    console.print(f"id : {user['id']}")
    console.print(f"email : {user['email']}")
    console.print(f"first_name : {user['first_name']}")
    console.print(f"last_name : {user['last_name']}")
    console.print(f"role : {user['role']}")

def templateUserStr(user,name=0):
    if name == 0:
        data = (
            f"[bold cyan]Contact commercial :[/bold cyan]\n"
            f"  id : {user['id']}\n"
            f"  email : {user['email']}\n"
            f"  first_name : {user['first_name']}\n"
            f"  last_name : {user['last_name']}\n"
            f"  role : {user['role']}\n"
        )
    elif name == 1:
        data = (
            f"[bold cyan]Support contact :[/bold cyan]\n"
            f"  id : {user['id']}\n"
            f"  email : {user['email']}\n"
            f"  first_name : {user['first_name']}\n"
            f"  last_name : {user['last_name']}\n"
            f"  role : {user['role']}\n"
        )
    else:
        data=""
    return data


@click.group(name='user')
def user():
    pass


@user.command()
def show():
    console = Console()
    conf = initConfig()
    response = requests.get(conf['url']+'api/users/', headers=conf["headers"])
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule(f"[red]0 utilisateur trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} utilisateurs trouvés[/green]", style="bold green", characters="=")
            console.print(f'\n')
            parcoursList(console, templateUsers, reponseJson)
            console.print(f'\n')
            console.rule(style="bold green", characters="=")


@user.command()
@click.argument('email', required=False)
@click.argument('password', required=False)
@click.argument('validate_password', required=False)
@click.argument('first_name', required=False)
@click.argument('last_name', required=False)
@click.argument("role", required=False)
def create(email=None, password=None, validate_password=None, first_name=None, last_name=None, role=None):
    data = {}
    data = argumentData(data, email, 'email', "entrez l'email de l'utilsateur ")
    data = argumentData(data, password, 'password', "entrez le mot de passe de l'utilisateur ",
                      {'hide_input':True}, True, validate_password,
                      "re rentrez le mot de passe de l'utilisateur afin de le valider ", {'hide_input':True},
                      "[bold red]Le mot de passe n'a pas ete correctement validé[/bold red]")
    data = argumentData(data, first_name, 'first_name', "entrez le prenom de l'utilisateur ")
    data = argumentData(data, last_name, 'last_name', "entrez le nom de l'utilisateur ")
    data = argumentData(data, role, 'role', "entrez le role ('Gestion'('GE'), 'Support'('SU') ou 'Commercial'('CO')) de l'utilisateur ")
    conf = initConfig()
    response = requests.post(conf['url']+'api/users/', headers=conf["headers"], data=data)
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 201:
            console = Console()
            console.rule(f"[green]Utilisateur créé avec succes ![green]", style="bold green", characters="=")
            templateUser(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")


@user.command()
@click.argument('id',required=False)
@click.option('--email')
@click.option('--password')
@click.option('--validate_password')
@click.option('--first_name')
@click.option('--last_name')
@click.option("--role")
def change(id=None, email=None, password=None, validate_password=None, first_name=None, last_name=None, role=None):
    dataUrl = argumentData({}, id,'id',"id de l'utilisateur dont vous voulez modifier les données")
    print("[bold cyan]Toutes les option laissez vide lors de l'appel vont vous etre demandé, veuillez ne rien rentrer si vous ne voulez pas les modifier[/bold cyan]")
    waitUser()
    data = {}
    data = optionData(data, email, 'email', "entrez le nouvel email de l'utilsateur ")
    data = optionData(data, password, 'password', "entrez le nouveau mot de passe de l'utilisateur ",
                      {'hide_input':True}, True, validate_password,
                      "re rentrez le nouveau mot de passe afin de le valider ", {'hide_input':True},
                      "[bold red]Le mot de passe n'a pas ete correctement validé[/bold red]")
    data = optionData(data, first_name, 'first_name', "entrez le nouveau prenom de l'utilisateur ")
    data = optionData(data, last_name, 'last_name', "entrez le nouveau nom de l'utilisateur ")
    data = optionData(data, role, 'role', "entrez le nouveau role ('Gestion'('GE'), 'Support'('SU') ou 'Commercial'('CO')) de l'utilisateur ")
    if data == {}:
        print(f"[bold red]Vous n'avez rien changer a l'utilisateur[/bold red]")
        return None
    conf = initConfig()
    response = requests.put(conf['url']+'api/users/'+dataUrl['id']+'/', headers=conf["headers"], data=data)
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 200:
            console = Console()
            console.rule(f"[green]Utilisateur modifié avec succes ![green]", style="bold green", characters="=")
            templateUser(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")


@user.command()
@click.argument('id',required=False)
def delete(id=None):
    dataUrl = argumentData({}, id,'id',"id de l'utilisateur que vous voulez supprimer ?")
    conf = initConfig()
    response = requests.delete(conf['url']+'api/users/'+dataUrl['id']+'/', headers=conf["headers"])
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 204:
            print(['[bold green] Utilisateur supprimé avec succes ![/bold green]'])
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")
