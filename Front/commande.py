from rich import print
import click
import keyboard
import configparser
import requests


def initConfig():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    url = config.get('api', 'url')
    token = config.get('api', 'token')
    headers = {'Authorization': f'Bearer {token}', }
    return {'config': config, 'url': url, 'token': token, 'headers': headers}


def statusOK(response):
    if response.status_code == 401:
        print("[bold red]Vous n'êtes pas connecté a l'API[/bold red]")
        return False
    elif response.status_code == 403:
        print("[bold red]Vous n'avez pas les droits pour cette action[/bold red]")
        return False
    return True


def parcoursList(console, functionCall, listItem):
    here = functionCall(console, listItem, 0)
    while here < len(listItem):
        while keyboard.is_pressed('space'):
            pass
        key = keyboard.read_event(suppress=True)
        if key.name == "space":
            here = functionCall(console, listItem, here)
            console.print(title="Appuyez sur ESPACE pour afficher les éléments suivants ou Q pour quitter")
        else:
            here = len(listItem)


def argumentData(
    dataDict,
    data,
    nameData,
    promptData,
    optionData={},
    validate=False,
    dataValidate=None,
    promptValidate='',
    optionValidate={},
    notValidateText='',
    blank=False
):
    if blank:
        if 'default' not in optionData:
            optionData['default'] = ''
        if 'show_default' not in optionData:
            optionData['show_default'] = False
        if 'default' not in optionValidate:
            optionValidate['default'] = ''
        if 'show_default' not in optionValidate:
            optionValidate['show_default'] = False
    isNotValide = True
    while isNotValide:
        if not data:
            data = click.prompt(promptData, **optionData)
        if validate:
            if not dataValidate:
                dataValidate = click.prompt(promptValidate, **optionValidate)
            if data != dataValidate:
                if notValidateText:
                    print(notValidateText)
                data = None
                dataValidate = None
            else:
                isNotValide = False
        else:
            isNotValide = False
    dataDict[nameData] = data
    return dataDict


def optionData(
    dataDict,
    data,
    nameData,
    promptData,
    optionData={},
    validate=False,
    dataValidate=None,
    promptValidate='',
    optionValidate={},
    notValidateText=''
):
    if 'default' not in optionData:
        optionData['default'] = ''
    if 'show_default' not in optionData:
        optionData['show_default'] = False
    if 'default' not in optionValidate:
        optionValidate['default'] = ''
    if 'show_default' not in optionValidate:
        optionValidate['show_default'] = False
    if not data:
        data = click.prompt(promptData, **optionData)
    if not data:
        return dataDict
    if validate:
        if not dataValidate:
            dataValidate = click.prompt(promptValidate, **optionValidate)
        if data != dataValidate:
            if notValidateText:
                print(notValidateText)
            return dataDict
    dataDict[nameData] = data
    return dataDict


def waitUser():
    print("Appuiez sur n'importe quelle touche pour continuer...")
    c = True
    while c:
        keyboard.read_event(suppress=True)
        c = False


def myRequests(typeRequest, url, data={}, headers={}):
    if typeRequest == "get":
        try:
            return requests.get(url, headers=headers)
        except requests.exceptions.RequestException:
            print("[bold red] Impossible de joindre l'API[/bold red]")
            return False
    if typeRequest == "post":
        try:
            return requests.post(url, data=data, headers=headers)
        except requests.exceptions.RequestException:
            print("[bold red] Impossible de joindre l'API[/bold red]")
            return False
    if typeRequest == "put":
        try:
            return requests.put(url, data=data, headers=headers)
        except requests.exceptions.RequestException:
            print("[bold red] Impossible de joindre l'API[/bold red]")
            return False
    if typeRequest == "delete":
        try:
            return requests.delete(url, data=data, headers=headers)
        except requests.exceptions.RequestException:
            print("[bold red] Impossible de joindre l'API[/bold red]")
            return False
