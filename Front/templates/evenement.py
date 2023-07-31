from rich import print
from rich.columns import Columns
from rich.console import Console
from datetime import datetime
import click
import requests
from commande import initConfig, statusOK, parcoursList, optionData, argumentData, waitUser
from templates.user import templateUserStr
from templates.client import templateClientStr
from templates.contrat import templateContratStr


def templateEvenements(console, listItem, here):
    end = min(here + 5, len(listItem))
    for i in range(here, end):
        evenement = listItem[i]
        console.rule(f"Evenement {evenement['id']}", style="bold cyan", characters="=")
        # checker si support existe et ajouter contrat str ainsi quer changer client en contrat.client
        if evenement['support_contact']:
            console.print(Columns([printEvenement(evenement), templateContratStr(evenement['contrat']),templateClientStr(evenement['client']), templateUserStr(evenement['support_contact'],1), templateUserStr(evenement['contrat']['commercial_contact'])], expand=True))
        else:
            console.print(Columns([printEvenement(evenement), templateContratStr(evenement['contrat']),templateClientStr(evenement['client']), templateUserStr(evenement['contrat']['commercial_contact'])], expand=True))
    return end

def printEvenement(evenement):
    data = (
        f"id : {evenement['id']}\n"
        f"nom : {evenement['nom']}\n"
        f"commence le {datetime.strptime(evenement['date_start'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y %H:%M')}\n"
        f"fini le {datetime.strptime(evenement['date_end'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y %H:%M')}\n"
        f"lieu : {evenement['location']}\n"
        f"nombre de personne attendu : {evenement['attende']}\n"
        f"note : {evenement['note']}\n"
    )
    return data


def templateEvenement(console, evenement):
    console.rule(f"Evenement {evenement['id']}", style="bold cyan", characters="=")
    if evenement['support_contact']:
        console.print(Columns([printEvenement(evenement), templateContratStr(evenement['contrat']),templateClientStr(evenement['client']), templateUserStr(evenement['support_contact'],1), templateUserStr(evenement['contrat']['commercial_contact'])], expand=True))
    else:
        console.print(Columns([printEvenement(evenement), templateContratStr(evenement['contrat']),templateClientStr(evenement['client']), templateUserStr(evenement['contrat']['commercial_contact'])], expand=True))

@click.group(name='evenement')
def evenement():
    pass


@evenement.command()
def show():
    console = Console()
    conf = initConfig()
    response = requests.get(conf['url']+'api/evenements/all/', headers=conf["headers"])
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule(f"[red]0 evenement trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} evenements trouvés[/green]", style="bold green", characters="=")
            console.print(f'\n')
            parcoursList(console, templateEvenements, reponseJson)
            console.print(f'\n')
            console.rule(style="bold green", characters="=")


@evenement.command()
def showFilter():
    console = Console()
    conf = initConfig()
    response = requests.get(conf['url']+'api/evenements/', headers=conf["headers"])
    if statusOK(response):
        reponseJson = response.json()
        if len(reponseJson) == 0:
            console.rule(f"[red]0 evenement trouvé[red]", style="bold red", characters="=")
        else:
            console.rule(f"[green]{len(reponseJson)} evenements trouvés[/green]", style="bold green", characters="=")
            console.print(f'\n')
            parcoursList(console, templateEvenements, reponseJson)
            console.print(f'\n')
            console.rule(style="bold green", characters="=")


