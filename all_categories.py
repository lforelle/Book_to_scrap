from bs4 import BeautifulSoup
import category
from urllib.parse import urljoin
import book_details


def absolute_url_extract(all_categories_href_list):
    # On extrait l'URL absolue de chaque catégorie et on les liste
    all_categories_absolute_url_list=[]
    for url in all_categories_href_list:
        category_absolute_url = urljoin('https://books.toscrape.com/', url)
        all_categories_absolute_url_list.append(category_absolute_url)
    return all_categories_absolute_url_list


def main(site_url):
    # On verifie l'acces au site "https://books.toscrape.com/"
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

    # On boucle sur chaque categorie de la navbar, et on liste les liens url absolus de chaque categorie
    all_categories_absolute_url = absolute_url_extract(all_categories_href_list)
    print("\n",all_categories_absolute_url)
    for category_url in all_categories_absolute_url:
        # On accede à la page de la categorie pour recuperer les href des livres de la page
        category.main(category_url)
 

#================== Main script ===================

if __name__ == "__main__":
    site_url = "https://books.toscrape.com/"
    main(site_url)