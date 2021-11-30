# -*- coding: utf-8 -*-
import mysql.connector


def insert_product(
    name, novascore, nutriscore, url, brands_ids, stores_ids, categories_ids, cursor
):
    cursor.execute(
        "INSERT INTO product (name, novascore, nutriscore, url)"
        "VALUES (%s, %s, %s, %s) ;",
        (name, novascore, nutriscore, url),
    )
    product_id = cursor.lastrowid
    for brand_id in brands_ids:
        cursor.execute(
            "INSERT INTO product_brand (product_id, brand_id) VALUES (%s, %s);",
            (product_id, brand_id),
        )
    for store_id in stores_ids:
        cursor.execute(
            "INSERT INTO product_store (product_id, store_id) VALUES (%s, %s);",
            (product_id, store_id),
        )
    for category_id in categories_ids:
        cursor.execute(
            "INSERT INTO product_category (product_id, category_id) VALUES (%s, %s);",
            (product_id, category_id),
        )
    return product_id


def insert_categories(names, cursor):
    ids = []
    for name in names:
        ids.append(insert_category(name, cursor))
    return ids


def insert_category(name, cursor):
    query = "SELECT id FROM category WHERE name=(%s);"
    cursor.execute(query, (name,))
    response = cursor.fetchone()
    if response:
        return response[0]
    cursor.execute("INSERT INTO category (name) VALUES (%s);", (name,))
    return cursor.lastrowid


def insert_brands(names, cursor):
    ids = []
    try:
        for name in names:
            ids.append(insert_brand(name, cursor))
    except:
        print("insertion impossible")
    return ids


def insert_brand(name, cursor):
    query = "SELECT id FROM brand where name=(%s);"
    cursor.execute(query, (name,))
    response = cursor.fetchone()
    if response:
        return response[0]
    cursor.execute("INSERT INTO brand (name) VALUES (%s);", (name,))
    return cursor.lastrowid


def insert_stores(names, cursor):
    ids = []
    try:
        for name in names:
            ids.append(insert_store(name, cursor))
    except:
        print("insertion impossible")
    return ids


def insert_store(name, cursor):
    query = "SELECT id FROM store WHERE name=(%s);"
    cursor.execute(query, (name,))
    response = cursor.fetchone()
    if response:
        return response[0]
    cursor.execute("INSERT INTO store (name) VALUES (%s);", (name,))
    return cursor.lastrowid


def get_all_categories(cursor):
    # On return un tableau d'id
    query = "SELECT id, name FROM category LIMIT 50;"
    cursor.execute(query)
    return [(category[0], category[1]) for category in cursor.fetchall()]


def products_categories(category_id, cursor):
    # Cette fonction return tout les produits d'une category
    query = "SELECT p.id, p.name from product p inner join product_category cp on p.id = cp.product_id where cp.category_id = (%s);"
    cursor.execute(query, (category_id,))
    return cursor.fetchall()


def get_name_of_product(cursor):
    query = "SELECT name FROM product;"
    cursor.execute(query)
    return cursor.fetchall()


def get_product_by_name(name, cursor):
    query = "SELECT DISTINCT id, name FROM product WHERE name like %s LIMIT 10;"
    cursor.execute(query, (f"%{name}%",))
    return cursor.fetchall()


def get_all_information(product_id, cursor):
    get_information = "SELECT * FROM product WHERE id = %s;"
    cursor.execute(get_information, (product_id,))
    return cursor.fetchone()


def get_substitute(cursor, product_id):
    # On récupere le nutriscore et novascore du product_id
    product_info = get_all_information(product_id, cursor)
    product_nutri = product_info[3]
    product_nova = product_info[4]

    # On récupère les categories du produit

    categories = get_categories_for_product(product_id, cursor)

    # On récupére les produits qui sont dans les categories de la variable categories

    query = "SELECT DISTINCT p.id, p.name FROM product AS p INNER JOIN product_category as pc ON p.id = pc.product_id WHERE p.novascore < %s AND p.nutriscore > %s AND pc.category_id IN ({}) LIMIT 10;".format(
        ",".join(["%s"] * len(categories))
    )
    cursor.execute(query, (product_nova, product_nutri, *categories))
    return cursor.fetchall()


def get_categories_for_product(product_id, cursor):
    # On va recuperer la liste de categories du product_id
    get_list = "SELECT category_id from product_category WHERE product_id = %s;"
    cursor.execute(get_list, (product_id,))
    return [category[0] for category in cursor.fetchall()]


def saved_substitut(cursor, cnx, substitut_id, product_id):
    # On sauvegarde le substitut dans la base de donnée
    query = "UPDATE product SET substitut_id = %s WHERE id = %s;"
    cursor.execute(query, (substitut_id, product_id))
    cnx.commit()


def get_all_substituts(cursor):
    # On effectue une requête pour sélectionner le nom et l'id du produit et de son substitut.

    query = "SELECT p.id, p.name, s.id, s.name from product AS p inner join product AS s ON s.id = p.substitut_id;"
    cursor.execute(query)
    return cursor.fetchall()