import requests
from bs4 import BeautifulSoup
import category
from urllib.parse import urljoin
import book_details


def categories_url_extract(categories_url_list):
    # On extrait l'URL de chaque livre de la catégorie
    # Les liens sont ajoutés dans la liste "books_url_list"  
    
    books_url_list=[]
    for url in categories_url_list:
        category_url = urljoin('https://books.toscrape.com/', url)
        books_url_list.append(category_url)
    return books_url_list


def main(site_url):
    # Par defaut le site est 'books_to_scrap'
    response = book_details.test_page_access(site_url)
    if response is None:
        print(f"Pas de données pour : {site_url}")
        return
    soup = BeautifulSoup(response.text, "html.parser")

    # Dans la page d'accueil du site, on recupere toutes les url des categories de la navbar  
    categories_url_list = []
    ul_categories_list = soup.find("ul", class_="nav nav-list").find("li").find("ul")
    for li in ul_categories_list.find_all("li"):
        href = li.find("a").get("href")
        categories_url_list.append(href)
        #categories = li.find("a").get_text(strip=True)
        #print(categories, ":", href)

    # On boucle sur chaque categorie repertoriee, et on recupere la liste du lien url de chaque page categorie
    category_pages_url = categories_url_extract(categories_url_list)
    print("\n",category_pages_url)
    for category_page_url in category_pages_url:
        # Acceder à la categorie et recuperer les url des livres de cette page
        category.main(category_page_url)
 

#================== Main script ===================

if __name__ == "__main__":
    site_url = "https://books.toscrape.com/"
    main(site_url)