#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import mysql.connector
import os
from openfoodfacts.Constant import MAX_NB_CATEGORIES
from openfoodfacts.Database import (
    insert_product,
    insert_categories,
    insert_stores,
    insert_brands,
)


def main():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="pur_beurre_travaille",
    )
    cursor = cnx.cursor()

    url = "https://fr.openfoodfacts.org/categories.json"
    response = requests.get(url)

    if response.ok:
        response_json = response.json()
        for category_dict in response_json["tags"][:MAX_NB_CATEGORIES]:
            category_id = category_dict["id"][3:]
            payload = {
                "tag_0": category_id,
                "tag_contains_0": "contains",
                "page_size": 100,
                "tagtype_0": "categories",
                "json": "true",
                "action": "process",
            }
            response = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl", params=payload
            )
            if response.ok:
                products = response.json()["products"]
                for product in products:
                    product_name_fr = product.get("product_name_fr", "")
                    store_names = product.get("stores_tags")
                    novascore = product.get("nova_groups")
                    nutriscore = product.get("nutriscore_grade")
                    url = product.get("url")
                    brands_tags = product.get("brands_tags")
                    categories_hierarchy = product.get("categories_hierarchy")
                    stores_ids = insert_stores(store_names, cursor)
                    categories_ids = insert_categories(categories_hierarchy, cursor)
                    brands_ids = insert_brands(brands_tags, cursor)
                    print("On incère le produit : " + product_name_fr)
                    try:
                        if product_name_fr:
                            insert_product(
                                name=product_name_fr,
                                novascore=novascore,
                                nutriscore=nutriscore,
                                url=url,
                                brands_ids=brands_ids,
                                stores_ids=stores_ids,
                                categories_ids=categories_ids,
                                cursor=cursor,
                            )
                    except:
                        print("INSERTION IPOSSIBLE")

    cnx.commit()
    cnx.close()