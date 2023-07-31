from rich import print
from rich.columns import Columns
from rich.console import Console
from datetime import datetime
import click
import requests
from commande import initConfig, statusOK, parcoursList, optionData, argumentData, waitUser
from templates.user import templateUserStr


def templateClients(console, listItem, here):
    end = min(here + 5, len(listItem))
    for i in range(here, end):
        client = listItem[i]
        console.rule(f"Client {client['id']}", style="bold cyan", characters="=")
        console.print(Columns([printClient(client), templateUserStr(client['commercial_contact'])], expand=True))
    return end

def printClient(client):
    data = (
        f"id : {client['id']}\n"
        f"email : {client['email']}\n"
        f"first_name : {client['first_name']}\n"
        f"last_name : {client['last_name']}\n"
        f"telephone : {client['tel']}\n"
        f"entreprise : {client['entreprise']}\n"
        f"créé le {datetime.strptime(client['time_created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')}\n"
        f"derniere modification faite le {datetime.strptime(client['time_update'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')}"
    )
    return data


def templateClient(console, client):
    console.rule(f"Client {client['id']}", style="bold cyan", characters="=")
    console.print(Columns([printClient(client), templateUserStr(client['commercial_contact'])], expand=True))

def templateClientStr(client):
    data = (
        f"[bold cyan]Client :[/bold cyan]\n"
        f"  id : {client['id']}\n"
        f"  email : {client['email']}\n"
        f"  first_name : {client['first_name']}\n"
        f"  last_name : {client['last_name']}\n"
        f"  telephone : {client['tel']}\n"
        f"  entreprise : {client['entreprise']}\n"
    )
    return data


@click.group(name='client')
def client():
    pass


@client.command()
def show():
    console = Console()
    conf = initConfig()
    response = requests.get(conf['url']+'api/clients/all/', headers=conf["headers"])
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule(f"[red]0 client trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} clients trouvés[/green]", style="bold green", characters="=")
            console.print(f'\n')
            parcoursList(console, templateClients, reponseJson)
            console.print(f'\n')
            console.rule(style="bold green", characters="=")

@client.command()
def showFilter():
    console = Console()
    conf = initConfig()
    response = requests.get(conf['url']+'api/clients/', headers=conf["headers"])
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule(f"[red]0 client trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} clients trouvés[/green]", style="bold green", characters="=")
            console.print(f'\n')
            parcoursList(console, templateClients, reponseJson)
            console.print(f'\n')
            console.rule(style="bold green", characters="=")


@client.command()
@click.argument('email', required=False)
@click.argument('first_name', required=False)
@click.argument('last_name', required=False)
@click.argument('tel', required=False)
@click.argument('entreprise', required=False)
def create(email=None, first_name=None, last_name=None, tel=None, entreprise=None):
    data = {}
    data = argumentData(data, email, 'email', "entrez l'email de du client ")
    data = argumentData(data, first_name, 'first_name', "entrez le prenom du client ")
    data = argumentData(data, last_name, 'last_name', "entrez le nom du client ")
    data = argumentData(data, tel, 'tel', "entrez le numero de téléphone du client ")
    data = argumentData(data, entreprise, 'entreprise', "entrez l'entreprise du client ")
    conf = initConfig()
    response = requests.post(conf['url']+'api/clients/', headers=conf["headers"], data=data)
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 201:
            console = Console()
            console.rule(f"[green]Client créé avec succes ![green]", style="bold green", characters="=")
            templateClient(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")


@client.command()
@click.argument('id',required=False)
@click.option('--email')
@click.option('--first_name')
@click.option('--last_name')
@click.option('--tel')
@click.option('--entreprise')
def change(id=None, email=None, first_name=None, last_name=None, tel=None, entreprise=None):
    dataUrl = argumentData({}, id,'id',"id du contrat dont vous voulez modifier les données")
    print("[bold cyan]Toutes les option laissez vide lors de l'appel vont vous etre demandé, veuillez ne rien rentrer si vous ne voulez pas les modifier[/bold cyan]")
    waitUser()
    data = {}
    data = optionData(data, email, 'email', "entrez le nouvel email du client ")
    data = optionData(data, first_name, 'first_name', "entrez le nouveau prenom du client ")
    data = optionData(data, last_name, 'last_name', "entrez le nouveau nom du client ")
    data = optionData(data, tel, 'tel', "entrez le nouveau numero de téléphone du client ")
    data = optionData(data, entreprise, 'entreprise', "entrez la nouvelle entreprise du client ")
    if data == {}:
        print(f"[bold red]Vous n'avez rien changer au client[/bold red]")
        return None
    conf = initConfig()
    response = requests.put(conf['url']+'api/clients/'+dataUrl['id']+'/', headers=conf["headers"], data=data)
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 200:
            console = Console()
            console.rule(f"[green]Client modifié avec succes ![green]", style="bold green", characters="=")
            templateClient(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")
