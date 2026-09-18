import requests
from bs4 import BeautifulSoup
import book_details
from urllib.parse import urljoin
import os

# Repertoire du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def books_url_extract(soup, books_url_list_by_category, books_url_list):
    # On extrait l'URL de chaque livre de la catégorie dans la <div> "image_container"
    ol = soup.find("ol", class_="row")
    for li in ol.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        href = li.find("div", class_="image_container").find("a").get("href")
        href = href.split('../')[3]    # on supprime les '../' pour adresser l'url absolue
        book_link = urljoin('https://books.toscrape.com/catalogue/', href)
        books_url_list.append(book_link)    # Les liens sont ajoutés dans la liste "books_url_list"
        books_url_list_by_category["books"] = books_url_list


def pagination(soup, category_url):
    # On verifie la presence de la classe 'pager'
    ul_pager = soup.find("ul", class_="pager")
    if ul_pager == None:
        return False

    # Si on y trouve un bouton 'next', on recupere l'url de la page suivante
    li_next = ul_pager.find("li", class_="next")
    if li_next:
        href_page = li_next.find("a").get("href")
        return urljoin(category_url, href_page)  
    return False    # Si pas de bouton 'next' trouve, alors on retourne False


def main(category_url):
    # Par defaut, la categorie = 'young adult'
    # On verifie l'acces à la page de la catégorie
    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

    books_url_list_by_category = {}     # Liste des URL de tous les livres d'une categorie
    books_url_list = []        # Liste
    next_page = False

    # On recupere la catégorie des livres dans le <head> et on la stocke dans le dico
    category = soup.find("head").find("title").string
    category = category.split('|')[0].strip()
    books_url_list_by_category["category"] = category
    
    books_url_extract(soup, books_url_list_by_category, books_url_list)

    # Page suivante
    # On recherche la presence d'une balise <a> avec un intitulé 'next' 
    # Si ca match, on remplace le fichier html de la page courante par le href renseigné dans ce tag    
    next_page = pagination(soup, category_url)

    while next_page:
        response = requests.get(next_page)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extraction des livres présents sur la nouvelle page
        books_url_extract(soup, books_url_list_by_category, books_url_list)

        # La page actuelle devient la page précédemment téléchargée
        category_url = next_page

        # Recherche de la page suivante à partir du nouveau soup
        next_page = pagination(soup, category_url)

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
    book_details.data_to_save_to_csv(filename_category, books_url_list_by_category, "w")

    # Extraire les données produit de chaque livre de la catégorie
    # Pour chaque lien de la liste on appelle la fonction main du script 'book_details' 
    print("======= Extraction des données produit de chaque livre de la catégorie =======\n")
    filename_detail = "details_"
    print(f"####### livre(s) dans {category}")
    for book_link in books_url_list: 
        book_details.main(book_link, filename_detail)
    print(f"####### Fichiers CSV de la categorie {category} créés #######\n")

    # Retour dans le repertoire parent
    os.chdir("./..")
    

#================== Main script ===================

if __name__ == "__main__":
    category_url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html"
    main(category_url)
