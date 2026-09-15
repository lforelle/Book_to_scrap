import requests
from bs4 import BeautifulSoup
import detail_livre
from urllib.parse import urljoin

def main():
# categorie = Art
    category_url = "https://books.toscrape.com/catalogue/category/books/art_25/index.html"

    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

    url_books_list_by_category = {}
    books_list = []

# On recupere la catégorie des produits dans le <head> et on la stocke dans le dico
    category = soup.find("head").find("title").string
    category = category.split('|')[0].strip()
    url_books_list_by_category["category"] = category
    filename_category = "books_by_category_" + category + "_"
    filename_detail = "book_detail_"

    # On extrait l'URL de la page Produit pour chaque livre de la catégorie.
    # en recupèrant les liens href des livres dans la <div> "image_container"
    # Les liens sont stockés dans la liste "books_list"
    ol = soup.find("ol", class_="row")
    for li in ol.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        href = li.find("div", class_="image_container").find("a").get("href")
        # je supprime les '../' pour adresser l'url absolue
        href = href.split('../')[3]
        book_link = urljoin('https://books.toscrape.com/catalogue/', href)
        books_list.append(book_link)
        url_books_list_by_category["books"] = books_list
    
    print("\n============= Extraction des url de chaque livre la catégorie ===============\n")
    print(url_books_list_by_category)
    detail_livre.data_to_save_to_csv(filename_category, url_books_list_by_category)
     
# Extraire les données produit de chaque livre de la catégorie
    # Pour chaque lien de la liste on appel la fonction 
    print("\n============= Extraction des données produit de chaque livre de la catégorie ===============\n")
    for book_link in books_list:
        print(f"######## Traitement du livre : {book_link} ########\n")
        detail_livre.main(book_link, filename_detail)
        print(f"######### Fin du traitement : {book_link} #########\n")

# inscrire les données dans un seul fichier CSV.
 
  

if __name__ == "__main__":
    main()