@evenement.command()
@click.option('--client_id', required=False)
@click.option('--first_name', required=False)
@click.option('--last_name', required=False)
@click.option('--entreprise', required=False)
@click.argument('contrat_id', required=False)
@click.argument('nom', required=False)
@click.argument('date_start', required=False)
@click.argument('heure_start', required=False)
@click.argument('date_end', required=False)
@click.argument('heure_end', required=False)
@click.argument('location', required=False)
@click.argument('attende', required=False)
@click.argument('note', required=False)
def create(client_id=None, first_name=None, last_name=None, entreprise=None, contrat_id=None, nom=None, date_start=None, heure_start=None, date_end=None, heure_end=True, location=None, attende=None, note=None):
    data = {}
    data = optionData(data, client_id, 'client_id', "entrez l'id du client si vous le connaissez sinon apuuyez sur 'entrer' ")
    if not "client_id" in data:
        data = argumentData(data, first_name, 'first_name', "entrez le prenom du client ")
        data = argumentData(data, last_name, 'last_name', "entrez le nom du client ")
        data = argumentData(data, entreprise, 'entreprise', "entrez l'entreprise du client ")
    data = argumentData(data, contrat_id, 'contrat_id', "entrez l'id contrat qui va avec l'evenement ")
    data = argumentData(data, nom, 'nom', "entrez le nom de l'evenement ")
    user_timezone = pytz.timezone('Europe/Paris')
    while not 'date_start' in data:
        date = {}
        date = argumentData(date, date_start, 'date_start', "entrez la date de l'evenement (jj/mm/aaaa) ")
        date = argumentData(date, heure_start, 'heure_start', "entrez l'heure' de l'evenement (hh:mm) ")
        try:
            data['date_start'] = datetime.strptime(date['date_start']+date['heure_start'], "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone)
        except:
            print(f"[bold red] Erreur dans les données rentrer pour la date de strat{date['date_start']+date['heure_start']}. Exemple valide date : '21/8/2028' et heure : '15:30', veuillez recommencé[/bold red]")
    while not 'date_end' in data:
        date = {}
        date = argumentData(date, date_end, 'date_end', "entrez la date de l'evenement (jj/mm/aaaa) ")
        date = argumentData(date, heure_end, 'heure_end', "entrez l'heure' de l'evenement (hh:mm) ")
        try:
            data['date_end'] = datetime.strptime(date['date_end']+date['heure_end'], "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone)
        except:
            print(f"[bold red] Erreur dans les données rentrer pour la date de strat{date['date_end']+date['heure_end']}. Exemple valide date : '21/8/2028' et heure : '15:30', veuillez recommencé[/bold red]")
    data = argumentData(data, location, 'location', "entrez le lieu de l'evenement ")
    data = argumentData(data, attende, 'attende', "entrez le nombre de personne attendu à l'evenement ")
    data = argumentData(data, note, 'note', "entrez les notes, au besoin, sur l'evenement ")
    conf = initConfig()
    response = requests.post(conf['url']+'api/evenements/', headers=conf["headers"], data=data)
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 201:
            console = Console()
            console.rule(f"[green]Evenement créé avec succes ![green]", style="bold green", characters="=")
            templateEvenement(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")


@evenement.command()
@click.argument('id',required=False)
@click.option('--nom')
@click.option('--support_email')
@click.option('--date_start')
@click.option('--heure_start')
@click.option('--date_end')
@click.option('--heure_end')
@click.option('--location')
@click.option('--attende')
@click.option('--note')
def change(id=None, nom=None, support_email=None, date_start=None, heure_start=None, date_end=None, heure_end=None, location=None, attende=None, note=None):
    dataUrl = argumentData({}, id,'id',"id de l'evenement dont vous voulez modifier les données")
    qui = click.prompt("Etes vous de l'equipe gestion ('GE') ou support ('SU') ?")
    print("[bold cyan]Toutes les option laissez vide lors de l'appel vont vous etre demandé, veuillez ne rien rentrer si vous ne voulez pas les modifier[/bold cyan]")
    waitUser()
    data = {}
    if qui == 'SU':
        data = optionData(data, nom, 'nom', "entrez le nom de l'evenement ")
        date = {}
        date = optionData(date, date_start, 'date_start', "entrez la date de l'evenement (jj/mm/aaaa) ")
        date = optionData(date, heure_start, 'heure_start', "entrez l'heure' de l'evenement (hh:mm) ")
        if date:
            user_timezone = pytz.timezone('Europe/Paris')
            try:
                data['date_start'] = datetime.strptime(date['date_start']+date['heure_start'], "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone)
            except:
                print(f"[bold red] Erreur dans les données rentrer pour la date de strat{date['date_start']+date['heure_start']}. Exemple valide date : '21/8/2028' et heure : '15:30', veuillez recommencé[/bold red]")
        date = {}
        date = optionData(date, date_end, 'date_end', "entrez la date de l'evenement (jj/mm/aaaa) ")
        date = optionData(date, heure_end, 'heure_end', "entrez l'heure' de l'evenement (hh:mm) ")
        if date:
            user_timezone = pytz.timezone('Europe/Paris')
            try:
                data['date_end'] = datetime.strptime(date['date_end']+date['heure_end'], "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone)
            except:
                print(f"[bold red] Erreur dans les données rentrer pour la date de strat{date['date_end']+date['heure_end']}. Exemple valide date : '21/8/2028' et heure : '15:30', veuillez recommencé[/bold red]")
        data = optionData(data, location, 'location', "entrez le lieu de l'evenement ")
        data = optionData(data, attende, 'attende', "entrez le nombre de personne attendu à l'evenement ")
        data = optionData(data, note, 'note', "entrez les notes, au besoin, sur l'evenement ")
    elif qui == 'GE':
        data = optionData(data, support_email, 'support_email', "entrez l'email du compte support")
    else:
        print(f"[bold red]Vous n'avez pas ecrit une reponse que je connais ('GE' ou 'SU')[/bold red]")
        return None
    if data == {}:
        print(f"[bold red]Vous n'avez rien changer a l'evenement[/bold red]")
        return None
    conf = initConfig()
    response = requests.put(conf['url']+'api/evenements/'+dataUrl['id']+'/', headers=conf["headers"], data=data)
    if statusOK(response):
        reponseJson = response.json()
        if response.status_code == 200:
            console = Console()
            console.rule(f"[green]Evenement modifié avec succes ![green]", style="bold green", characters="=")
            templateEvenement(console, reponseJson)
            console.rule(style="bold green", characters="=")
        else:
            print(f"[bold red]{reponseJson['error']}[/bold red]")
