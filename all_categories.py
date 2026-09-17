import requests
from bs4 import BeautifulSoup
import category
import book_details
from urllib.parse import urljoin

def categories_urls_extract(categories_url_list):
    # On extrait l'URL de chaque livre de la catégorie en recupèrant
    # les liens href des livres dans la <div> "image_container"
    # Les liens sont ajoutés dans la liste "books_url_list"  
    
    books_url_list=[]
    for url in categories_url_list:
        category_url = urljoin('https://books.toscrape.com/', url)
        books_url_list.append(category_url)
    return books_url_list

def main(site_url):
    # Par defaut le site est 'books_to_scrap'
    
    response = requests.get(site_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

    # dans la page d'accueil du site, on recupere toutes les url des categories de la navbar  
    categories_url_list = []
    ul_categories_list = soup.find("ul", class_="nav nav-list").find("li").find("ul")
    for li in ul_categories_list.find_all("li"):
        href = li.find("a").get("href")
        categories_url_list.append(href)
        #categories = li.find("a").get_text(strip=True)
        #print(categories, ":", href)

    # On boucle sur chaque categorie repertoriee, et on recupere la liste du lien url de chaque page categorie
    category_pages_url = categories_urls_extract(categories_url_list)
    print("\n",category_pages_url)
    for category_page_url in category_pages_url:
        # acceder à la categorie et recuperer les url des livres de cette page
        category.main(category_page_url)

 

if __name__ == "__main__":
    site_url = "https://books.toscrape.com/"
    main(site_url)