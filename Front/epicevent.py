from rich import print
import click
import requests
from templates import user, client, contrat, evenement
from commande import initConfig
# import templates

@click.group()
def cli():
    pass

@cli.command()
@click.argument('email', required=False)
def login(email=None):
    if not email:
        email = click.prompt('entrez votre email ')
    password = click.prompt('entrez votre mot de passe ', hide_input=True)
    data = {
        'email':email,
        'password':password,
    }
    conf = initConfig()
    response = requests.post(conf['url']+'api/login/', data=data)
    if response.status_code == 200:
        reponseJson = response.json()
        conf['config'].set('api', 'token', reponseJson['access'])
        with open('config.cfg', 'w') as configfile:
            conf['config'].write(configfile)
        print(f"[bold green]Succès ! Tu es connecté avec l'email : {email}[/bold green]")
    else:
        print("[bold red]Erreur dans l'email ou le mot de passe[/bold red]")

@cli.command()
def logout():
    conf = initConfig()
    conf['config'].set('api', 'token', '')
    with open('config.cfg', 'w') as configfile:
        conf['config'].write(configfile)
    print(f"[bold green]Vous etes deconnecté[/bold green]")


cli.add_command(user.user)
cli.add_command(client.client)
cli.add_command(contrat.contrat)
cli.add_command(evenement.evenement)


if __name__ == '__main__':
    cli()