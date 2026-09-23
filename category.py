from bs4 import BeautifulSoup
import book_details
from urllib.parse import urljoin
import os
import csv

# Repertoire du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def books_href_extract(soup, one_category_books_href_list):
    # On extrait l'URL de chaque livre de la catégorie dans la <div> "image_container"
    ol = soup.find("ol", class_="row")
    for li in ol.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        image_container_href = li.find("div", class_="image_container").find("a").get("href")
        image_container_href = image_container_href.split('../')[3]    # on supprime les '../' pour adresser l'url absolue
        book_url = urljoin('https://books.toscrape.com/catalogue/', image_container_href)
        one_category_books_href_list.append(book_url)


def find_next_page_url(soup, category_page_href):
    # On verifie la presence de la classe 'pager'
    ul_pager = soup.find("ul", class_="pager")
    if ul_pager == None:
        return False

    # Si on y trouve un bouton 'next', on recupere l'url de la page suivante
    li_next = ul_pager.find("li", class_="next")
    if li_next:
        href_page = li_next.find("a").get("href")
        return urljoin(category_page_href, href_page)  # Combinaison des 2 urls pour remplacer la page courante
    return False    # Si pas de bouton 'next' trouve, alors on retourne False


def save_category_href_to_csv(filename, one_category_books_href_list, mode):   
    # Creation du repertoire et modele des noms de fichiers
    os.makedirs(book_details.DETAILS_DIR, exist_ok=True)
    path_output_filename = os.path.join(book_details.DETAILS_DIR, filename + ".csv")

    with open(path_output_filename, mode, newline="", encoding="utf-8") as output_csv:
        writer = csv.writer(output_csv, delimiter=",")
        writer.writerow(one_category_books_href_list)

def main(category_page_href):
    # On verifie l'acces à la page de la catégorie
    response = book_details.test_page_access(category_page_href)
    if response is None:
        print(f"Pas de données pour : {category_page_href}")
        return
    soup = BeautifulSoup(response.text, "html.parser")

    one_category_books_href_list = []    # liste des url des livres pour une categorie
    next_page = False

    # On recupere le nom de la catégorie des livres
    category_name = soup.find("head").find("title").string
    category_name = category_name.split('|')[0].strip()
    
    books_href_extract(soup, one_category_books_href_list)

    # Presence de pages supplémentaires: On recherche la presence d'une balise <a> avec un intitulé 'next' 
    # Si ca match, on remplace le fichier html de la page courante par le href renseigné dans ce tag    
    next_page = find_next_page_url(soup, category_page_href)

    while next_page:
        response = book_details.test_page_access(next_page)
        if response is None:
            print(f"Pas de données pour : {next_page}")
            return
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraction des livres présents sur la nouvelle page
        books_href_extract(soup, one_category_books_href_list)

        # La page actuelle devient la 'next_page' chargée
        category_page_href = next_page

        # Recherche si une autre 'page suivante' existe
        next_page = find_next_page_url(soup, category_page_href)

    # Stockage dans un CSV des url de chaque livre de la catégorie
    csv_dir = os.path.join(PROJECT_ROOT, "csv_files")    # Creation d'un repertoire pour tous les CSV
    if not os.path.isdir(csv_dir):
        os.mkdir(csv_dir)
    os.chdir(csv_dir)

    category_dir = category_name.replace(' ', '_')    # Creation d'un sous-repertoire au nom de chaque categorie
    if not os.path.isdir(category_dir):
        os.mkdir(category_dir)
    os.chdir(category_dir)

    category_filename = "books_by_category_" + category_dir + "_"    # Nom du fichier des url des categories
    save_category_href_to_csv(category_filename, one_category_books_href_list, "w")

    # Pour chaque lien de la liste on appelle la fonction main du script 'book_details' 
    print("======= Extraction des données produit de chaque livre de la catégorie =======\n")
    details_filename = "details_"
    print(f"####### livre(s) dans {category_name}")
    for book_url in one_category_books_href_list:
        book_details.main(book_url, details_filename)
    print(f"####### Fichiers CSV de la categorie {category_name} créés #######\n")

    # Retour dans le repertoire parent 'csv_files'
    os.chdir("./..")
   

#================== Main script ===================

if __name__ == "__main__":
    category_page_href = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html"
    main(category_page_href)
