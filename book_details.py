import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
from urllib.parse import urljoin

def data_to_save_to_csv(filename, dico_infos, mode):
    # Generation du Timestamp
    current_date_time = datetime.now().strftime("%Y%m%d_%H%M")

    # Nom du fichier CSV a horodater
    output_filename = filename + current_date_time + ".csv"
    
    # Vérifie si le fichier existe déjà
    file_exists = os.path.isfile(output_filename)

    with open(output_filename, mode, newline="", encoding="utf-8") as output_csv:
        # Les clefs en titre de colonnes
        fieldnames = dico_infos.keys()
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        # Si le fichier n'a pas encore été créé, on ecrit les titres de colonnes
        if not file_exists:
            writer.writeheader()
        writer.writerow(dico_infos)

def acces_page(url):
    response = requests.get(url)
    print(f"{url} -> {response.status_code}")

    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    print(f"ERREUR : impossible d'accéder à {url}")
    return None


def main(url_book, filename):
    soup = acces_page(url_book)
    if soup is None:
        print(f"Pas de données pour : {url_book}")
        return
        
    # la plupart des données du livre se trouve dans le tableau <table>
    table = soup.find("table", class_="table table-striped")

    # les informations trouvées seront ajoutées dans un dictionnaire
    dico_infos = {}
    dico_infos["product_page_url"] = url_book

    # On boucle sur les lignes <tr> et <th> du tableau. Si le contenu <th> match le motif
    # alors on copie le texte <td> correspondant dans le dico
    currency = "£"
    for tr in table.find_all("tr"):
        for th in tr.find_all("th"):
            if th.text.lower() == "upc":
                dico_infos[th.text] = tr.find("td").get_text(strip=True)
            if th.text.lower() == "price (incl. tax)":
                raw_taxed_price = tr.find("td").get_text(strip=True)
                taxed_price = raw_taxed_price.split(currency)[1] + currency
                dico_infos[th.text] = taxed_price
            if th.text.lower() == "price (excl. tax)":
                raw_free_price = tr.find("td").get_text(strip=True)
                free_price = raw_free_price.split(currency)[1] + currency
                dico_infos[th.text] = free_price
            if th.text.lower() == "tax":
                raw_tax = tr.find("td").get_text(strip=True)
                tax = raw_tax.split(currency)[1] + currency
                dico_infos[th.text] = tax
            if th.text.lower() == "availability":
                raw_availibility = tr.find("td").get_text(strip=True)
                availibility = (raw_availibility.split("(")[1]).split(" ")[0]
                dico_infos[th.text] = availibility

    # Le titre du livre se trouve dans le tag <h1> qui est contenu dans un <div> de classe "col-sm-6 product_main"
    title = soup.find("div", class_="col-sm-6 product_main").find("h1").text
    dico_infos["title"] = title

    # La description du livre se trouve dans le tag <p> qui suit le <h2> "Product Description"
    header_product_description = soup.find("h2", string="Product Description")
    product_description = header_product_description.find_next("p")
    dico_infos["product_description"] = product_description.text

    # La catégorie du livre se trouve dans le tag <ul> de classe "breadcrumb"
    ul = soup.find("ul", class_="breadcrumb")
    for li in ul.find_all("li"):
        a = li.find("a")
        if a:
            if a.string.lower() == "home" or a.string.lower() == "books":
                continue
            else:
                category = li.find("a").text
                dico_infos["category"] = category

    # Recuperation du nb d'etoiles (review_rating)
    star_rating = soup.find("i", class_="icon-star").find_parent("p")
    review_rating = star_rating.get("class")
    # La classe extraite est une liste
    nb_stars_en = review_rating[1].lower()
    # Conversion des notations string en numerique
    nb_stars = {"one":1, "two": 2, "three": 3, "four": 4, "five": 5}
    nb_stars_fr = nb_stars[nb_stars_en]
    dico_infos["review_rating"] = nb_stars_fr
    
    # L'url de l'image
    image_url = soup.find(id="product_gallery").find("img").get("src")
    src_image = image_url.split('../')[2]
    image_url = urljoin('https://books.toscrape.com/', src_image)
    dico_infos["image_url"] = image_url
    
    print(dico_infos, "\n")
    data_to_save_to_csv(filename, dico_infos, "a")

#================== Main script ===================

if __name__ == "__main__":
    url_book = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    main(url_book, "book_detail_")

