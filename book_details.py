import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
from urllib.parse import urljoin
import re

DETAILS_DIR = "Books_details"


def data_to_save_to_csv(filename, dico_infos, mode):
    # Generation d'un Timestamp
    # current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    # Nom du fichier CSV a horodater
    os.makedirs(DETAILS_DIR, exist_ok=True)
    output_filename = os.path.join(DETAILS_DIR, filename + ".csv")
    
    # On vérifie si le fichier existe déjà
    file_exists = os.path.isfile(output_filename)

    with open(output_filename, mode, newline="", encoding="utf-8") as output_csv:
        fieldnames = dico_infos.keys()    # Les clefs en titre de colonnes
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        if not file_exists:    # Si le fichier n'a pas encore été créé, on y ecrit les titres de colonnes
            writer.writeheader()
        writer.writerow(dico_infos)


def test_acces_page(url):
    # On verifie que la page est accessible 
    response = requests.get(url)
    print(f"{url} -> {response.status_code}")

    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    print(f"ERREUR : impossible d'accéder à {url}")
    return None


def main(url_book, filename):
    # Par defaut, livre = 'a light in the attic'
    soup = test_acces_page(url_book)
    if soup is None:
        print(f"Pas de données pour : {url_book}")
        return
        
    # La plupart des données du livre se trouve dans le tableau <table>
    table = soup.find("table", class_="table table-striped")

    # Les informations trouvées seront ajoutées dans un dictionnaire
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
    if header_product_description:
        product_description = header_product_description.find_next("p")
        #dico_infos["product_description"] = product_description.get_text(strip=True)
        dico_infos["product_description"] = "Recup Description commentée pour accelerer le processus"
    else:
        dico_infos["product_description"] = "No description found !!"

    # La catégorie du livre se trouve dans le tag <ul> de classe "breadcrumb"
    ul = soup.find("ul", class_="breadcrumb")
    for li in ul.find_all("li"):
        a_category = li.find("a")
        if a_category:
            # je cherche un lien qui n'est ni le repertoire 'Home' ni son sous repertoire 'Books' 
            if a_category.string.lower() == "home" or a_category.string.lower() == "books":
                continue
            else:
                category = li.find("a").text
                dico_infos["category"] = category

    # Recuperation du nb d'etoiles (review_rating)
    star_rating = soup.find("i", class_="icon-star").find_parent("p")
    review_rating = star_rating.get("class")
    nb_stars_en = review_rating[1].lower()    # La classe extraite est une liste

    # Conversion des notations string en numerique
    nb_stars = {"one":1, "two": 2, "three": 3, "four": 4, "five": 5}
    nb_stars_fr = nb_stars[nb_stars_en]
    dico_infos["review_rating"] = nb_stars_fr
    
    # Conversion de l'url de l'image en adresse absolue
    image_url = soup.find(id="product_gallery").find("img").get("src")
    src_image = image_url.split('../')[2]
    image_url = urljoin('https://books.toscrape.com/', src_image)
    dico_infos["image_url"] = image_url
    
    # On reformate le titre pour supprimer les caracteres interdits ainsi que les blancs
    safe_title = re.sub(r"[\\/:*?\"'(),.#@+&~=<>|\s]+", "_", title).strip("_")
    # On conserve uniquement les 15 premiers caracteres du titre
    filename = filename + (safe_title)[:25] + "_"

    data_to_save_to_csv(filename, dico_infos, "a")

    # Recuperation de l'image et sauvegarde dans le meme dossier que les 'csv'
    response = requests.get(image_url)
    response.raise_for_status()
    jpg_filename = DETAILS_DIR + "/" + filename + '.jpg'
    with open(jpg_filename, "wb") as image_file:
        image_file.write(response.content)


#================== Main script ===================

if __name__ == "__main__":
    url_book = "https://books.toscrape.com/catalogue/the-argonauts_837/index.html"
    main(url_book, "details_")
