import mysql.connector
import os
import sys
from openfoodfacts.Import_off import main as main_import
from openfoodfacts.Database import (
    get_all_categories,
    products_categories,
    get_all_information,
    get_product_by_name,
    get_substitute,
    saved_substitut,
    get_all_substituts,
)

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="pur_beurre_travaille",
)


def menu():
    cursor = cnx.cursor()
    choices = [
        "1 Rechercher un produit par categorie",
        "2 Rechercher un produit par son nom",
        "3 Afficher ses substitus",
    ]
    for name in choices:
        print(name)
    name = input("Entrez votre choix")
    if name == "1":
        list_categories(cursor)
    elif name == "2":
        product_by_name(cursor)
    elif name == "3":
        saved_substituts(cursor)
    else:
        print("Option invalide")


def list_categories(cursor):
    categories = get_all_categories(cursor)
    print("Voici les différentes categories :")
    print("")
    # On affiche les categories.
    for category in categories:
        print("ID :", category[0], "NAME :", category[1])

    category_id = input("Entrez l'id de la categorie :")
    print(f"Vous avez choisis la categorie {category_id}")
    print("")
    product_by_category(category_id, cursor)


def product_by_category(category_id, cursor):
    products_by_categories = products_categories(category_id, cursor)

    if products_by_categories:
        for product in products_by_categories:
            print("ID :", product[0], "NAME :", product[1])
    else:
        print("Il n'y a pas de produit disponible")
        print("Essayez avec une autre categorie ou un autre produit")
        print("")
        menu()

    product_id = input("Choisissez un produits à substituer : ")
    print(f"Vous souhaitez substituer le produit suivant : {product_id}")
    print("")
    substitute_of_product = get_substitute(cursor, product_id)
    information_of_product = get_all_information(product_id, cursor)
    print("Voici les informations du produits : ")
    print("")
    print("ID :", information_of_product[0])
    print("URL :", information_of_product[1])
    print("NAME :", information_of_product[2])
    print("NUTRISCORE :", information_of_product[3])
    print("NOVASCORE:", information_of_product[4])
    print("")
    print("Voici les substituts du produits choisis : ")
    if substitute_of_product:
        for substitut in substitute_of_product:
            print("ID :", substitut[0], "NOM :", substitut[1])

    else:
        print("Le produit n'a pas de substitut ")
        print("Essayer avec un autre produit : ")
        menu()

    print("")
    substitut_id = input("quel substitut souhaitez vous enregistrer :")
    print(f"Vous souhaitez enregistrer le produit : {substitut_id}", "comme substitut")
    print("")
    save_substitut = saved_substitut(cursor, cnx, substitut_id, product_id)
    saved_substituts(cursor)


def product_by_name(cursor):

    # Ici on va afficher le produit demandé.

    name = input("Choisissez un produit à rechercher ")
    product_name = get_product_by_name(name, cursor)
    print("")
    print(f"Voici les produits qui contiennent le nom : {name}")

    for name in product_name:
        print("ID :", name[0], "NOM :", name[1])

    product_id = input("Choisissez un produits à substituer ")
    product_information(product_id, cursor)


def product_information(product_id, cursor):

    # On récupère les informations du produit.

    products_informations = get_all_information(product_id, cursor)
    substitute = get_substitute(cursor, product_id)
    print("")
    print("Voici les informations du produit : ")
    print("")
    print("ID :", products_informations[0])
    print("URL :", products_informations[1])
    print("NAME :", products_informations[2])
    print("NUTRISCORE :", products_informations[3])
    print("NOVASCORE:", products_informations[4])
    print("")
    # On affiche les substituts du produit.
    print("Les substitut du  produit sont : ")
    if substitute:
        for substitut in substitute:
            print("ID :", substitut[0], "NOM :", substitut[1])

    else:
        print("Le produit n'a pas de substitut ")
        print("Essayer avec un autre produit : ")
        menu()

    print("")
    substitut_id = input("quel substitut souhaitez vous enregistrer :")
    print(f"Vous souhaitez enregistrer le produit : {substitut_id}", "comme substitut")
    print("")
    save_substitut = saved_substitut(cursor, cnx, substitut_id, product_id)
    saved_substituts(cursor)
    # On enregistre le substitut souhaité.


def saved_substituts(cursor):
    products = get_all_substituts(cursor)
    print("Voici les produits sauvegardés : ")
    for product in products:
        print(
            " Le produit : ",
            product[0],
            product[1],
            "à pour substitut le produit :",
            product[2],
            product[3],
        )
    print("")
    main()


def main():
    print("1 : Import de donné")
    print("2 : Lancer le script")
    print("3 : Quitter le programme")
    response = input("Choix : ")
    if response == "1":
        main_import()
    elif response == "2":
        menu()
    else:
        sys.exit()