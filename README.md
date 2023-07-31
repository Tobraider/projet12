Ce projet est un CRM pour epicEvent

Cette appli est composé d'une partie front-end (Front) et back-end (Back)

Le Back est une API djangoREST qui utilise en base de données MySQL

Le Front quand a lui est une appli en CLI qui utilise rich et click

Vous n'avez pas besoin des deux sur toute vos machine. Vous pouvez garder seulement le dossier que vous souhaitez selon ce que vous voulez installer

BACK

Pour mettre en place le Back les actions sont les suivantes :

1. Aller dans le dossier epicEvent 

    `cd epicEvent`

2. Creer et initialiser l'environnement virtuel

    Windows :

        python -m venv env

        .\env\Scripts\activate

        pip install -r ./requirements.txt

    
    Linux :

        python3 -m venv env

        source env/bin/activate

        pip install -r ../requirements.txt

3. Configurez l'environnement pour la connexion à la base de données

    Veuillez ajouter un fichier .env dans le dossiers epicEvent ou alors les rentrer directement dans les variable d'environnement. Les variables à ajouter sont les suivantes :

        - DATABASE_ENGINE=enginDeVotreBDD
        - DATABASE_NAME=nameDeVotreDatabase
        - DATABASE_USER=userDeVotreDatabasePourLAppli
        - DATABASE_PASSWORD=passwordDeVotreUser
        - DATABASE_HOST=dnsDeVotreBDD
        - DATABASE_PORT=portDeVotreBDD
    


4. Lancer le serveur

    Windows :

        python manage.py runserver

    Linux :
        
        python3 manage.py runserver


FRONT

Pour mettre en place le Front les actions sont les suivantes :

1. Creer et initialiser l'environnement virtuel

    Windows :

        python -m venv env

        .\env\Scripts\activate

        pip install -r ./requirements.txt

    
    Linux :

        python3 -m venv env

        source env/bin/activate

        pip install -r ../requirements.txt


3. Executer les differente action possible :

    Windows : 

        python epicevent.py [nomDeLaction]
    
    Exemple pour se connecté : 
    
        python epicevent.py login

    Linux : 

        python3 epicevent.py [nomDeLaction]
    
    Exemple pour se connecté : 
    
        python3 epicevent.py login

Pour en savoir plus sur les commandes possible il suffit d'ecrire les commandes incomplete.

Exemple windows :

    python epicevent.py

Exemple linux :

    python3 epicevent.py