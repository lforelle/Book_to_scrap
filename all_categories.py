from bs4 import BeautifulSoup
import category
from urllib.parse import urljoin
import book_details


def books_href_extract(all_categories_href_list):
    # On extrait l'URL des livres de chaque catégorie et on les ajoute dans une liste
    one_category_books_href_list=[]
    for url in all_categories_href_list:
        category_url = urljoin('https://books.toscrape.com/', url)
        one_category_books_href_list.append(category_url)
    return one_category_books_href_list


def main(site_url):
    # On verifie l'acces au site
    response = book_details.test_page_access(site_url)
    if response is None:
        print(f"Pas de données pour : {site_url}")
        return
    soup = BeautifulSoup(response.text, "html.parser")

    # Dans la page d'accueil du site, on liste les href de toutes les categories de la navbar  
    all_categories_href_list = []
    ul_categories_list = soup.find("ul", class_="nav nav-list").find("li").find("ul")
    for li in ul_categories_list.find_all("li"):
        href = li.find("a").get("href")
        all_categories_href_list.append(href)

    # On boucle sur chaque categorie de la navbar, et on liste les liens url des livres contenus dans chaque categorie
    category_pages_href = books_href_extract(all_categories_href_list)
    print("\n",category_pages_href)
    for category_page_href in category_pages_href:
        # Acceder à la page de la categorie et recuperer les href des livres de la page
        category.main(category_page_href)
 

#================== Main script ===================

if __name__ == "__main__":
    site_url = "https://books.toscrape.com/"
    main(site_url)