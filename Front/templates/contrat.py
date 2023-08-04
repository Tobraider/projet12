from rich import print
from rich.columns import Columns
from rich.console import Console
from datetime import datetime
import click
from commande import initConfig, statusOK, parcoursList, optionData, argumentData, waitUser, myRequests
from templates.user import templateUserStr
from templates.client import templateClientStr


def templateContrats(console, listItem, here):
    end = min(here + 5, len(listItem))
    for i in range(here, end):
        contrat = listItem[i]
        console.rule(f"Contrat {contrat['id']}", style="bold cyan", characters="=")
        console.print(
            Columns(
                [
                    printContrat(contrat),
                    templateClientStr(contrat['client']),
                    templateUserStr(contrat['commercial_contact'])
                ],
                expand=True
            )
        )
    return end


def printContrat(contrat):
    data = (
        f"id : {contrat['id']}\n"
        f"prix_ttl : {contrat['prix_ttl']}\n"
        f"prix_restant : {contrat['prix_restant']}\n"
        f"statut : {contrat['statut']}\n"
        f"créé le {datetime.strptime(contrat['time_created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')}\n"
    )
    return data


def templateContrat(console, contrat):
    console.rule(f"Contrat {contrat['id']}", style="bold cyan", characters="=")
    console.print(
        Columns(
            [
                printContrat(contrat),
                templateClientStr(contrat['client']),
                templateUserStr(contrat['commercial_contact'])
            ],
            expand=True
        )
    )


def templateContratStr(contrat):
    data = (
        f"[bold cyan]Contrat :[/bold cyan]\n"
        f"  id : {contrat['id']}\n"
        f"  prix_ttl : {contrat['prix_ttl']}\n"
        f"  prix_restant : {contrat['prix_restant']}\n"
        f"  statut : {contrat['statut']}\n"
        f"  créé le {datetime.strptime(contrat['time_created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')}\n"
    )
    return data


@click.group(name='contrat')
def contrat():
    pass


@contrat.command()
def show():
    console = Console()
    conf = initConfig()
    response = myRequests("get", conf['url']+'api/contrats/all/', headers=conf["headers"])
    if not response:
        return False
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule("[red]0 contrat trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} contrats trouvés[/green]", style="bold green", characters="=")
            console.print('\n')
            parcoursList(console, templateContrats, reponseJson)
            console.print('\n')
            console.rule(style="bold green", characters="=")


@contrat.command()
def showFilter():
    console = Console()
    conf = initConfig()
    response = myRequests("get", conf['url']+'api/contrats/', headers=conf["headers"])
    if not response:
        return False
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule("[red]0 contrat trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} contrats trouvés[/green]", style="bold green", characters="=")
            console.print('\n')
            parcoursList(console, templateContrats, reponseJson)
            console.print('\n')
            console.rule(style="bold green", characters="=")


@contrat.command()
@click.option('--client_id', required=False)
@click.option('--first_name', required=False)
@click.option('--last_name', required=False)
@click.option('--entreprise', required=False)
@click.argument('prix_ttl', required=False)
@click.argument('prix_restant', required=False)
@click.argument('statut', required=False)
def create(
    client_id=None,
    first_name=None,
    last_name=None,
    entreprise=None,
    prix_ttl=None,
    prix_restant=None,
    statut=None
):
    data = {}
    data = optionData(
        data,
        client_id,
        'client_id',
        "entrez l'id du client si vous le connaissez sinon apuuyez sur 'entrer' "
    )
    if "client_id" not in data:
        data = argumentData(data, first_name, 'first_name', "entrez le prenom du client ")
        data = argumentData(data, last_name, 'last_name', "entrez le nom du client ")
        data = argumentData(data, entreprise, 'entreprise', "entrez l'entreprise du client ")
    data = argumentData(data, prix_ttl, 'prix_ttl', "entrez le prix total du contrat ")
    data = argumentData(data, prix_restant, 'prix_restant', "entrez le prix restant à payer par le client du contrat ")
    data = argumentData(data, statut, 'statut', "entrez '1' si le contrat est signé ou '0' s'il ne l'est pas ")
    conf = initConfig()
    response = myRequests("post", conf['url']+'api/contrats/', headers=conf["headers"], data=data)
    if not response:
        return False
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 201:
            console = Console()
            console.rule("[green]Contrat créé avec succes ![green]", style="bold green", characters="=")
            templateContrat(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")


@contrat.command()
@click.argument('id', required=False)
@click.option('--prix_ttl')
@click.option('--prix_restant')
@click.option('--statut')
def change(id=None, prix_ttl=None, prix_restant=None, statut=None):
    dataUrl = argumentData({}, id, 'id', "id du client dont vous voulez modifier les données")
    print(
        "[bold cyan]Toutes les option laissez vide lors de l'appel vont vous etre demandé, "
        "veuillez ne rien rentrer si vous ne voulez pas les modifier[/bold cyan]"
    )
    waitUser()
    data = {}
    data = optionData(data, prix_ttl, 'prix_ttl', "entrez le prix total du contrat ")
    data = optionData(data, prix_restant, 'prix_restant', "entrez le prix restant à payer par le client du contrat ")
    data = optionData(data, statut, 'statut', "entrez '1' si le contrat est signé ou '0' s'il ne l'est pas ")
    if data == {}:
        print("[bold red]Vous n'avez rien changer au contrat[/bold red]")
        return None
    conf = initConfig()
    response = myRequests("put", conf['url']+'api/contrats/'+dataUrl['id']+'/', headers=conf["headers"], data=data)
    if not response:
        return False
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 200:
            console = Console()
            console.rule("[green]Contrat modifié avec succes ![green]", style="bold green", characters="=")
            templateContrat(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")
