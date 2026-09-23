import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
from urllib.parse import urljoin
import re

DETAILS_DIR = "Books_details"     # Nom attribué au repertoire contenant les CSV des caracteristiques des livres

def save_book_data_to_csv(filename, dico_infos, mode):   
    # Creation du repertoire et modele des noms de fichiers
    os.makedirs(DETAILS_DIR, exist_ok=True)
    path_output_filename = os.path.join(DETAILS_DIR, filename + ".csv")
    
    # Si le fichier CSV n'a pas encore été créé, la 1ere fois on y ecrit les titres de colonnes
    file_exists = os.path.isfile(path_output_filename)

    with open(path_output_filename, mode, newline="", encoding="utf-8") as output_csv:
        fieldnames = dico_infos.keys()    # Les clefs du dico en titre de colonnes
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(dico_infos)


def test_page_access(url):
    # On verifie que la page est accessible 
    response = requests.get(url)
    print(f"{url} -> {response.status_code}")

    if response.status_code == 200:
        return response
    print(f"ERREUR : impossible d'accéder à {url}")
    return None


def main(book_url, filename):
    response = test_page_access(book_url)
    if response is None:
        print(f"Pas de données pour : {book_url}")
        return
    soup = BeautifulSoup(response.text, "html.parser")
        
    # La plupart des données relatives livre se trouve dans le tableau <table>
    table = soup.find("table", class_="table table-striped")

    # Les informations trouvées sont ajoutées dans un dictionnaire
    dico_infos = {}
    dico_infos["product_page_url"] = book_url

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
    h2_product_description = soup.find("h2", string="Product Description")
    if h2_product_description:
        product_description = h2_product_description.find_next("p")
        dico_infos["product_description"] = product_description.get_text(strip=True)
    else:
        dico_infos["product_description"] = "No description found !!"

    # La catégorie du livre se trouve dans un tag <li> dans le tag <ul> de classe "breadcrumb"
    ul_breadcrumb = soup.find("ul", class_="breadcrumb")
    for li in ul_breadcrumb.find_all("li"):
        a = li.find("a")
        if a:
            # Je cherche un lien qui n'est ni le repertoire 'Home' ni son sous repertoire 'Books' 
            if a.string.lower() == "home" or a.string.lower() == "books":
                continue
            else:
                book_category = li.find("a").text
                dico_infos["category"] = book_category

    # Recuperation du nb d'etoiles (review_rating)
    star_rating = soup.find("i", class_="icon-star").find_parent("p")
    review_rating = star_rating.get("class")
    nb_stars_en = review_rating[1].lower()    # La classe extraite est une liste

    # Conversion des notations string en numerique
    nb_stars = {"one":1, "two": 2, "three": 3, "four": 4, "five": 5}
    nb_stars_fr = nb_stars[nb_stars_en]
    dico_infos["review_rating"] = nb_stars_fr
    
    # Conversion de l'url de l'image trouvee en url absolue
    image_url = soup.find(id="product_gallery").find("img").get("src")
    src_image = image_url.split('../')[2]
    image_url = urljoin('https://books.toscrape.com/', src_image)
    dico_infos["image_url"] = image_url
    
    # On utilise le titre du livre reformaté pour le nom de fichier 'csv'
    # On accepte uniquement les caractères alphanumériques ASCII. Tous les autres caractères sont remplacés par "_"
    safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", title).strip("_")
    filename = filename + (safe_title)[:25] + "_"     # 25 premiers caracteres du titre seulement
    save_book_data_to_csv(filename, dico_infos, "a")

    # Recuperation de l'image et sauvegarde dans le meme dossier que les 'csv'
    response = test_page_access(image_url)
    if response is None:
        print(f"Pas de données pour : {image_url}")
        return
    path_jpg_filename = DETAILS_DIR + "/" + filename + '.jpg'
    with open(path_jpg_filename, "wb") as image_file:
        image_file.write(response.content)


#================== Main script ===================

if __name__ == "__main__":
    book_url = "https://books.toscrape.com/catalogue/the-argonauts_837/index.html"
    main(book_url, "details_")
