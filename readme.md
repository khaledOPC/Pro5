#Introduction

L'objectif ici est de créer une base de données dans la quelle on va récupérer des données du site openfoodfacts et ainsi pouvoir les manipuler. On va trouver des substituts au produit qu'on import pour que les clients puissent choisir les produits les plus sains. Enfin ils auront le choix de les enregistrer ou non dans la base de données.
Tout cela est modélisé dans l'invite de commande par des scripts.
On va donc créer plusieurs scripts python dont un script sql
Les différents scripts vont contenir les différentes tables mysql

Liens github du projet 5 : https://github.com/khaledOPC/Pro5

# Environnement testé

- Windows10
- python3.8
- mysql


# Utilisation

- pip install python
- pip install mysql
- pip install requests
- pip install mysql.connector
- python main.py



# Paque

- windows10
- Système d'exploitation

# Utile à savoir

Le fichier import_off contient les requêtes pour importer les données depuis le site internet.
Le fichier database contient le script python avec les requêtes mysql.
Le fichier script modélise dans la console le fichier database en appelant les fonction et en formatent les données via des fonctions.

Pour lancer le code dans la console il faut se placer dans l'environnement virtuel et appeler le module openfoodfacts ou se trouve tout le code python et mysql comme ceci: C:\Users\khale\Desktop\Workspace\P5\env\scripts\activate: python -m openfoodfacts


La création d'un script SQL pour pouvoir manipuler la base de données à distance a été très importante "Schema.sql". Avec une ligne de code on peut facilement manipuler à notre guise la création ou non des tables de la base de donnée.

A lire dans la console mysql pour lancer le script 'Schema.sql': source C:/Users/khale/Desktop/Workspace/P5/openfoodfacts/Schema.sql;

Nous allons également utiliser une variable environnement pour masquer les identifiants de la BDD.

Sur windows la création d'une variable environnement à fin de masquer les identifiants de la base de données via la fonction OS.getenv(), se fait avec la commande : setx identifiant exemple : DB_PASSWORD = MOT_DE_PASSE. Il faut faire un import os dans les scripts concernés. 
