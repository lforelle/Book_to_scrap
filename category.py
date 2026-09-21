from bs4 import BeautifulSoup
import book_details
from urllib.parse import urljoin
import os
import csv

# Repertoire du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def book_href_extract(soup, one_category_books_href_list):
    # On extrait l'URL de chaque livre de la catégorie dans la <div> "image_container"
    ol = soup.find("ol", class_="row")
    for li in ol.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        image_container_href = li.find("div", class_="image_container").find("a").get("href")
        image_container_href = image_container_href.split('../')[3]    # on supprime les '../' pour adresser l'url absolue
        book_href = urljoin('https://books.toscrape.com/catalogue/', image_container_href)
        one_category_books_href_list.append(book_href)


def pagination(soup, category_page_href):
    # On verifie la presence de la classe 'pager'
    ul_pager = soup.find("ul", class_="pager")
    if ul_pager == None:
        return False

    # Si on y trouve un bouton 'next', on recupere l'url de la page suivante
    li_next = ul_pager.find("li", class_="next")
    if li_next:
        href_page = li_next.find("a").get("href")
        return urljoin(category_page_href, href_page)  
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

    one_category_books_href_list = []
    next_page = False

    # On recupere la catégorie des livres dans le <head> et on la stocke dans le dico
    category = soup.find("head").find("title").string
    category = category.split('|')[0].strip()
    
    book_href_extract(soup, one_category_books_href_list)

    # Page suivante
    # On recherche la presence d'une balise <a> avec un intitulé 'next' 
    # Si ca match, on remplace le fichier html de la page courante par le href renseigné dans ce tag    
    next_page = pagination(soup, category_page_href)

    while next_page:
        response = book_details.test_page_access(next_page)
        if response is None:
            print(f"Pas de données pour : {next_page}")
            return
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraction des livres présents sur la nouvelle page
        book_href_extract(soup, one_category_books_href_list)

        # La page actuelle devient la page précédemment téléchargée
        category_page_href = next_page

        # Recherche de la page suivante à partir du nouveau soup
        next_page = pagination(soup, category_page_href)

    # Stockage dans un CSV des url de chaque livre de la catégorie
    csv_dir = os.path.join(PROJECT_ROOT, "csv_files")    # Creation d'un repertoire pour tous les CSV
    if not os.path.isdir(csv_dir):
        os.mkdir(csv_dir)
    os.chdir(csv_dir)

    category_dir = category.replace(' ', '_')    # Creation d'un sous-repertoire pour chaque categorie
    if not os.path.isdir(category_dir):
        os.mkdir(category_dir)
    os.chdir(category_dir)

    filename_category = "books_by_category_" + category_dir + "_"
    save_category_href_to_csv(filename_category, one_category_books_href_list, "w")

    # Extraire les données produit de chaque livre de la catégorie
    # Pour chaque lien de la liste on appelle la fonction main du script 'book_details' 
    print("======= Extraction des données produit de chaque livre de la catégorie =======\n")
    filename_detail = "details_"
    print(f"####### livre(s) dans {category}")
    for book_href in one_category_books_href_list:
        book_details.main(book_href, filename_detail)
    print(f"####### Fichiers CSV de la categorie {category} créés #######\n")

    # Retour dans le repertoire parent
    os.chdir("./..")
    

#================== Main script ===================

if __name__ == "__main__":
    category_page_href = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html"
    main(category_page_href)
