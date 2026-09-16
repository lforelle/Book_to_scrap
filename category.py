import requests
from bs4 import BeautifulSoup
import book_details
from urllib.parse import urljoin

def urls_extract(soup, url_books_list_by_category, books_list):
    # On extrait l'URL de chaque livre de la catégorie en recupèrant
    # les liens href des livres dans la <div> "image_container"
    # Les liens sont ajoutés dans la liste "books_list"  
    ol = soup.find("ol", class_="row")
    for li in ol.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        href = li.find("div", class_="image_container").find("a").get("href")
        # je supprime les '../' pour adresser l'url absolue
        href = href.split('../')[3]
        book_link = urljoin('https://books.toscrape.com/catalogue/', href)
        books_list.append(book_link)
        url_books_list_by_category["books"] = books_list


def pagination(soup, category_url):
    # On recherche la presence d'une balise <a> avec un intitulé 'next' et si ca match
    # on remplace le fichier html de la page courante par le href renseigné dans ce tag    
    ul_pager = soup.find("ul", class_="pager")
    a_pager = ul_pager.find("a")
    # tant que l'on trouve un bouton 'next', on accede à la page suivante et on relance l'extraction
    # sinon on stoppe l'execution
    if a_pager.text == "next":
        next_page = a_pager.get("href")
        category_url_mod = category_url.rstrip('lmth.xedni')
        url_next_page = urljoin(category_url_mod, next_page)
        return url_next_page


def main():
# categorie = Art
    category_url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
    
    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

    url_books_list_by_category = {}
    books_list = []
    page_suivante = False

# On recupere la catégorie des livres dans le <head> et on la stocke dans le dico
    category = soup.find("head").find("title").string
    category = category.split('|')[0].strip()
    url_books_list_by_category["category"] = category
    
    filename_category = "books_by_category_" + category + "_"
    filename_detail = "book_detail_"
    urls_extract(soup, url_books_list_by_category, books_list)

# Pagination
    # On recherche la presence d'une balise <a> avec un intitulé 'next' et si ca match
    # on remplace le fichier html de la page courante par le href renseigné dans ce tag    
    page_suivante = pagination(soup, category_url)
    while page_suivante:
        # Extraction URL de tous les livres de la catégorie
        urls_extract(soup, url_books_list_by_category, books_list)
        # On accede à la page suivante
        book_details.acces_page(page_suivante)
        print(f"!!!!! page {page_suivante} accedée pour lecture !!!!!!")
        page_suivante = ""


    print("\n============= Stockage csv des url de chaque livre de la catégorie ===============\n")
    print(url_books_list_by_category)
    book_details.data_to_save_to_csv(filename_category, url_books_list_by_category, "w")

# Extraire les données produit de chaque livre de la catégorie
    # Pour chaque lien de la liste on appelle la fonction main du script 'book_details' 
    print("\n============= Extraction des données produit de chaque livre de la catégorie ===============\n")
    for book_link in books_list:
        print(f"######## Traitement du livre : {book_link} ########\n")
        book_details.main(book_link, filename_detail)
        print(f"######### Fin du traitement : {book_link} #########\n")
    

if __name__ == "__main__":
    main()

